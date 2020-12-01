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

import numpy as np
import scipy.constants as c

from hyperspy.axes import DataAxis

from inspect import getfullargspec
from scipy.interpolate import interp1d


#
# Functions needed for signal axis conversion
#

def _n_air(wl):
    """Refractive index of air as a function of WL in nm.

    This analytical function is correct for the range 185-1700 nm.

    According to `E.R. Peck and K. Reeder. Dispersion of air, 
    J. Opt. Soc. Am. 62, 958-962 (1972).`
    """
    wl = wl / 1000
    return 1 + 806051e-10 + 2480990e-8/(132274e-3 - 1/wl**2) + \
           174557e-9/(3932957e-5 - 1/wl**2)


def nm2eV(x):
    """Converts wavelength (nm) to energy (eV) using wavelength-dependent 
    permittivity of air.
    """
    return 1e9 * c.h * c.c / (c.e * _n_air(x) * x)


def eV2nm(x):
    """Converts energy (eV) to wavelength (nm) using wavelength-dependent 
    permittivity of air.
    """
    wl = 1239.5/x # approximate WL to obtain permittivity
    return 1e9 * c.h * c.c / (c.e * _n_air(wl) * x)


def axis2eV(ax0):
    """Converts given signal axis to energy scale (eV) using wavelength
    dependent permittivity of air. Assumes wavelength in units of nm unless the
    axis units are specifically set to µm.
    """
    if ax0.units == 'eV':
        raise AttributeError('Signal unit is already eV.')
    # transform axis, invert direction
    if ax0.units == 'µm':
        evaxis=nm2eV(1000*ax0.axis)[::-1]
        factor = 1e3 # correction factor for intensity
    else:
        evaxis=nm2eV(ax0.axis)[::-1]
        factor = 1e6
    axis = DataAxis(axis = evaxis, name = 'Energy', units = 'eV', 
                    navigate=False)
    return axis,factor


def data2eV(data, factor, ax0, evaxis):
    """The intensity is converted from counts/nm (counts/µm) to counts/meV by 
    doing a Jacobian transformation, see e.g. Wang and Townsend, J. Lumin. 142, 
    202 (2013). Ensures that integrated signals are still correct.
    """
    return data * factor * c.h * c.c / (c.e * _n_air(ax0[::-1])
           * evaxis**2)


def nm2invcm(x):
    r"""Converts wavelength (nm) to wavenumber (cm$^{-1}$).
    """
    return 1e7/x


def invcm2nm(x):
    r"""Converts wavenumber (cm$^{-1}$) to wavelength (nm).
    """
    return 1e7/x
    

def axis2invcm(ax0):
    r"""Converts given signal axis to wavenumber scale (cm$^{-1}$). Assumes
    wavelength in units of nm unless the axis units are specifically set to µm.
    """
    if ax0.units == r'cm$^{-1}$':
        raise AttributeError(r'Signal unit is already cm$^{-1}$.')
    # transform axis, invert direction
    if ax0.units == 'µm':
        invcmaxis=nm2invcm(1000*ax0.axis)[::-1]
        factor = 1e4 # correction factor for intensity
    else:
        invcmaxis=nm2invcm(ax0.axis)[::-1]
        factor = 1e7
    axis = DataAxis(axis = invcmaxis, name = 'Wavenumber', units = r'cm$^{-1}$', 
                    navigate=False)
    return axis,factor


def data2invcm(data, factor, ax0, invcmaxis):
    r"""The intensity is converted from counts/nm (counts/µm) to
    counts/cm$^{-1}$ by doing a Jacobian transformation, see e.g. Wang and
    Townsend, J. Lumin. 142, 202 (2013). Ensures that integrated signals are
    still correct.
    """
    return data * factor / (invcmaxis**2)

#
# spectrum manipulation
#

