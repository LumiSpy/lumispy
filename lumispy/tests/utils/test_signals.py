# -*- coding: utf-8 -*-
# Copyright 2019-2025 The LumiSpy developers
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

from lumispy.utils.signals import com, crop_edges
from hyperspy.axes import FunctionalDataAxis, DataAxis, UniformDataAxis
from numpy import ones, array
from numpy.testing import assert_allclose
from pytest import raises, mark, warns
from hyperspy.signals import Signal1D, Signal2D
from lumispy.signals import LumiSpectrum


@mark.parametrize(
    "axis, output",
    [
        (
            FunctionalDataAxis(
                **{
                    "expression": "a * x + b",
                    "a": 1,
                    "b": 0,
                },
                size=2
            ),
            0.5,
        ),
        (DataAxis(axis=[0.0, 1.0]), 0.5),
        (UniformDataAxis(size=2), 0.5),
    ],
)
def test_com_axes(axis, output):
    intensities = array([1, 1])

    centroid = com(intensities, axis)
    assert_allclose(centroid, output, atol=0.1)


def test_com_list():
    # Float without decimals as index for centroid
    wavelengths = [200, 300, 400, 500, 600, 700]
    intensities = array([1, 2, 3, 2, 1, 0])
    centroid = com(intensities, wavelengths)
    assert_allclose(centroid, 400.0, atol=0.1)

    # Float with decimals as index for centroid
    wavelengths = [
        200,
        300,
    ]
    intensities = array(
        [
            1,
            1,
        ]
    )
    centroid = com(intensities, wavelengths)
    assert_allclose(centroid, 250.0, atol=0.1)


def test_com_inputs():
    with raises(ValueError, match="The length of the spectrum array"):
        com(ones(2), ones(3))
    with raises(ValueError):
        com(ones(3), ones(2))
    with raises(
        ValueError, match="The parmeter `signal_axis` must be a HyperSpy Axis object."
    ):
        com(ones(3), "string")


#
# Test navigation axis utils
#


@mark.parametrize(
    "range, output",
    [
        (2, (6, 6)),
        (2.0, (6, 6)),
        ((2, 4), (6, 2)),
        ((2.0, 4.0), (6, 2)),
        ((1, 2, 3, 4), (6, 4)),
        ((1.0, 8.0, 7.0, 4.0), (6, 4)),
        ((1, 2, 3), ()),
        ((1, 2, 3, 4, 5), ()),
        (True, ()),
        ((1, 0, 0, 3), (9, 7)),
        ((None), (10, 10)),
    ],
)
def test_crop_edges_s(range, output):
    s1 = [LumiSpectrum(ones((10, 10, 10)))]

    # Check for bad input range
    if type(range) not in (int, float, tuple, str, type(None)):
        with raises(ValueError, match="value must be a number,"):
            crop_edges(s1, range)

    elif type(range) == tuple and len(range) not in (1, 2, 4):
        with raises(ValueError, match="tuple must be either a"):
            crop_edges(s1, range)

    else:
        s1 = crop_edges(s1, range)
        assert s1[0].axes_manager.navigation_shape[0] == output[0]
        assert s1[0].axes_manager.navigation_shape[1] == output[1]


@mark.parametrize(
    "error, range, output",
    [
        (False, "1nm", (8, 8)),
        (False, "rel0.1", (8, 8)),
        (False, ("rel0.2", "rel0.4"), (6, 2)),
        (False, ("2nm", "4nm"), (6, 2)),
        (False, ("rel0.1", "rel0.8", "rel0.3", "rel0.2"), (2, 5)),
        (False, ("1nm", "8nm", "7nm", "4nm"), (6, 4)),
        (True, "a", ()),
        (True, "11", ()),
    ],
)
def test_crop_edges_fancy_str(error, range, output):
    s1 = [LumiSpectrum(ones((10, 10, 10)))]
    s1[0].axes_manager.navigation_axes[0].units = "nm"
    s1[0].axes_manager.navigation_axes[1].units = "nm"

    # Check for bad input range
    if error:
        with raises(ValueError):
            crop_edges(s1, range)

    else:
        s1 = crop_edges(s1, range)
        assert s1[0].axes_manager.navigation_shape[0] == output[0]
        assert s1[0].axes_manager.navigation_shape[1] == output[1]


def test_crop_single_spectrum():
    s1 = LumiSpectrum(ones((10, 10, 10)))
    s2 = crop_edges(
        s1,
        crop_range=1.0,
    )
    assert s2.axes_manager.navigation_shape[0] == 8
    assert s2.axes_manager.navigation_shape[1] == 8
    s2 = crop_edges(
        s1,
        crop_range=1,
    )
    assert s2.axes_manager.navigation_shape[0] == 8
    assert s2.axes_manager.navigation_shape[1] == 8


def test_crop_edges_metadata():
    s1 = LumiSpectrum(ones((10, 10, 10)))
    s2 = crop_edges(s1, crop_range=2)
    assert (s2.metadata.Signal.cropped_edges == array([2, -2, -2, 2])).all()
    s2 = crop_edges(s1, crop_range="rel0.1")
    assert (s2.metadata.Signal.cropped_edges == array([1, -1, -1, 1])).all()
    s3 = crop_edges(s2, crop_range=1)
    assert (
        s3.metadata.Signal.cropped_edges == array([[1, -1, -1, 1], [1, -1, -1, 1]])
    ).all()


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
        ("2nm", (6)),
        (("2nm", "4nm"), (2)),
    ],
)
def test_crop_edges_linescan(range, output):
    s1 = [LumiSpectrum(ones((10, 10)))]
    s1[0].axes_manager.navigation_axes[0].units = "nm"

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


def test_crop_edges_deprecated():
    s1 = LumiSpectrum(ones((10, 10, 10)))
    with warns(DeprecationWarning, match="is deprecated"):
        s2 = crop_edges(s1, crop_px=1)
    assert s2.axes_manager.navigation_shape[0] == 8
    assert s2.axes_manager.navigation_shape[1] == 8
    with warns(DeprecationWarning, match="Both"):
        s2 = crop_edges(s1, crop_range=1, crop_px=2)
    assert s2.axes_manager.navigation_shape[0] == 8
    assert s2.axes_manager.navigation_shape[1] == 8


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
