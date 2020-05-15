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

#
# This file contains function needed for signal axis conversion
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
    """Converts given signal axis to eV using wavelength dependent permittivity 
    of air. Assumes WL in units of nm 
    unless the axis units are specifically set to µm.
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
    202 (2013). Ensures that integrates signals are still correct.
    """
    return data * factor * c.h * c.c / (c.e * _n_air(ax0[::-1])
           * evaxis**2)
