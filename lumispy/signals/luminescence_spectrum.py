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

"""Signal class for Luminescence spectral data (1D).
"""

from hyperspy._signals.signal1d import Signal1D
from hyperspy._signals.lazy import LazySignal
from lumispy.signals.common_luminescence import CommonLumi


class LumiSpectrum(Signal1D, CommonLumi):
    """General 1D Luminescence signal class.
    """
    _signal_type = "Luminescence"
    _signal_dimension = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LazyLumiSpectrum(LazySignal, LumiSpectrum):
    _lazy = True

    pass
