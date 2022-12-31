# -*- coding: utf-8 -*-
# Copyright 2019-2022 The LumiSpy developers
#
# This file is part of LumiSpy.
#
# LumiSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the license, or
# (at your option) any later version.
#
# LumiSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LumiSpy. If not, see <https://www.gnu.org/licenses/#GPL>.

from numpy import ones, arange, all
from numpy.random import random
from numpy.testing import assert_allclose
from pytest import raises, mark, skip, warns

from hyperspy.axes import DataAxis
from hyperspy.signals import Signal1D, Signal2D
from lumispy import join_spectra, nm2eV, eV2nm, nm2invcm, invcm2nm
from lumispy.utils.axes import _n_air, crop_edges
from lumispy.signals import LumiSpectrum


def test__n_air():
    wl = arange(800) * 2 + 150
    with warns(UserWarning, match="The wavelength"):
        n = _n_air(wl)
    assert n[0] == _n_air(185)
    assert n[-1] == _n_air(1700)
    with warns(UserWarning):
        assert _n_air(180) == _n_air(185)
    with warns(UserWarning):
        assert _n_air(1705) == _n_air(1700)
    assert_allclose(_n_air(200), 1.00032406)
    assert_allclose(_n_air(500), 1.00027896)


def test_nm2eV():
    assert_allclose(nm2eV(200), 6.19720164)
    assert_allclose(nm2eV(300), 4.13160202)


def test_eV2nm():
    assert_allclose(eV2nm(2), 619.74951462)
    assert_allclose(eV2nm(3), 413.16411768)


def test_nm2invcm():
    assert nm2invcm(250) == 4e4
    assert nm2invcm(400) == 25e3


def test_invcm2nm():
    assert invcm2nm(4e4) == 250
    assert invcm2nm(25e3) == 400


@mark.parametrize(("average"), (True, False))
@mark.parametrize(("scale"), (True, False))
@mark.parametrize(("kind"), ("slinear", "linear"))
def test_joinspectra(average, scale, kind):
    s1 = LumiSpectrum(arange(32))
    s2 = LumiSpectrum(arange(32) + 25)
    s3 = LumiSpectrum(arange(32) + 50)
    s2.axes_manager.signal_axes[0].offset = 25
    s3.axes_manager.signal_axes[0].offset = 50
    s = join_spectra([s1, s2, s3], r=2, average=average, scale=scale, kind=kind)
    assert s.data[-1] == 81
    assert s.axes_manager.signal_axes[0].scale == 1
    assert s.axes_manager.signal_axes[0].size == 82


def test_joinspectra2():
    s1 = LumiSpectrum(arange(32))
    s2 = LumiSpectrum(arange(32) + 25)
    s2.axes_manager.signal_axes[0].offset = 25
    s2.isig[3] = 0
    s = join_spectra([s1, s2], r=2, average=True, scale=True)
    assert s.data[-1] == 56
    assert s.data[28] == 28 / 3


def test_joinspectra_length1():
    s1 = LumiSpectrum(arange(32))
    s2 = LumiSpectrum(arange(32) + 27)
    s2.axes_manager.signal_axes[0].offset = 27
    s = join_spectra([s1, s2], r=1, average=False, scale=True)
    assert s.data[-1] == 58
    with raises(ValueError, match="Averaging can not be performed for r=1."):
        s = join_spectra([s1, s2], r=1, average=True, scale=True)
    s1.axes_manager[0].convert_to_non_uniform_axis()
    s2.axes_manager[0].convert_to_non_uniform_axis()
    s = join_spectra([s1, s2], r=1, average=True, scale=True)
    assert s.data[-1] == 58


def test_joinspectra_errors():
    s1 = LumiSpectrum(ones(32))
    s2 = LumiSpectrum(ones(32) * 2)
    s2.axes_manager.signal_axes[0].offset = 25
    # Test that catch for r works
    raises(ValueError, join_spectra, [s1, s2])
    s2.axes_manager.signal_axes[0].offset = 35
    # Test that overlap catch works
    raises(ValueError, join_spectra, [s1, s2], r=2)
    s1.data *= -1
    s2.axes_manager.signal_axes[0].offset = 25
    raises(ValueError, join_spectra, [s1, s2], r=2)


@mark.parametrize(("average"), (True, False))
@mark.parametrize(("scale"), (True, False))
@mark.parametrize(("kind"), ("slinear", "linear"))
def test_joinspectra_linescan(average, scale, kind):
    s1 = LumiSpectrum(random((4, 64)))
    s2 = LumiSpectrum(random((4, 64)))
    s2.axes_manager.signal_axes[0].offset = 47
    s = join_spectra([s1, s2], r=7, average=average, scale=scale, kind=kind)
    assert s.axes_manager.signal_axes[0].size == 111
    assert s.axes_manager.signal_axes[0].scale == 1


