# -*- coding: utf-8 -*-
# Copyright 2019-2023 The LumiSpy developers
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

from hyperspy.signals import Signal1D, Signal2D
from hyperspy._signals.lazy import LazySignal

from lumispy.signals import LumiSpectrum, LumiTransient
from lumispy.signals.common_luminescence import CommonLumi
from lumispy.signals.common_transient import CommonTransient


class TransientSpectrumCasting(Signal1D, CommonLumi, CommonTransient):
    """**1D signal class for casting reduced LumiTransientSpectrum to either Luminescence or Transient**"""

    _signal_type = "TransientSpec"
    _signal_dimension = 1

    def __init__(self, *args, **kwargs):
        if hasattr(self, "axes_manager") and self.axes_manager[-1].units in [
            "fs",
            "ps",
            "ns",
            "µs",
            "mus",
            "ms",
            "s",
        ]:
            self.metadata.Signal.signal_type = "Transient"
            self.__class__ = LumiTransient
            self.__init__(*args, **kwargs)
        else:
            self.metadata.Signal.signal_type = "Luminescence"
            self.__class__ = LumiSpectrum
            self.__init__(*args, **kwargs)


class LumiTransientSpectrum(Signal2D, CommonLumi, CommonTransient):
    """**2D luminescence signal class (spectrum+transient/time resolved dimensions)**"""

    _signal_type = "TransientSpec"
    _signal_dimension = 2


class LazyLumiTransientSpectrum(LazySignal, LumiTransientSpectrum):
    """**Lazy 2D luminescence signal class (spectral+transient/time resolved dimensions)**"""

    _lazy = True
