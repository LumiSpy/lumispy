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


from . import (
    components,
    signals,
    utils,
)
from ._version import __version__
from .utils.axes import nm2eV, eV2nm, nm2invcm, invcm2nm, join_spectra
from .utils.io import to_array, savetxt
from .utils import crop_edges

__all__ = [
    "__version__",
    "components",
    "signals",
    "utils",
    "nm2eV",
    "eV2nm",
    "nm2invcm",
    "invcm2nm",
    "join_spectra",
    "to_array",
    "savetxt",
    "crop_edges",
]