@mark.parametrize(("average"), (True, False))
@mark.parametrize(("scale"), (True, False))
@mark.parametrize(("kind"), ("slinear", "linear"))
def test_joinspectra_nonuniform(average, scale, kind):
    s1 = LumiSpectrum(arange(32))
    s2 = LumiSpectrum(arange(32) + 25)
    s2.axes_manager.signal_axes[0].offset = 25
    s1.axes_manager.signal_axes[0].convert_to_non_uniform_axis()
    s = join_spectra([s1, s2], r=2, average=average, scale=scale, kind=kind)
    assert s.axes_manager.signal_axes[0].is_uniform == False
    assert s.axes_manager.signal_axes[0].size == 57
    assert s.axes_manager.signal_axes[0].axis[-1] == 56
    assert s.data.size == 57
    assert s.data[-1] == 56
    s1 = LumiSpectrum(arange(12))
    s2 = LumiSpectrum(arange(12) + 3.8, axes=[DataAxis(axis=arange(12) + 3.8)])
    s = join_spectra([s1, s2], r=2, average=average, scale=scale, kind=kind)
    assert s.axes_manager[0].axis.size == 16
    assert s.data.size == 16
    assert s.data[-1] == 14.8


@mark.parametrize(("average"), (True, False))
@mark.parametrize(("scale"), (True, False))
@mark.parametrize(("kind"), ("slinear", "linear"))
def test_joinspectra_FunctionalDA(average, scale, kind):
    try:
        from hyperspy.axes import FunctionalDataAxis
    except ImportError:
        skip("HyperSpy version doesn't support non-uniform axis")
    s1 = LumiSpectrum(ones(32))
    s2 = LumiSpectrum(ones(32) * 2)
    s2.axes_manager.signal_axes[0].offset = 25
    s1.axes_manager.signal_axes[0].convert_to_functional_data_axis(expression="x**2")
    s2.axes_manager.signal_axes[0].convert_to_functional_data_axis(expression="x**2")
    s = join_spectra([s1, s2], r=2, average=average, scale=scale, kind=kind)
    assert s.axes_manager.signal_axes[0].is_uniform == False
    assert s.axes_manager.signal_axes[0].size == 57
    assert s.axes_manager.signal_axes[0].axis[-1] == 3136
    assert s.data.size == 57
    if scale:
        assert s.data[-1] == 1
    else:
        assert s.data[-1] == 2
    # test that join_spectra works for r that is float not int
    s = join_spectra([s1, s2], r=2.1, average=average, scale=scale, kind=kind)


# Test axes utils
# -----------


@mark.parametrize(
    "range, output",
    [
        (2, (6, 6)),
        ((2, 4), (6, 2)),
        ((1, 2, 3, 4), (6, 4)),
        ((1, 2, 3), ()),
        ((1, 2, 3, 4, 5), ()),
        ("s", ()),
        ((1, 0, 0, 3), (9, 7)),
        ((None), (10, 10)),
    ],
)
def test_crop_edges_s(range, output):
    s1 = [LumiSpectrum(ones((10, 10, 10)))]

    # Check for bad input range
    if type(range) not in (int, float, tuple, type(None)):
        with raises(ValueError, match="value must be a number or a tuple"):
            crop_edges(s1, range)

    elif type(range) == tuple and len(range) not in (1, 2, 4):
        with raises(ValueError, match="tuple must be either a"):
            crop_edges(s1, range)

    else:
        s1 = crop_edges(s1, range)
        assert s1[0].axes_manager.navigation_shape[0] == output[0]
        assert s1[0].axes_manager.navigation_shape[1] == output[1]


def test_crop_percent_and_single_spectrum():
    s1 = LumiSpectrum(ones((10, 10, 10)))
    s2 = crop_edges(s1, crop_range=0.1, crop_units="percent")
    assert s2.axes_manager.navigation_shape[0] == 8
    assert s2.axes_manager.navigation_shape[1] == 8
    s2 = crop_edges(s1, crop_range=10, crop_units="%")
    assert s2.axes_manager.navigation_shape[0] == 8
    assert s2.axes_manager.navigation_shape[1] == 8


@mark.parametrize("units", ["pixel", "px", "PIXEL", "percent", "pixels", "%", "nm"])
def test_crop_edges_units(units):
    s1 = LumiSpectrum(ones((10, 10, 10)))

    # Check for bad units
    if units.lower() not in ("px", "pixel", "pixels", "percent", "%"):
        with raises(ValueError, match="only accepts the strings"):
            crop_edges(s1, crop_range=1, crop_units=units)


