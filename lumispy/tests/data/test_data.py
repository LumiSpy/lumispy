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

import lumispy as lum
from lumispy.data import asymmetric_peak_map, nanoparticles


def test_asymmetric_peak_map():
    s = asymmetric_peak_map()
    assert isinstance(s, lum.signals.CLSpectrum)
    assert s.axes_manager.navigation_dimension == 2
    assert s._signal_type == "CL"


def test_nanoparticles():
    s = nanoparticles()
    assert isinstance(s, lum.signals.CLSEMSpectrum)
    assert s.axes_manager.navigation_dimension == 2
    assert s._signal_type == "CL_SEM"
