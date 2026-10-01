# -*- coding: utf-8 -*-
# Copyright 2019-2026 The LumiSpy developers
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

from importlib.resources import as_file, files

import hyperspy.api as hs

_PACKAGE = "lumispy.data"
_DIRECTORY = "optical_constants"
_FILE_SUFFIX = ".hspy"


def _optical_constants():
    """Return all packaged optical-constants by name."""
    directory = files(_PACKAGE).joinpath(_DIRECTORY)

    return {
        op_const.name.removesuffix(_FILE_SUFFIX): op_const
        for op_const in directory.iterdir()
        if op_const.is_file() and op_const.name.endswith(_FILE_SUFFIX)
    }


def supported_optical_constants():
    """Return the names of all bundled optical constants."""
    return tuple(sorted(_optical_constants()))


def load_optical_constants(name):
    """Load bundled optical constants as a HyperSpy signal."""
    name = name.removesuffix(_FILE_SUFFIX)
    op_const = _optical_constants()

    try:
        op_const = op_const[name]
    except KeyError:
        supported = ", ".join(repr(item) for item in sorted(op_const))
        raise ValueError(
            f"Unknown optical constants {name!r}. "
            f"Available optical constants are: {supported}"
        )

    with as_file(op_const) as path:
        return hs.load(path, lazy=False)
