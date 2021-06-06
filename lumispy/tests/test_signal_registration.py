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

import pytest
from numpy import arange

from hyperspy.signals import Signal1D, Signal2D

from lumispy.signals import (
    LumiSpectrum,
    CLSpectrum,
    CLSEMSpectrum,
    CLSTEMSpectrum,
    PLSpectrum,
    ELSpectrum,
    LumiTransient,
    CLTransient,
    PLTransient,
    LazyLumiSpectrum,
    LazyCLSpectrum,
    LazyCLSEMSpectrum,
    LazyCLSTEMSpectrum,
    LazyPLSpectrum,
    LazyELSpectrum,
    LazyLumiTransient,
    LazyCLTransient,
    LazyPLTransient,
)

signal1d_class_list = [
    LumiSpectrum,
    CLSpectrum,
    CLSEMSpectrum,
    CLSTEMSpectrum,
    PLSpectrum,
    ELSpectrum,
    LazyLumiSpectrum,
    LazyCLSpectrum,
    LazyCLSEMSpectrum,
    LazyCLSTEMSpectrum,
    LazyPLSpectrum,
    LazyELSpectrum,
]
signal2d_class_list = [
    LumiTransient,
    CLTransient,
    PLTransient,
    LazyLumiTransient,
    LazyCLTransient,
    LazyPLTransient,
]


@pytest.mark.parametrize("signal_class", signal1d_class_list)
def test_signal_registration1d(signal_class):
    s = signal_class(0)

    s2 = Signal1D([0, 1, 2])
    if s._lazy:
        s2 = s2.as_lazy()

    print("signal_type:", s._signal_type)

    s2.set_signal_type(s._signal_type)
    assert isinstance(s2, signal_class)


@pytest.mark.parametrize("signal_class", signal2d_class_list)
def test_signal_registration2d(signal_class):
    data = arange(1000).reshape((10, 10, 10))
    s = signal_class(data)

    s2 = Signal2D(data)
    if s._lazy:
        s2 = s2.as_lazy()

    print("signal_type:", s._signal_type)

    s2.set_signal_type(s._signal_type)
    assert isinstance(s2, signal_class)
