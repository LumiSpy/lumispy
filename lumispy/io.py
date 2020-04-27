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

import os
import hyperspy.io
# To keep the unmodified version of `load_single_files` from hyperspy before modification
from hyperspy.io import load_single_file as hyperspy_load_single_file
from lumispy.io_plugins import io_plugins


def load_single_file(filename, **kwds):
    """
    Modified version of `load_single_file()` of Hyperspy.
    It also supports HYPScan.bin files (from Attolight).

    Parameters
    ----------

    filename : string
        File name (including the extension)

    """
    extension = os.path.splitext(filename)[1][1:]

    for i in range(len(io_plugins)):
        if extension.lower() in io_plugins[i].file_extensions:
            reader = io_plugins[i]
            # Maybe this needs to be changed...
            lumispy_object = reader.file_reader(filename, **kwds)
            return lumispy_object

    # Load with the Hyperspy function
    return hyperspy_load_single_file(filename, **kwds)


# Monkey patch function (updating it from hyperspy's default function)
hyperspy.io.load_single_file = load_single_file

load = hyperspy.io.load
