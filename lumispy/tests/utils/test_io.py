# -*- coding: utf-8 -*-
# Copyright 2019-2021 The LumiSpy developers
#
# This file is part of LumiSpy.
#
# LumiSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LumiSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LumiSpy.  If not, see <http://www.gnu.org/licenses/>.

from pytest import raises, mark
from numpy import loadtxt, arange
from numpy.testing import assert_array_equal

from hyperspy.signals import Signal2D

from lumispy.signals import LumiSpectrum
from lumispy import savetxt


@mark.parametrize("axes", (True, False))
def test_to_array_spectrum(axes):
    s = LumiSpectrum(arange(5))
    a = s.to_array(axes=axes)
    if axes:
        assert_array_equal(s.axes_manager[0].axis, a[:, 0])
    else:
        assert_array_equal(s.data, a)


@mark.parametrize("axes", (True, False))
@mark.parametrize("transpose", (True, False))
def test_to_array_linescan(axes, transpose):
    s = LumiSpectrum(arange(20).reshape((4, 5)))
    a = s.to_array(axes=axes, transpose=transpose)
    if axes:
        if transpose:
            assert_array_equal(s.axes_manager[0].axis, a[0, 1:])
            assert_array_equal(s.axes_manager[1].axis, a[1:, 0])
            assert_array_equal(s.data.T, a[1:, 1:])
        else:
            assert_array_equal(s.axes_manager[1].axis, a[0, 1:])
            assert_array_equal(s.axes_manager[0].axis, a[1:, 0])
            assert_array_equal(s.data, a[1:, 1:])
    else:
        if transpose:
            assert_array_equal(s.data.T, a)
        else:
            assert_array_equal(s.data, a)


@mark.parametrize("axes", (True, False))
def test_savetxt_spectrum(axes, tmp_path):
    s = LumiSpectrum(arange(5))
    fname = tmp_path / "test.txt"
    s.savetxt(fname, axes=axes)
    s2 = loadtxt(fname)
    if axes:
        assert_array_equal(s.axes_manager[0].axis, s2[:, 0])
    else:
        assert_array_equal(s.data, s2)


@mark.parametrize("axes", (True, False))
def test_savetxt_navigate1D(axes, tmp_path):
    s = LumiSpectrum(arange(5))
    s.axes_manager[0].navigate = True
    fname = tmp_path / "test.txt"
    s.savetxt(fname, axes=axes)
    s2 = loadtxt(fname)
    if axes:
        assert_array_equal(s.axes_manager[0].axis, s2[:, 0])
    else:
        assert_array_equal(s.data, s2)


@mark.parametrize("axes", (True, False))
@mark.parametrize("transpose", (True, False))
def test_savetxt_linescan(axes, transpose, tmp_path):
    s = LumiSpectrum(arange(20).reshape((4, 5)))
    fname = tmp_path / "test.txt"
    s.savetxt(fname, axes=axes, transpose=transpose)
    s2 = loadtxt(fname)
    if axes:
        if transpose:
            assert_array_equal(s.axes_manager[0].axis, s2[0, 1:])
            assert_array_equal(s.axes_manager[1].axis, s2[1:, 0])
            assert_array_equal(s.data.T, s2[1:, 1:])
        else:
            assert_array_equal(s.axes_manager[1].axis, s2[0, 1:])
            assert_array_equal(s.axes_manager[0].axis, s2[1:, 0])
            assert_array_equal(s.data, s2[1:, 1:])
    else:
        if transpose:
            assert_array_equal(s.data.T, s2)
        else:
            assert_array_equal(s.data, s2)


@mark.parametrize("axes", (True, False))
@mark.parametrize("transpose", (True, False))
def test_savetxt_signal2D(axes, transpose, tmp_path):
    s = Signal2D(arange(20).reshape((4, 5)))
    fname = tmp_path / "test.txt"
    savetxt(s, fname, axes=axes, transpose=transpose)
    s2 = loadtxt(fname)
    if axes:
        if transpose:
            assert_array_equal(s.axes_manager[1].axis, s2[0, 1:])
            assert_array_equal(s.axes_manager[0].axis, s2[1:, 0])
            assert_array_equal(s.data.T, s2[1:, 1:])
        else:
            assert_array_equal(s.axes_manager[0].axis, s2[0, 1:])
            assert_array_equal(s.axes_manager[1].axis, s2[1:, 0])
            assert_array_equal(s.data, s2[1:, 1:])
    else:
        if transpose:
            assert_array_equal(s.data.T, s2)
        else:
            assert_array_equal(s.data, s2)


@mark.parametrize("axes", (True, False))
@mark.parametrize("transpose", (True, False))
def test_savetxt_navigate2D(axes, transpose, tmp_path):
    s = Signal2D(arange(20).reshape((4, 5)))
    s.axes_manager[0].navigate = True
    s.axes_manager[1].navigate = True
    fname = tmp_path / "test.txt"
    savetxt(s, fname, axes=axes, transpose=transpose)
    s2 = loadtxt(fname)
    if axes:
        if transpose:
            assert_array_equal(s.axes_manager[1].axis, s2[0, 1:])
            assert_array_equal(s.axes_manager[0].axis, s2[1:, 0])
            assert_array_equal(s.data.T, s2[1:, 1:])
        else:
            assert_array_equal(s.axes_manager[0].axis, s2[0, 1:])
            assert_array_equal(s.axes_manager[1].axis, s2[1:, 0])
            assert_array_equal(s.data, s2[1:, 1:])
    else:
        if transpose:
            assert_array_equal(s.data.T, s2)
        else:
            assert_array_equal(s.data, s2)


def test_savetxt_dimension_error(tmp_path):
    s = LumiSpectrum(arange(60).reshape((3, 4, 5)))
    fname = tmp_path / "test.txt"
    with raises(NotImplementedError):
        s.savetxt(fname)


def test_to_array_dimension_error():
    s = LumiSpectrum(arange(60).reshape((3, 4, 5)))
    with raises(NotImplementedError):
        s.to_array()
