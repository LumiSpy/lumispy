# -*- coding: utf-8 -*-
# Copyright 2019-2023 The LumiSpy developers
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

import numpy as np
import scipy.constants as c
from copy import deepcopy
from warnings import warn
from hyperspy.axes import DataAxis, UniformDataAxis


#
# Functions needed for signal axis conversion
#


def _n_air(x):
    """Refractive index of air as a function of WL in nm.
    This analytical function is correct for the range 185-1700 nm.
    According to `E.R. Peck and K. Reeder. Dispersion of air,
    J. Opt. Soc. Am. 62, 958-962 (1972).`
    """
    wl = deepcopy(x)
    # Check for supported range
    if (np.min(wl) < 185) or (np.max(wl) > 1700):
        if np.size(wl) == 1:
            if wl < 185:
                wl = 185
            if wl > 1700:
                wl = 1700
        else:
            wl[wl < 185] = 185
            wl[wl > 1700] = 1700
        warn(
            "The wavelength range exceeds the interval of 185 to 1700 nm for "
            "which the exact refractive index of air is used. Beyond this "
            "range, the refractive index is kept constant.",
            UserWarning,
        )
    wl = wl / 1000
    return (
        1
        + 806051e-10
        + 2480990e-8 / (132274e-3 - 1 / wl**2)
        + 174557e-9 / (3932957e-5 - 1 / wl**2)
    )


def nm2eV(x):
    """Converts wavelength (nm) to energy (eV) using wavelength-dependent
    refractive index of air.
    """
    return 1e9 * c.h * c.c / (c.e * _n_air(x) * x)


def eV2nm(x):
    """Converts energy (eV) to wavelength (nm) using wavelength-dependent
    refractive index of air.
    """
    wl = 1239.5 / x  # approximate WL to obtain refractive index
    return 1e9 * c.h * c.c / (c.e * _n_air(wl) * x)


def axis2eV(ax0):
    """Converts given signal axis to energy scale (eV) using wavelength
    dependent refractive index of air. Assumes wavelength in units of nm unless the
    axis units are specifically set to µm.
    """
    if ax0.units == "eV":
        raise AttributeError("Signal unit is already eV.")
    # transform axis, invert direction
    if ax0.units == "µm":
        evaxis = nm2eV(1000 * ax0.axis)[::-1].astype("float")
        factor = 1e3  # correction factor for intensity
    else:
        evaxis = nm2eV(ax0.axis)[::-1].astype("float")
        factor = 1e6
    axis = DataAxis(axis=evaxis, name="Energy", units="eV", navigate=False)
    return axis, factor


def data2eV(data, factor, evaxis, ax0):
    """The intensity is converted from counts/nm (counts/µm) to counts/meV by
    doing a Jacobian transformation, see e.g. Mooney and Kambhampati, J. Phys.
    Chem. Lett. 4, 3316 (2013). Ensures that integrated signals are still
    correct.
    """
    if ax0.units == "µm":
        return (
            data
            * factor
            * c.h
            * c.c
            / (c.e * _n_air(1000 * ax0.axis)[::-1] * evaxis**2)
        )
    else:
        return data * factor * c.h * c.c / (c.e * _n_air(ax0.axis[::-1]) * evaxis**2)


def var2eV(variance, factor, evaxis, ax0):
    """The variance is converted doing a squared Jacobian renormalization to
    match with the transformation of the data.
    """
    if ax0.units == "µm":
        return (
            variance
            * (factor * c.h * c.c / (c.e * _n_air(1000 * ax0.axis)[::-1] * evaxis**2))
            ** 2
        )
    else:
        return (
            variance
            * (factor * c.h * c.c / (c.e * _n_air(ax0.axis[::-1]) * evaxis**2)) ** 2
        )


def nm2invcm(x):
    r"""Converts wavelength (nm) to wavenumber (cm$^{-1}$)."""
    return 1e7 / x


def invcm2nm(x):
    r"""Converts wavenumber (cm$^{-1}$) to wavelength (nm)."""
    return 1e7 / x


def axis2invcm(ax0):
    r"""Converts given signal axis to wavenumber scale (cm$^{-1}$). Assumes
    wavelength in units of nm unless the axis units are specifically set to µm.
    """
    if ax0.units == r"cm$^{-1}$":
        raise AttributeError(r"Signal unit is already cm$^{-1}$.")
    # transform axis, invert direction
    if ax0.units == "µm":
        invcmaxis = nm2invcm(1000 * ax0.axis)[::-1].astype("float")
        factor = 1e4  # correction factor for intensity
    else:
        invcmaxis = nm2invcm(ax0.axis)[::-1].astype("float")
        factor = 1e7
    axis = DataAxis(
        axis=invcmaxis,
        name="Wavenumber",
        units=r"cm$^{-1}$",
        navigate=False,
    )
    return axis, factor


