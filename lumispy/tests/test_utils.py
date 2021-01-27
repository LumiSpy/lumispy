# -*- coding: utf-8 -*-
# Copyright 2019 The LumiSpy developers
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

from pytest import raises, mark, skip
from numpy import ones, arange
from numpy.random import random

from hyperspy.axes import DataAxis

from lumispy.signals import LumiSpectrum
from lumispy import join_spectra


@mark.parametrize(("average"), (True,False))
@mark.parametrize(("scale"), (True,False))
@mark.parametrize(("kind"), ('slinear','linear'))
def test_joinspectra(average, scale, kind):
    s1 = LumiSpectrum(arange(32))
    s2 = LumiSpectrum(arange(32)+25)
    s3 = LumiSpectrum(arange(32)+50)
    s2.axes_manager.signal_axes[0].offset = 25
    s3.axes_manager.signal_axes[0].offset = 50
    s = join_spectra([s1,s2,s3], r=2, average=average, scale=scale, kind=kind)
    assert s.data[-1] == 81
    assert s.axes_manager.signal_axes[0].scale == 1
    assert s.axes_manager.signal_axes[0].size == 82
    
def test_joinspectra2():
    s1 = LumiSpectrum(arange(32))
    s2 = LumiSpectrum(arange(32)+25)
    s2.axes_manager.signal_axes[0].offset = 25
    s2.isig[3] = 0
    s = join_spectra([s1,s2], r=2, average=True, scale=True)
    assert s.data[-1] == 56
    assert s.data[28] == 28/3

def test_joinspectra_errors():
    s1 = LumiSpectrum(ones(32))
    s2 = LumiSpectrum(ones(32)*2)
    s2.axes_manager.signal_axes[0].offset = 25
    # Test that catch for r works
    raises(ValueError, join_spectra, [s1,s2])
    s2.axes_manager.signal_axes[0].offset = 35
    # Test that overlap catch works
    raises(ValueError, join_spectra, [s1,s2], r=2)
    s1.data*=-1
    s2.axes_manager.signal_axes[0].offset = 25
    raises(ValueError, join_spectra, [s1,s2], r=2)

@mark.parametrize(("average"), (True,False))
@mark.parametrize(("scale"), (True,False))
@mark.parametrize(("kind"), ('slinear','linear'))
def test_joinspectra_linescan(average, scale, kind):
    s1 = LumiSpectrum(random((4,64)))
    s2 = LumiSpectrum(random((4,64)))
    s2.axes_manager.signal_axes[0].offset = 47
    s = join_spectra([s1,s2], r=7, average=average, scale=scale, kind=kind)
    assert s.axes_manager.signal_axes[0].size == 111
    assert s.axes_manager.signal_axes[0].scale == 1
    
@mark.parametrize(("average"), (True,False))
@mark.parametrize(("scale"), (True,False))
@mark.parametrize(("kind"), ('slinear','linear'))
def test_joinspectra_nonuniform(average, scale, kind):
    try:
        from hyperspy.axes import UniformDataAxis
    except ImportError:
        skip("HyperSpy version doesn't support non-uniform axis")
    s1 = LumiSpectrum(arange(32))
    s2 = LumiSpectrum(arange(32)+25)
    s2.axes_manager.signal_axes[0].offset = 25
    s1.axes_manager.signal_axes[0].convert_to_non_uniform_axis()
    s = join_spectra([s1,s2], r=2, average=average, scale=scale, kind=kind)
    assert s.axes_manager.signal_axes[0].is_uniform == False
    assert s.axes_manager.signal_axes[0].size == 57
    assert s.axes_manager.signal_axes[0].axis[-1] == 56
    assert s.data.size == 57
    assert s.data[-1] == 56
    s1 = LumiSpectrum(arange(12))
    s2 = LumiSpectrum(arange(12)+3.8, axes=[DataAxis(axis = arange(12)+3.8)])
    s = join_spectra([s1,s2], r=2, average=average, scale=scale, kind=kind)
    assert s.axes_manager[0].axis.size == 16
    assert s.data.size == 16
    assert s.data[-1] == 14.8

@mark.parametrize(("average"), (True,False))
@mark.parametrize(("scale"), (True,False))
@mark.parametrize(("kind"), ('slinear','linear'))
def test_joinspectra_FunctionalDA(average, scale, kind):
    try:
        from hyperspy.axes import FunctionalDataAxis
    except ImportError:
        skip("HyperSpy version doesn't support non-uniform axis")
    s1 = LumiSpectrum(ones(32))
    s2 = LumiSpectrum(ones(32)*2)
    s2.axes_manager.signal_axes[0].offset = 25
    s1.axes_manager.signal_axes[0].convert_to_functional_data_axis(expression='x**2')
    s2.axes_manager.signal_axes[0].convert_to_functional_data_axis(expression='x**2')
    s = join_spectra([s1,s2], r=2, average=average, scale=scale, kind=kind)
    assert s.axes_manager.signal_axes[0].is_uniform == False
    assert s.axes_manager.signal_axes[0].size == 57
    assert s.axes_manager.signal_axes[0].axis[-1] == 3136
    assert s.data.size == 57
    if scale: assert s.data[-1] == 1
    else: assert s.data[-1] == 2
