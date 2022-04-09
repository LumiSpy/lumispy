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
Signal class for luminescence transient data (2D)
-------------------------------------------------
"""

from hyperspy.signals import Signal2D
from hyperspy._signals.lazy import LazySignal

from lumispy.signals.common_luminescence import CommonLumi
from lumispy.signals.common_transient import CommonTransient


class LumiTransientSpectrum(Signal2D, CommonLumi, CommonTransient):
    """**General 2D luminescence signal class (transient/time resolved)**"""

    _signal_type = "TransientSpec"
    _signal_dimension = 2

    pass


class LazyLumiTransientSpectrum(LazySignal, LumiTransientSpectrum):
    """**General lazy 2D luminescence signal class (transient/time resolved)**"""

    _lazy = True

    pass
