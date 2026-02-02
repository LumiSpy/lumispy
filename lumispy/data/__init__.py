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

# from .__init__ import asymmetric_peak_map, nanoparticles

from pathlib import Path
import warnings

import hyperspy.api as hs

__all__ = [
    "asymmetric_peak_map",
    "nanoparticles",
]


def __dir__():
    return sorted(__all__)


def _resolve_dir():
    """Returns the absolute path to this file's directory."""
    return Path(__file__).resolve().parent


def asymmetric_peak_map():
    """Load example asymmetric peak map data.

    Returns
    -------
    :py:class:`~hyperspy._signals.signal.Signal1D`
    """
    file_path = _resolve_dir().joinpath("asymmetric_peak_map.hspy")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        return hs.load(file_path, mode="r", reader="hspy")


def nanoparticles():
    """Load example nanoparticle spectrum data.

    Returns
    -------
    :py:class:`~hyperspy._signals.signal.Signal1D`
    """
    file_path = _resolve_dir().joinpath("nanoparticles.hspy")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        return hs.load(file_path, mode="r", reader="hspy")