def data2invcm(data, factor, invcmaxis, ax0=None):
    r"""The intensity is converted from counts/nm (counts/µm) to
    counts/cm$^{-1}$ by doing a Jacobian transformation, see e.g. Mooney and
    Kambhampati, J. Phys. Chem. Lett. 4, 3316 (2013). Ensures that integrated
    signals are still correct.
    """
    return data * factor / (invcmaxis**2)


def var2invcm(variance, factor, invcmaxis, ax0=None):
    r"""The variance is converted doing a squared Jacobian renormalization to
    match with the transformation of the data.
    """
    return variance * (factor / (invcmaxis**2)) ** 2


GRATING_EQUATION_DOCSTRING_PARAMETERS = r"""
    gamma_deg: float
        Inclination angle between the focal plane and the centre of the grating
        (found experimentally from calibration). In degree.
    deviation_angle_deg: float
        Also known as included angle. It is defined as the difference between
        angle of diffraction (:math:`\beta`) and angle of incidence
        (:math:`\alpha`). Given by manufacturer specsheet. In degree.
    focal_length_mm: float
        Given by manufacturer specsheet. In mm.
    ccd_width_mm: float
        The width of the CDD. Given by manufacturer specsheet. In mm.
    grating_central_wavelength_nm: float
        Wavelength at the centre of the grating, where exit slit is placed. In nm.
    grating_density_gr_mm: int
        Grating density in gratings per mm."""


def solve_grating_equation(
    axis,
    gamma_deg,
    deviation_angle_deg,
    focal_length_mm,
    ccd_width_mm,
    grating_central_wavelength_nm,
    grating_density_gr_mm,
):
    r"""Solves the grating equation.
    See `horiba.com/uk/scientific/products/optics-tutorial/wavelength-pixel-position`
    for equations.

    Parameters
    ----------
    axis: hyperspy.axis
        Axis in pixel units (no units) to convert to wavelength.
    %s

    Returns
    -------
    axis: hyperspy.axis
        HyperSpy axis object.
    """

    # From axis --> x-array
    s = str(axis.units).lower()
    non_defined = s in "<undefined>"
    pixel_units = s in ["pixel", "px"]

    if not non_defined and not pixel_units:
        warn(
            "The signal axes are already in {} units (not in pixel units)."
            "The conversion will run anyways.".format(str(axis.units)),
            SyntaxWarning,
        )

    # Set up variables
    # ch: channels,
    ch = len(axis.axis)

    # Calculate geometry
    # l_h: Perpendicular distance from the spectral plane to grating (Eq. 5.3)
    l_h = focal_length_mm * np.cos(np.deg2rad(gamma_deg))
    # h_blc: Distance from the intercept of the normal to the focal plane to the wavelength lambda_c (Eq. 5.5)
    h_blc = focal_length_mm * np.sin(np.deg2rad(gamma_deg))

    # alpha = angle of incidence (Eq. 2.1)
    numerator = 1e-6 * grating_density_gr_mm * grating_central_wavelength_nm
    denominator = 2 * np.cos(np.deg2rad(deviation_angle_deg / 2))
    alpha = np.arcsin(np.deg2rad(numerator / denominator)) - deviation_angle_deg / 2

    # beta: angle of diffraction (Eq. 1.2)
    beta = alpha + deviation_angle_deg

    # Find beta at the ends of the grating (Eq. 5.7)
    beta_min = (
        beta
        + np.deg2rad(gamma_deg)
        - np.arctan((ccd_width_mm / ch * 0.5 * ch - h_blc) / l_h)
    )
    beta_max = (
        beta
        + np.deg2rad(gamma_deg)
        - np.arctan((ccd_width_mm / ch * (1 - ch / 2) - h_blc) / l_h)
    )

    # Find lambda max/min given beta (Eq. 5.2)
    l_min = 1e6 * (np.sin(alpha) + np.sin(beta_min)) / grating_density_gr_mm
    l_max = 1e6 * (np.sin(alpha) + np.sin(beta_max)) / grating_density_gr_mm
    l_min = abs(l_min)
    l_max = abs(l_max)

    # Correct for diffraction index of air (lambda not in vacuum)
    l_min *= 1 / _n_air(l_min)
    l_max *= 1 / _n_air(l_max)

    # Create axis object to return
    scale = (l_max - l_min) / ch

    axis_class = UniformDataAxis

    axis_nm = axis_class(
        scale=scale,
        offset=l_min,
        name="Wavelength",
        units="nm",
        navigate=False,
        size=ch,
    )
    return axis_nm


solve_grating_equation.__doc__ %= GRATING_EQUATION_DOCSTRING_PARAMETERS
