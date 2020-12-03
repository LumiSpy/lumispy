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

from numpy import arange
from numpy import ones
from pytest import raises
from numpy.testing import assert_allclose

from hyperspy.axes import DataAxis
from lumispy import LumiSpectrum
from lumispy import CLSEMSpectrum
from lumispy.utils.axes import *


def test_nm2eV():
    wl = arange(300,400,90)
    en = nm2eV(wl)
    assert_allclose(en[0],4.13160202)
    assert_allclose(en[-1],3.17818160)
    
def test_eV2nm():
    en = arange(1,2,0.8)
    wl = eV2nm(en)
    assert_allclose(wl[0],1239.50284)
    assert_allclose(wl[-1],688.611116)
    
def test_axes2eV():
    axis = DataAxis(axis = arange(200,400,10))
    axis2 = DataAxis(axis = arange(0.2,0.400,0.01),units='µm')
    axis3 = DataAxis(axis = arange(1,2,0.1),units='eV')
    evaxis,factor = axis2eV(axis)
    evaxis2,factor2 = axis2eV(axis2)
    raises(AttributeError,axis2eV,axis3)
    assert factor == 1e6
    assert factor2 == 1e3
    assert evaxis.name == 'Energy'
    assert evaxis.units == 'eV'
    assert not evaxis.navigate
    assert evaxis2.units == 'eV'
    assert evaxis2.size == 20
    assert_allclose(evaxis.axis[0],evaxis2.axis[0])
    assert_allclose(evaxis.axis[-1],evaxis2.axis[-1])
    assert_allclose(evaxis.axis[0],3.1781816)

def test_data2eV():
    data = 100*ones(20)
    factor = 1e6
    ax0 = arange(200,400,10)
    evaxis = nm2eV(ax0)
    evdata = data2eV(data,factor,ax0,evaxis)
    assert_allclose(evdata[-1],12.27066795)

def test_to_eV():
    axis = DataAxis(axis = arange(200,400,10))
    data = ones(20)
    S1 = LumiSpectrum(data, axes=(axis.get_axis_dictionary(), ))
    S1.to_eV()
    axis.units = 'µm'
    axis.axis = axis.axis / 1000
    data *= 1000
    S2 = CLSEMSpectrum(data, axes=(axis.get_axis_dictionary(), ))
    S3 = S2.to_eV(inplace=False)
    assert S1.axes_manager[0].units == 'eV'
    assert S3.axes_manager[0].name == 'Energy'
    assert S3.axes_manager[0].size == 20
    assert S1.axes_manager[0].axis[0] == S3.axes_manager[0].axis[0]
    assert_allclose(S1.data,S3.data,5e-4)
