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

"""
Signal class for electroluminescence spectral data
--------------------------------------------------
"""

from hyperspy._signals.lazy import LazySignal

from lumispy.signals import LumiSpectrum


class ELSpectrum(LumiSpectrum):
    """**General 1D electroluminescence signal class**"""

    _signal_type = "EL"
    _signal_dimension = 1

    pass


class LazyELSpectrum(LazySignal, ELSpectrum):
    """**General lazy 1D electroluminescence signal class**"""

    _lazy = True

    pass
