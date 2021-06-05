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

SAVETXT_DOCSTRING = """
    Writes single spectra to a two-column data file with signal axis as
        X and data as Y.
    Writes linescan data to file with signal axis as first row and
        navigation axis as first column (flipped if `transpose=True`)."""

SAVETXT_PARAMETERS = """
    Parameters
    ----------
    filename : string
    fmt : str or sequence of strs, optional
        A single or sequence of format strings. Default is '%.5f'.
    delimiter : str, optional
        String or character separating columns. Default is ','
    axes : bool, optional
        If True (default), include axes in saved file. If False, save the data
        array only.
    transpose : bool, optional
        If True, transpose data array and exchange axes. Default is false.
        Ignored for single spectra.
    **kwargs 
        Takes any additional arguments of numpy.loadtxt, e.g. `newline`
        `header`, `footer`, `comments`, or `encoding`.

    See also
    --------
    numpy.savetxt"""

SAVETXT_EXAMPLE = """
    Examples
    --------
    >>> import lumispy as lum
    >>> import numpy as np
    
    # Spectrum:
    >>> S = lum.signals.LumiSpectrum(np.arange(5))
    >>> lum.savetxt(S, 'spectrum.txt')
    # 0.00000	0.00000
    # 1.00000	1.00000
    # 2.00000	2.00000
    # 3.00000	3.00000
    # 4.00000	4.00000
    
    # Linescan:
    >>> L = lum.signals.LumiSpectrum(np.arange(25).reshape((5,5)))
    >>> lum.savetxt(L, 'linescan.txt')
    # 0.00000	0.00000	1.00000	2.00000	3.00000	4.00000
    # 0.00000	0.00000	5.00000	10.00000	15.00000	20.00000
    # 1.00000	1.00000	6.00000	11.00000	16.00000	21.00000
    # 2.00000	2.00000	7.00000	12.00000	17.00000	22.00000
    # 3.00000	3.00000	8.00000	13.00000	18.00000	23.00000
    # 4.00000	4.00000	9.00000	14.00000	19.00000	24.00000
    """

TOARRAY_DOCSTRING = """
    
    Returns single spectra as two-column array.
    Returns linescan data as array with signal axis as first row and
        navigation axis as first column (flipped if `transpose=True`)."""

TOARRAY_PARAMETERS = """
    Parameters
    ----------
    axes : bool, optional
        If True (default), include axes in array. If False, return the data
        array only.
    transpose : bool, optional
        If True, transpose data array and exchange axes. Default is false.
        Ignored for single spectra.
    **kwargs 
        Takes any additional arguments of numpy.loadtxt, e.g. `newline`
        `header`, `footer`, `comments`, or `encoding`."""

TOARRAY_EXAMPLE = """
    Note
    --------
    The output of this function can be used to convert a signal object to a
    pandas dataframe, e.g. using `df = pd.Dataframe(lum.to_array(S))`.
    
    Examples
    --------
    >>> import lumispy as lum
    >>> import numpy as np
    
    # Spectrum:
    >>> S = lum.signals.LumiSpectrum(np.arange(5))
    >>> lum.to_array(S)
    # array([[0., 0.],
    #    [1., 1.],
    #    [2., 2.],
    #    [3., 3.],
    #    [4., 4.]])
    
    # Linescan:
    >>> L = lum.signals.LumiSpectrum(np.arange(25).reshape((5,5)))
    >>> lum.to_array(L)
    # array([[ 0.,  0.,  1.,  2.,  3.,  4.],
    #    [ 0.,  0.,  1.,  2.,  3.,  4.],
    #    [ 1.,  5.,  6.,  7.,  8.,  9.],
    #    [ 2., 10., 11., 12., 13., 14.],
    #    [ 3., 15., 16., 17., 18., 19.],
    #    [ 4., 20., 21., 22., 23., 24.]])
    """


def to_array(S, axes=True, transpose=False):
    """Returns signal object as numpy array (optionally including the axes).
    %s
    Returns image as array with the navigation axes as first column and first
        row.
    Returns 2D data (e.g. map of a fit parameter value) as array with the signal
        axes as first column and first row.
    %s
    %s
    """
    nav_axes = S.axes_manager.navigation_axes
    sig_axes = S.axes_manager.signal_axes
    dim = len(nav_axes) + len(sig_axes)
    # Convert single spectrum or data with only navigation axis
    if dim == 1:
        if axes:
            if len(sig_axes) == 1:
                x = sig_axes[0].axis
            else:
                x = nav_axes[0].axis
            output = np.array([x, S.data]).T
        else:
            output = S.data
    # Convert linescan or matrix
    elif dim == 2:
        if axes:
            if len(sig_axes) == 1:
                x = np.concatenate(([0], sig_axes[0].axis))
                y = nav_axes[0].axis
            elif len(nav_axes) == 0:
                x = np.concatenate(([0], sig_axes[0].axis))
                y = sig_axes[1].axis
            else:
                x = np.concatenate(([0], nav_axes[0].axis))
                y = nav_axes[1].axis
            if transpose:
                output = np.hstack(
                    (x.reshape(x.size, 1), np.vstack((y, np.transpose(S.data))))
                )
            else:
                output = np.vstack((x, np.hstack((y.reshape(y.size, 1), S.data))))
        else:
            if transpose:
                output = np.transpose(S.data)
            else:
                output = S.data
    else:
        raise NotImplementedError(
            "The to_array function currently handles a " "maximum of two axes."
        )
    return output


to_array.__doc__ %= (TOARRAY_DOCSTRING, TOARRAY_PARAMETERS, TOARRAY_EXAMPLE)


def savetxt(
    S, filename, fmt="%.5f", delimiter="\t", axes=True, transpose=False, **kwargs
):
    """Writes signal object to simple text file.
    %s
    Writes image to file with the navigation axes as first column and first
        row.
    Writes 2D data (e.g. map of a fit parameter value) to file with the signal
        axes as first column and first row.
    %s
    %s
    """
    dim = len(S.axes_manager.signal_axes) + len(S.axes_manager.navigation_axes)
    if dim <= 2:
        output = to_array(S, axes, transpose)
        np.savetxt(filename, output, fmt=fmt, delimiter=delimiter, **kwargs)
    else:
        raise NotImplementedError(
            "The savetxt function currently handles a " "maximum of two axes."
        )


savetxt.__doc__ %= (SAVETXT_DOCSTRING, SAVETXT_PARAMETERS, SAVETXT_EXAMPLE)