def join_spectra(S,r=50,scale=True,average=False,kind='slinear'):
    """ Takes list of Signal1D objects and returns a single object with all
    spectra joined. Joins spectra at the center of the overlapping range.
    Scales spectra by a factor determined as average over the range
    `center -/+ r` pixels. Works both for uniform and non-uniform axes 
    (FunctionalDataAxis is converted into a non-uniform DataAxis).
    
    Parameters
    ----------
    S : list of Signal1D objects (with overlapping signal axes)
    r : int, optional
        Number of pixels left/right of center (default `50`) defining the range
        over which to determine the scaling factor, has to be less than half
        of the overlapping pixels. Change the size of `r` or use `average=True`
        if the function induces a step in the intensity.
    scale : boolean, optional
        If `True` (default), the later spectra in the list are scaled by a
        factor determined over `center -/+ r` pixels. If `False`, spectra are
        joined without scaling, which will likely induce a step unless
        `average=True`.
    average : boolean, optional
        If `True`, the contribution of the two signals is continuously graded
        within the range defined by `r` instead of joining at the center of
        the range (default).
    kind : str, optional
        Interpolation method (default 'slinear') to use when joining signals
        with a uniform signal axes. See `scipy.interpolate.interp1d` for
        options.
    
    Returns
    -------
    A new Signal1D object containing the joined spectra (properties are copied
    from first spectrum).
    
    Examples
    --------
    
    >>> s1 = hs.signals.Signal1D(np.ones(32))
    >>> s2 = hs.signals.Signal1D(np.ones(32)*2)
    >>> s2.axes_manager.signal_axes[0].offset = 25
    >>> lum.join_spectra([s1,s2],r=2)
    <Signal1D, title: , dimensions: (|57)>
    """
    
    import numpy as np
    import os
    
    # Test that spectra overlap
    for i in range(1,len(S)):
        if S[i-1].axes_manager.signal_axes[0].axis.max() \
           < S[i].axes_manager.signal_axes[0].axis.min():
            raise ValueError("Signal axes not overlapping")
    
    # take first spectrum as basis
    S1 = S[0].deepcopy()
    axis = S1.axes_manager.signal_axes[0]
    for i in range(1,len(S)): # join following spectra
        S2 = S[i].deepcopy()
        axis2 = S2.axes_manager.signal_axes[0]
        omax = axis.axis.max() # define overlap range
        omin = axis2.axis.min()
        ocenter = (omax+omin)/2 # center of overlap range
        # closest index to center of overlap first spectrum
        ind1 = axis.value2index(ocenter)
        # closest index to center of overlap second spectrum
        ind2 = axis2.value2index(ocenter)
        # Test that r is not too large
        if (axis.size - ind1 - 1) <= r:
            raise ValueError("`r` is too large")
        # calculate mean deviation over defined range ignoring nan/zero values
        init = np.empty(S2.isig[ind2-r:ind2+r].data.shape)
        init[:] = np.nan
        # Do scaling of following signals
        if scale:
            if (axis.axis[ind1-r:ind1+r] == axis2.axis[ind2-r:ind2+r]).all():
                factor = np.nanmean(np.ma.masked_invalid(np.divide(S1.isig[ind1-r:ind1+r].data,
                         S2.isig[ind2-r:ind2+r].data, out = init,
                         where = S2.isig[ind2-r:ind2+r].data != 0)), axis = -1)
            else: # interpolate to get factor at same positions
                ind2r1 = axis2.value2index(axis.axis[ind1-r])
                ind2r2 = axis2.value2index(axis.axis[ind1+r])
                f = interp1d(axis2.axis[ind2r1-1:ind2r2+1],
                         S2.isig[ind2r1-1:ind2r2+1].data,kind=kind)
                factor = np.nanmean(np.ma.masked_invalid(np.divide(S1.isig[ind1-r:ind1+r].data,
                         f(axis.axis[ind1-r:ind1+r]), out = init,
                         where = S2.isig[ind2-r:ind2+r].data != 0)), axis = -1)
            if (factor < 0).any():
                raise ValueError("One of the signals has a negative mean"\
                                 " value in the overlapping range. Try to set"\
                                 " `scale=False` and `average=True`.")
            S2.data = (S2.data.T * factor).T # scale 2nd spectrum by factor
        # Make sure the corresponding values are in correct order
        if axis.axis[ind1] >= axis2.axis[ind2]:
            ind2 += 1        
        # for UniformDataAxis
        if (not 'axis' in getfullargspec(DataAxis)[0]) or (axis.is_uniform \
           and axis2.is_uniform):
            # join axis vectors  
            axis.size = axis.axis[:ind1+1].size + np.floor((axis2.axis[-1]
                        - axis.axis[ind1])/axis.scale)
            # join data vectors interpolating to a common uniform axis
            if average: # average over range
                ind2r = axis2.value2index(axis.axis[ind1-r])
                length = axis.axis[ind1-r:ind1+r].size
                grad = 1/(length-1)
                vect = np.arange(length)
                f = interp1d(axis2.axis[ind2r-1:],
                          S2.isig[ind2r-1:].data,kind=kind)
                S1.data = np.hstack((S1.isig[:ind1-r].data,
                          (1-grad*vect)*S1.isig[ind1-r:ind1+r].data +
                          grad*vect*f(axis.axis[ind1-r:ind1+r]),
                          f(axis.axis[ind1+r:])))
            else: # just join at center of overlap
                f = interp1d(axis2.axis[ind2:], 
                          S2.isig[ind2:].data,kind=kind)
                S1.data = np.hstack((S1.isig[:ind1+1].data,
                          f(axis.axis[ind1+1:])))
        else: # for DataAxis/FunctionalDataAxis (non uniform)
            # convert FunctionalDataAxes or UniformDataAxis to DataAxes
            if hasattr(axis,'expression') or axis.is_uniform:
                axis.convert_to_non_uniform_axis()
            if hasattr(axis2,'expression'):
                axis2.convert_to_non_uniform_axis()
            # join axis vectors
            axis.axis = np.hstack((axis.axis[:ind1+1],axis2.axis[ind2:]))
            axis.size = axis.axis.size
            if average: # average over range
                f1 = interp1d(S[i-1].axes_manager.signal_axes[0].axis[ind1-1:ind1+r+1],
                          S1.isig[ind1-1:ind1+r+1].data,kind=kind)
                f2 = interp1d(axis2.axis[ind2-r-1:ind2+1],
                          S2.isig[ind2-r-1:ind2+1].data,kind=kind)
                length1 = axis.axis[ind1-r:ind1+1].size
                grad1 = 0.5/(length1-1)
                vect1 = np.arange(length1)
                length2 = axis2.axis[ind2:ind2+r].size
                grad2 = 0.5+0.5/(length2-1)
                vect2 = np.arange(length2)
                S1.data = np.hstack((S1.isig[:ind1-r].data,
                          (1-grad1*vect1)*S1.isig[ind1-r:ind1+1].data +
                          grad1*vect1*f2(axis.axis[ind1-r:ind1+1]),
                          (1-grad2*vect2)*f1(axis2.axis[ind2:ind2+r]) +
                          grad2*vect2*S2.isig[ind2:ind2+r].data,
                          S2.isig[ind2+r:].data))
            else: # just join at center of overlap
                S1.data = np.hstack((S1.isig[:ind1+1].data,
                          S2.isig[ind2:].data))
    return S1