def test_crop_edges_metadata():
    s1 = LumiSpectrum(ones((10, 10, 10)))
    s1 = crop_edges(s1, crop_range=2)
    assert all(s1.metadata.Signal.cropped_edges == 2)
    s1 = crop_edges(s1, crop_range=2)
    assert all(s1.metadata.Signal.cropped_edges == 4)


def test_crop_edges_too_far():
    s1 = LumiSpectrum(ones((10, 10, 10)))
    with raises(IndexError, match="The pixels to be cropped"):
        crop_edges(s1, crop_range=6)


@mark.parametrize(
    "range, output",
    [
        (2, (6)),
        ((2, 4), (4)),
        ((1, 2, 3, 4), ()),
        ((1, 2, 3), ()),
    ],
)
def test_crop_edges_linescan(range, output):
    s1 = [LumiSpectrum(ones((10, 10)))]

    if type(range) == tuple and len(range) not in (1, 2):
        with raises(ValueError, match="tuple must be either a"):
            crop_edges(s1, range)

    else:
        s1 = crop_edges(s1, range)
        assert s1[0].axes_manager.navigation_shape[0] == output


@mark.parametrize("data", [((10,) * 4), ((10,) * 5)])
def test_crop_edges_multidim(data):
    s1 = [LumiSpectrum(ones((data)))]
    with raises(NotImplementedError, match="navigation axes with more than 2"):
        crop_edges(s1, 2)


def test_crop_edges_depreciated():
    s1 = LumiSpectrum(ones((10, 10, 10)))
    with warns(DeprecationWarning, match="is deprecated"):
        s2 = crop_edges(s1, crop_px=1)
    assert s2.axes_manager.navigation_shape[0] == 8
    assert s2.axes_manager.navigation_shape[1] == 8
    with raises(TypeError, match="Both"):
        crop_edges(s1, crop_range=2, crop_px=2)


def test_crop_edges_multiple_no_rebin():
    s1 = [LumiSpectrum(ones((10, 10, 10)))] * 2
    s2 = crop_edges(s1, crop_range=1, rebin_nav=False)
    for s in s2:
        assert s.axes_manager.navigation_shape[0] == 8
        assert s.axes_manager.navigation_shape[1] == 8
    s1 = [
        LumiSpectrum(ones((10, 10, 10))),
    ] * 3
    s2 = crop_edges(s1, crop_range=1, rebin_nav=False)
    for s in s2:
        assert s.axes_manager.navigation_shape[0] == 8
        assert s.axes_manager.navigation_shape[1] == 8

    s1 = [
        LumiSpectrum(ones((10, 10, 10))),
        Signal1D(ones((10, 10, 10))),
        Signal2D(ones((10, 10, 10, 10))),
    ]
    s2 = crop_edges(s1, crop_range=1, rebin_nav=False)
    for s in s2:
        assert s.axes_manager.navigation_shape[0] == 8
        assert s.axes_manager.navigation_shape[1] == 8

    s1 = [
        LumiSpectrum(ones((10, 10, 10))),
        LumiSpectrum(ones((20, 5, 10))),
    ]
    s2 = crop_edges(s1, crop_range=1, rebin_nav=False)
    assert s2[0].axes_manager.navigation_shape[0] == 8
    assert s2[0].axes_manager.navigation_shape[1] == 8
    assert s2[1].axes_manager.navigation_shape[0] == 3
    assert s2[1].axes_manager.navigation_shape[1] == 18


def test_crop_edges_multiple_error():
    s1 = [
        LumiSpectrum(ones((10, 10, 10))),
        LumiSpectrum(ones((10, 10))),
    ]
    with raises(ValueError, match="mix of navigation axes"):
        crop_edges(s1, 1)


def test_crop_edges_multiple_rebin():
    s1 = [
        LumiSpectrum(ones((10, 10, 10))),
        LumiSpectrum(ones((20, 20, 10))),
        LumiSpectrum(ones((5, 5, 10))),
        LumiSpectrum(ones((13, 7, 10))),
        LumiSpectrum(ones((5, 20, 5))),
    ]
    s2 = crop_edges(s1, crop_range=1, rebin_nav=True)
    for s in s2:
        assert s.axes_manager.navigation_shape[0] == 8
        assert s.axes_manager.navigation_shape[1] == 8
    # Check signal axis has not been changed
    assert s2[0].axes_manager.signal_shape[0] == 10
    assert s2[-1].axes_manager.signal_shape[0] == 5
