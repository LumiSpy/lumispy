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

SAVETXT_DOCSTRING = \
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

    See also
    --------
    numpy.savetxt
    
    """

SAVETXT_DOCSTRING_EXAMPLE = \
    """Examples
    --------
    >>> import lumispy as lum
    >>> import numpy as np
    
    # Spectrum:
    >>> s = lum.signals.LumiSpectrum(np.arange(5))
    >>> lum.savetxt(s, 'spectrum.txt')
    # 0.00000	0.00000
    # 1.00000	1.00000
    # 2.00000	2.00000
    # 3.00000	3.00000
    # 4.00000	4.00000
    
    # Linescan:
    >>> l = lum.signals.LumiSpectrum(np.arange(25).reshape((5,5)))
    >>> lum.savetxt(l, 'linescan.txt')
    # 0.00000	0.00000	1.00000	2.00000	3.00000	4.00000
    # 0.00000	0.00000	5.00000	10.00000	15.00000	20.00000
    # 1.00000	1.00000	6.00000	11.00000	16.00000	21.00000
    # 2.00000	2.00000	7.00000	12.00000	17.00000	22.00000
    # 3.00000	3.00000	8.00000	13.00000	18.00000	23.00000
    # 4.00000	4.00000	9.00000	14.00000	19.00000	24.00000
    """


def savetxt(S, filename, fmt='%.5f', delimiter='\t', **kwargs):
    """%s
    %s
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

savetxt.__doc__ %= (SAVETXT_DOCSTRING, SAVETXT_DOCSTRING_EXAMPLE)
