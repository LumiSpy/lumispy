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

"""Signal class for Luminescence transient data (2D).
"""

from hyperspy.signals import Signal2D
from hyperspy._signals.lazy import LazySignal

from lumispy.signals.luminescence_transient import LumiTransient


class CLTransient(LumiTransient):
    """CL 2D luminescence signal class (transient/time resolved)."""

    _signal_type = "TRCL"
    _signal_dimension = 2

    pass


class LazyCLTransient(LazySignal, CLTransient):
    _lazy = True

    pass
