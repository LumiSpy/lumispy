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

"""
Lazy signal classes for cathodoluminescence spectral data
---------------------------------------------------------
"""

from hyperspy.docstrings.signal import LAZYSIGNAL_DOC
from hyperspy.signals import LazySignal1D

from lumispy.signals import CLSpectrum, CLSEMSpectrum, CLSTEMSpectrum


class LazyCLSpectrum(LazySignal1D, CLSpectrum):
    """**General lazy 1D cathodoluminescence signal class.**"""

    __doc__ += LAZYSIGNAL_DOC.replace("__BASECLASS__", "CLSpectrum")


class LazyCLSEMSpectrum(LazySignal1D, CLSEMSpectrum):
    """**Lazy 1D scanning electron microscopy cathodoluminescence signal class.**"""

    __doc__ += LAZYSIGNAL_DOC.replace("__BASECLASS__", "CLSEMSpectrum")


class LazyCLSTEMSpectrum(LazySignal1D, CLSTEMSpectrum):
    """**Lazy 1D scanning transmission electron microscopy cathodoluminescence signal class.**"""

    __doc__ += LAZYSIGNAL_DOC.replace("__BASECLASS__", "CLSTEMSpectrum")

