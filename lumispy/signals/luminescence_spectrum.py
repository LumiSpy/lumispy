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

"""Signal class for Luminescence spectral data (1D).
"""
import warnings
from inspect import getfullargspec
from warnings import warn
import numpy as np


from hyperspy.signals import Signal1D
from hyperspy._signals.lazy import LazySignal
from hyperspy.axes import DataAxis

from lumispy.signals.common_luminescence import CommonLumi
from lumispy import nm2invcm, to_array, savetxt
from lumispy.utils import (
    axis2eV,
    data2eV,
    axis2invcm,
    data2invcm,
    solve_grating_equation,
    GRATING_EQUATION_DOCSTRING_PARAMETERS,
)
from lumispy.utils.io import (
    SAVETXT_DOCSTRING,
    SAVETXT_PARAMETERS,
    TOARRAY_DOCSTRING,
    TOARRAY_PARAMETERS,
)


class LumiSpectrum(Signal1D, CommonLumi):
    """General 1D Luminescence signal class."""

    _signal_type = "Luminescence"
    _signal_dimension = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_eV(self, inplace=True, jacobian=True):
        """Converts signal axis of 1D signal to non-linear energy axis (eV)
        using wavelength dependent permittivity of air. Assumes wavelength in
        units of nm unless the axis units are specifically set to µm.

        The intensity is converted from counts/nm (counts/µm) to counts/meV by
        doing a Jacobian transformation, see e.g. Wang and Townsend, J. Lumin.
        142, 202 (2013), which ensures that integrated signals are correct also
        in the energy domain.

        Input parameters
        ----------------
        inplace : boolean
            If `False`, a new signal object is created and returned. Otherwise
            (default) the operation is performed on the existing signal object.
        jacobian : boolean
            The default is to do the Jacobian transformation (recommended at
            least for luminescence signals), but the transformation can be
            suppressed by setting this option to `False`.

        Example
        -------
        > import numpy as np
        > from lumispy import LumiSpectrum
        > S1 = LumiSpectrum(np.ones(20), DataAxis(axis = np.arange(200,400,10)), ))
        > S1.to_eV()

        Note
        ----
        Using a non-linear axis works only for the non_uniform_axis development
        branch of HyperSpy.

        """

        # Check if non_uniform_axis is available in hyperspy version
        if not "axis" in getfullargspec(DataAxis)[0]:
            raise ImportError(
                "Conversion to energy axis works only "
                "if the non_uniform_axis branch of HyperSpy is used."
            )

        evaxis, factor = axis2eV(self.axes_manager.signal_axes[0])

        # in place conversion
        if inplace:
            if jacobian:
                self.data = data2eV(
                    self.isig[::-1].data,
                    factor,
                    self.axes_manager.signal_axes[0],
                    evaxis.axis,
                )
            else:
                self.data = self.isig[::-1].data
            self.axes_manager.remove(-1)
            self.axes_manager._axes.append(evaxis)
        # create and return new signal
        else:
            if jacobian:
                s2data = data2eV(
                    self.isig[::-1].data,
                    factor,
                    self.axes_manager.signal_axes[0],
                    evaxis.axis,
                )
            else:
                s2data = self.isig[::-1].data
            if self.data.ndim == 1:
                s2 = LumiSpectrum(s2data, axes=(evaxis.get_axis_dictionary(),))
            elif self.data.ndim == 2:
                s2 = LumiSpectrum(
                    s2data,
                    axes=(
                        self.axes_manager.navigation_axes[0].get_axis_dictionary(),
                        evaxis.get_axis_dictionary(),
                    ),
                )
            else:
                s2 = LumiSpectrum(
                    s2data,
                    axes=(
                        self.axes_manager.navigation_axes[1].get_axis_dictionary(),
                        self.axes_manager.navigation_axes[0].get_axis_dictionary(),
                        evaxis.get_axis_dictionary(),
                    ),
                )
            s2.set_signal_type(self.metadata.Signal.signal_type)
            s2.metadata = self.metadata
            return s2

    def to_invcm(self, inplace=True, jacobian=True):
        """Converts signal axis of 1D signal to non-linear wavenumber axis
        (cm^-1). Assumes wavelength in units of nm unless the axis units are
        specifically set to µm.

        The intensity is converted from counts/nm (counts/µm) to counts/cm^-1
        by doing a Jacobian transformation, see e.g. Wang and Townsend,
        J. Lumin. 142, 202 (2013), which ensures that integrated signals are
        correct also in the energy domain.

        Input parameters
        ----------------
        inplace : boolean
            If `False`, a new signal object is created and returned. Otherwise
            (default) the operation is performed on the existing signal object.
        jacobian : boolean
            The default is to do the Jacobian transformation (recommended at
            least for luminescence signals), but the transformation can be
            suppressed by setting this option to `False`.

        Examples
        --------
        > import numpy as np
        > from lumispy import LumiSpectrum
        > S1 = LumiSpectrum(np.ones(20), DataAxis(axis = np.arange(200,400,10)), ))
        > S1.to_invcm()

        Note
        ----
        Using a non-linear axis works only for the non_uniform_axis development
        branch of HyperSpy.

        """

        # Check if non_uniform_axis is available in hyperspy version
        if not "axis" in getfullargspec(DataAxis)[0]:
            raise ImportError(
                "Conversion to wavenumber axis works only"
                " if the non_uniform_axis branch of HyperSpy is used."
            )

        invcmaxis, factor = axis2invcm(self.axes_manager.signal_axes[0])

        # in place conversion
        if inplace:
            if jacobian:
                self.data = data2invcm(
                    self.isig[::-1].data,
                    factor,
                    self.axes_manager.signal_axes[0].axis,
                    invcmaxis.axis,
                )
            else:
                self.data = self.isig[::-1].data
            self.axes_manager.remove(-1)
            self.axes_manager._axes.append(invcmaxis)
        # create and return new signal
        else:
            if jacobian:
                s2data = data2invcm(
                    self.isig[::-1].data,
                    factor,
                    self.axes_manager.signal_axes[0].axis,
                    invcmaxis.axis,
                )
            else:
                s2data = self.isig[::-1].data
            if self.data.ndim == 1:
                s2 = LumiSpectrum(s2data, axes=(invcmaxis.get_axis_dictionary(),))
            elif self.data.ndim == 2:
                s2 = LumiSpectrum(
                    s2data,
                    axes=(
                        self.axes_manager.navigation_axes[0].get_axis_dictionary(),
                        invcmaxis.get_axis_dictionary(),
                    ),
                )
            else:
                s2 = LumiSpectrum(
                    s2data,
                    axes=(
                        self.axes_manager.navigation_axes[1].get_axis_dictionary(),
                        self.axes_manager.navigation_axes[0].get_axis_dictionary(),
                        invcmaxis.get_axis_dictionary(),
                    ),
                )
            s2.set_signal_type(self.metadata.Signal.signal_type)
            s2.metadata = self.metadata
            return s2

    def to_invcm_relative(self, laser, inplace=True, jacobian=True):
        """Converts signal axis of 1D signal to non-linear wavenumber axis
        (cm^-1) relative to the exciting laser wavelength (Stokes/Anti-Stokes
        shift). Assumes wavelength in units of nm unless the axis units are
        specifically set to µm.

        The intensity is converted from counts/nm (counts/µm) to counts/cm^-1
        by doing a Jacobian transformation, see e.g. Wang and Townsend,
        J. Lumin. 142, 202 (2013), which ensures that integrated signals are
        correct also in the energy domain.

        Input parameters
        ----------------
        laser : float
            Laser wavelength in same units as signal axes (nm or µm).
        inplace : boolean
            If `False`, a new signal object is created and returned. Otherwise
            (default) the operation is performed on the existing signal object.
        jacobian : boolean
            The default is to do the Jacobian transformation (recommended at
            least for luminescence signals), but the transformation can be
            suppressed by setting this option to `False`.

        Examples
        --------
        > import numpy as np
        > from lumispy import LumiSpectrum
        > S1 = LumiSpectrum(np.ones(20), DataAxis(axis = np.arange(200,400,10)), ))
        > S1.to_invcm()

        Note
        ----
        Using a non-linear axis works only for the non_uniform_axis development
        branch of HyperSpy.

        """

        # Check if non_uniform_axis is available in hyperspy version
        if not "axis" in getfullargspec(DataAxis)[0]:
            raise ImportError(
                "Conversion to wavenumber axis works only"
                " if the non_uniform_axis branch of HyperSpy is used."
            )

        invcmaxis, factor = axis2invcm(self.axes_manager.signal_axes[0])

        # convert to relative wavenumber scale
        if self.axes_manager.signal_axes[0].units == "µm":
            invcmlaser = nm2invcm(1000 * laser)
        else:
            invcmlaser = nm2invcm(laser)
        absaxis = invcmaxis.axis[::-1]
        invcmaxis.axis = invcmlaser - absaxis

        # in place conversion
        if inplace:
            if jacobian:
                self.data = data2invcm(
                    self.data, factor, self.axes_manager.signal_axes[0].axis, absaxis
                )
            # else:
            #    self.data = self.isig[::-1].data
            self.axes_manager.remove(-1)
            self.axes_manager._axes.append(invcmaxis)
        # create and return new signal
        else:
            if jacobian:
                s2data = data2invcm(
                    self.data, factor, self.axes_manager.signal_axes[0].axis, absaxis
                )
            else:
                s2data = self.data
            if self.data.ndim == 1:
                s2 = LumiSpectrum(s2data, axes=(invcmaxis.get_axis_dictionary(),))
            elif self.data.ndim == 2:
                s2 = LumiSpectrum(
                    s2data,
                    axes=(
                        self.axes_manager.navigation_axes[0].get_axis_dictionary(),
                        invcmaxis.get_axis_dictionary(),
                    ),
                )
            else:
                s2 = LumiSpectrum(
                    s2data,
                    axes=(
                        self.axes_manager.navigation_axes[1].get_axis_dictionary(),
                        self.axes_manager.navigation_axes[0].get_axis_dictionary(),
                        invcmaxis.get_axis_dictionary(),
                    ),
                )
            s2.set_signal_type(self.metadata.Signal.signal_type)
            s2.metadata = self.metadata
            return s2

    def remove_background_from_file(self, background=None, inplace=False, **kwargs):
        """
        Subtract the background to the signal in all navigation axes.If no
        background file is passed as argument, the `remove_background()` from
        HyperSpy is called with the GUI.

        Parameters
        ----------
        background : array shape (2, n) or Signal1D
            An array containing the background x-axis and the intensity values [[xs],[ys]] or a Signal1D object.
            If the x-axis values do not match the signal_axes, then interpolation is done before subtraction.
            If only the intensity values are provided, [ys], the functions assumes no interpolation needed.

        inplace : boolean
            If False, it returns a new object with the transformation. If True,
            the original object is transformed, returning no object.

        Returns
        -------
        signal : LumiSpectrum
            A background subtracted signal.
        Note
        ----
        This function does not work with non-linear axes.
        """
        if hasattr(self.metadata.Signal, "background_subtracted"):
            if self.metadata.Signal.background_subtracted is True:
                raise RecursionError(
                    "You have already removed background once. If you need to remove it again, "
                    "set the s.metadata.Signal.background_subtracted to False"
                )
        elif background is None:
            warn(
                "Using the Hyperspy specfic `remove_background` function. Use `s.remove_background()` "
                "instead.",
                category=SyntaxWarning,
            )
            self.remove_background(**kwargs)
        else:
            signal_x = self.axes_manager.signal_axes[0].axis

            if hasattr(background, "axes_manager"):  # Check if Hyperspy-like object
                x = background.axes_manager.signal_axes[0].axis
                y = background.data
                background = [x, y]

            background_xy = np.array(background)

            if background_xy.shape[0] == 1 and background_xy.dtype != "O":
                bkg_x = signal_x
                bkg_y = background_xy
            elif background_xy.shape[0] == 2 and background_xy.dtype != "O":
                try:
                    bkg_x = background_xy[0]
                    bkg_y = background_xy[1]
                    if len(bkg_x) is not len(bkg_y):
                        raise AttributeError(
                            "The length of the x and y axis must match."
                        )
                except IndexError:
                    raise AttributeError(
                        "Please provide a background file containing both the x and y axis."
                    )
            else:
                raise AttributeError(
                    "Please, provide a background of shape (2, n) or (n)"
                )

            if not np.array_equal(bkg_x, signal_x):
                # Interpolation needed
                bkg_y = np.interp(signal_x, bkg_x, bkg_y)

            if not inplace:
                self_subtracted = self.map(
                    lambda s, bkg: s - bkg, bkg=bkg_y, inplace=False
                )
                self_subtracted.metadata.set_item("Signal.background_subtracted", True)
                self_subtracted.metadata.set_item("Signal.background", bkg_y)
                return self_subtracted
            else:
                self.metadata.set_item("Signal.background_subtracted", True)
                self.metadata.set_item("Signal.background", bkg_y)
                return self.map(lambda s, bkg: s - bkg, bkg=bkg_y, inplace=True)

    SAVETXT_EXAMPLE = """
    Examples
    --------
    >>> import lumispy as lum
    >>> import numpy as np
    
    # Spectrum:
    >>> S = lum.signals.LumiSpectrum(np.arange(5))
    >>> S.savetxt('spectrum.txt')
    # 0.00000	0.00000
    # 1.00000	1.00000
    # 2.00000	2.00000
    # 3.00000	3.00000
    # 4.00000	4.00000
    
    # Linescan:
    >>> L = lum.signals.LumiSpectrum(np.arange(25).reshape((5,5)))
    >>> L.savetxt('linescan.txt')
    # 0.00000	0.00000	1.00000	2.00000	3.00000	4.00000
    # 0.00000	0.00000	5.00000	10.00000	15.00000	20.00000
    # 1.00000	1.00000	6.00000	11.00000	16.00000	21.00000
    # 2.00000	2.00000	7.00000	12.00000	17.00000	22.00000
    # 3.00000	3.00000	8.00000	13.00000	18.00000	23.00000
    # 4.00000	4.00000	9.00000	14.00000	19.00000	24.00000
    """

    def savetxt(
        self, filename, fmt="%.5f", delimiter="\t", axes=True, transpose=False, **kwargs
    ):
        """Writes luminescence spectrum object to simple text file.
        %s
        %s
        %s
        """
        savetxt(self, filename, fmt, delimiter, axes, transpose, **kwargs)

    savetxt.__doc__ %= (SAVETXT_DOCSTRING, SAVETXT_PARAMETERS, SAVETXT_EXAMPLE)

    TOARRAY_EXAMPLE = """
    Note
    --------
    The output of this function can be used to convert a signal object to a
    pandas dataframe, e.g. using `df = pd.Dataframe(S.to_array())`.
    
    Examples
    --------
    >>> import lumispy as lum
    >>> import numpy as np
    
    # Spectrum:
    >>> S = lum.signals.LumiSpectrum(np.arange(5))
    >>> S.to_array()
    # array([[0., 0.],
    #    [1., 1.],
    #    [2., 2.],
    #    [3., 3.],
    #    [4., 4.]])
    
    # Linescan:
    >>> L = lum.signals.LumiSpectrum(np.arange(25).reshape((5,5)))
    >>> L.to_array()
    # array([[ 0.,  0.,  1.,  2.,  3.,  4.],
    #    [ 0.,  0.,  1.,  2.,  3.,  4.],
    #    [ 1.,  5.,  6.,  7.,  8.,  9.],
    #    [ 2., 10., 11., 12., 13., 14.],
    #    [ 3., 15., 16., 17., 18., 19.],
    #    [ 4., 20., 21., 22., 23., 24.]])
    """

    def to_array(self, axes=True, transpose=False):
        """Returns luminescence spectrum object as numpy array (optionally
        including the axes).
        %s
        %s
        %s
        """
        return to_array(self, axes, transpose)

    to_array.__doc__ %= (TOARRAY_DOCSTRING, TOARRAY_PARAMETERS, TOARRAY_EXAMPLE)

    def px_to_nm_grating_solver(
        self,
        gamma_deg,
        deviation_angle_deg,
        focal_length_mm,
        ccd_width_mm,
        grating_central_wavelength_nm,
        grating_density_gr_mm,
        inplace=False,
    ):
        """
        Converts signal axis of 1D signal (in pixels) to wavelength, solving the grating
        equation.
        See ``lumispy.axes.solve_grating_equation` for more details.

        Parameters
        ----------------
        %s
        inplace : bool
            If False, it returns a new object with the transformation. If True,
            the original object is transformed, returning no object.

        Returns
        ---------------
        signal : LumiSpectrum
            A signal with calibrated wavelength units.

        Example
        -------
        > s = LumiSpectrum(np.ones(20),))
        > s.px_to_nm_grating_solver(*params, inplace=True)
        > s.axes_manager.signal_axes[0].units == 'nm'
        """

        nm_axis = solve_grating_equation(
            self.axes_manager.signal_axes[0],
            gamma_deg,
            deviation_angle_deg,
            focal_length_mm,
            ccd_width_mm,
            grating_central_wavelength_nm,
            grating_density_gr_mm,
        )

        if inplace:
            s = self
        else:
            s = self.deepcopy()

        s.axes_manager.remove(-1)
        s.axes_manager._axes.append(nm_axis)

        return s

    px_to_nm_grating_solver.__doc__ %= GRATING_EQUATION_DOCSTRING_PARAMETERS


class LazyLumiSpectrum(LazySignal, LumiSpectrum):
    _lazy = True

    pass
