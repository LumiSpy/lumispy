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
from hyperspy.signals import Signal1D

from inspect import getfullargspec


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
    """Converts wavelength to energy using wavelength-dependent permittivity of 
    air.
    """

    return 1e9 * c.h * c.c / (c.e * _n_air(x) * x)


def eV2nm(x):
    """Converts energy to wavelength using wavelength-dependent permittivity of 
    air.
    """

    wl = 1239.5/x # approximate WL to obtain permittivity
    return 1e9 * c.h * c.c / (c.e * _n_air(wl) * x)

def to_eV(s):
    """Creates new signal object with signal axis converted to eV (using 
    wavelength dependent permittivity of air). Assumes WL in units of nm 
    unless the axis units are specifically set to µm.
    
    The intensity is converted from counts/nm (counts/µm) to counts/meV by 
    doing a Jacobian transformation, see e.g. Wang and Townsend, J. Lumin. 142, 
    202 (2013).

    
    Input parameters
    ----------------
    s : signal object
    
    Returns
    -------
    New signal object with energy axis as new signal axis, but same navigation 
    axis and data.
    
    Note
    ----
    Setting non linear scale instead of offset and scale work only for 
    the non_uniform_axis branch of hyperspy.

    """

    # Check if non_uniform_axis is available in hyperspy version
    if not 'axis' in getfullargspec(DataAxis)[0]:
        raise NotImplementedError('Conversion to energy axis works only if '
                            'the non_uniform_axis branch of hyperspy is used.')
        
    ax0 = s.axes_manager.signal_axes[0]
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
    # invert direction for data and do Jacobian transformation so that 
    # integrated signals are correct
    s2data = s.isig[::-1].data * factor * c.h * c.c / (c.e * 
             _n_air(ax0.axis[::-1]) * evaxis**2)
    if s.data.ndim == 1:
        s2 = Signal1D(s2data, axes=(axis.get_axis_dictionary(),))
    elif s.data.ndim == 2:
        s2 = Signal1D(s2data, axes=
             (s.axes_manager.navigation_axes[0].get_axis_dictionary(),
             axis.get_axis_dictionary(), ))
    else:
        s2 = Signal1D(s2data, axes=
             (s.axes_manager.navigation_axes[1].get_axis_dictionary(),
             s.axes_manager.navigation_axes[0].get_axis_dictionary(),
             axis.get_axis_dictionary(), ))
    return s2
