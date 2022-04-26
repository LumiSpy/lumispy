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

from .luminescence_spectrum import LumiSpectrum, LazyLumiSpectrum
from .cl_spectrum import CLSpectrum, LazyCLSpectrum
from .cl_spectrum import CLSEMSpectrum, LazyCLSEMSpectrum
from .cl_spectrum import CLSTEMSpectrum, LazyCLSTEMSpectrum
from .pl_spectrum import PLSpectrum, LazyPLSpectrum
from .el_spectrum import ELSpectrum, LazyELSpectrum
from .luminescence_transient import LumiTransient, LazyLumiTransient
from .luminescence_transientspec import LumiTransientSpectrum, LazyLumiTransientSpectrum


__all__ = [
    "LumiSpectrum",
    "LazyLumiSpectrum",
    "CLSpectrum",
    "LazyCLSpectrum",
    "CLSEMSpectrum",
    "LazyCLSEMSpectrum",
    "CLSTEMSpectrum",
    "LazyCLSTEMSpectrum",
    "PLSpectrum",
    "LazyPLSpectrum",
    "ELSpectrum",
    "LazyELSpectrum",
    "LumiTransient",
    "LazyLumiTransient",
    "LumiTransientSpectrum",
    "LazyLumiTransientSpectrum",
]
