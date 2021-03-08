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

import numpy as np


def savetxt(S, filename, fmt='%.5f', delimiter='\t', **kwargs):
    """Write data to text file. 
    
    Writes single spectra to a two-column data file with signal axis as
        X and data as Y.
    Writes linescan data to file with signal axis as first column and
        navigation axis as first row.
    Writes ...
    
    Parameters
    ----------
    filename : string
    fmt : str or sequence of strs, optional
        A single or sequence of format strings. Default is '%.5f'.
    delimiter : str, optional
        String or character separating columns. Default is ','
    **kwargs 
        Takes any additional arguments of numpy.loadtxt, e.g. `newline`
        `header`, `footer`, `comments`, or `encoding`.
    """
    nav_axes = S.axes_manager.navigation_axes
    sig_axes = S.axes_manager.signal_axes
    dim = len(nav_axes) + len(sig_axes)
    # Write single spectrum or data with only navigation axis
    if dim == 1:
        if len(sig_axes) == 1:
            X = sig_axes[0].axis
        else:
            X = nav_axes[0].axis
        Y = S.data
        np.savetxt(filename, np.array([X,Y]).T, fmt=fmt,
                   delimiter=delimiter, **kwargs)
    # Write linescan or matrix
    elif dim == 2:
        if len(sig_axes) == 1:
            X = np.concatenate(([0],sig_axes[0].axis))
            X.shape = (X.size,1)
            Y = nav_axes[0].axis
        elif len(nav_axes) == 0: # TODO: check if axis order is correct
            X = np.concatenate(([0],sig_axes[0].axis))
            X.shape = (X.size,1)
            Y = sig_axes[1].axis
        else: # TODO: check if axis order is correct
            X = np.concatenate(([0],nav_axes[0].axis))
            X.shape = (X.size,1)
            Y = nav_axes[1].axis
        Z = np.hstack((X, np.vstack((Y, np.transpose(S.data)))))
        np.savetxt(filename, Z, fmt=fmt, delimiter=delimiter, **kwargs)
    # TODO make axes optional
    else:
        raise NotImplementedError("The savetxt function currently handles a "
                                   "maximum of two axes.")
