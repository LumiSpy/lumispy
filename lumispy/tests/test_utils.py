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

from numpy import ones
from numpy.random import random
from pytest import raises
#from numpy.testing import assert_allclose

from hyperspy.signals import Signal1D
from hyperspy.axes import DataAxis
from lumispy import join_spectra


def test_joinspectra():
    s1 = Signal1D(ones(32))
    s2 = Signal1D(ones(32)*2)
    s2.axes_manager.signal_axes[0].offset = 25
    s = join_spectra([s1,s2],r=2)
    assert s.data[-1] == 1
    assert s.axes_manager.signal_axes[0].scale == 1
    s = join_spectra([s1,s2],r=2,average=True)
    assert s.data[-1] == 1
    assert s.axes_manager.signal_axes[0].scale == 1
    # Also check for (non-uniform) DataAxis
    s1.axes_manager.signal_axes[0].convert_to_non_uniform_axis()
    s = join_spectra([s1,s2],r=2)
    assert s.axes_manager.signal_axes[0].is_uniform == False
    assert s.axes_manager.signal_axes[0].size == 57
    assert s.axes_manager.signal_axes[0].axis[-1] == 56
    assert s.data.size == 57
    assert s.data[-1] == 1
    s = join_spectra([s1,s2],r=2,average=True)
    assert s.data.size == 57
    assert s.axes_manager.signal_axes[0].size == 57
    s1.axes_manager.signal_axes[0].convert_to_non_uniform_axis()
    s = join_spectra([s1,s2],r=2)
    assert s.axes_manager.signal_axes[0].is_uniform == False
    assert s.axes_manager.signal_axes[0].size == 57
    assert s.axes_manager.signal_axes[0].axis[-1] == 56
    assert s.data.size == 57
    assert s.data[-1] == 1
    s = join_spectra([s1,s2],r=2,average=True)
    assert s.data.size == 57
    assert s.axes_manager.signal_axes[0].size == 57
    
def test_joinspectra_Errors():
    s1 = Signal1D(ones(32))
    s2 = Signal1D(ones(32)*2)
    s2.axes_manager.signal_axes[0].offset = 25
    # Test that catch for r works
    raises(ValueError,join_spectra,[s1,s2])
    s2.axes_manager.signal_axes[0].offset = 35
    # Test that overlap catch works
    raises(ValueError,join_spectra,[s1,s2])
    
def test_joinspectra_FunctionalDA():
    s1 = Signal1D(ones(32))
    s2 = Signal1D(ones(32)*2)
    s2.axes_manager.signal_axes[0].offset = 25
    s1.axes_manager.signal_axes[0].convert_to_functional_data_axis(expression='x**2')
    s2.axes_manager.signal_axes[0].convert_to_functional_data_axis(expression='x**2')
    s = join_spectra([s1,s2],r=2)
    assert s.axes_manager.signal_axes[0].is_uniform == False
    assert s.axes_manager.signal_axes[0].size == 57
    assert s.axes_manager.signal_axes[0].axis[-1] == 3136
    assert s.data.size == 57
    assert s.data[-1] == 1
    s = join_spectra([s1,s2],r=2,average=True)
    assert s.data.size == 57
    assert s.axes_manager.signal_axes[0].size == 57

def test_joinspectra_Linescan():
    s1 = Signal1D(random((4,64)))
    s2 = Signal1D(random((4,64)))
    s2.axes_manager.signal_axes[0].offset = 47
    s = join_spectra([s1,s2],r=7,average=True)
    assert s.axes_manager.signal_axes[0].size == 111
