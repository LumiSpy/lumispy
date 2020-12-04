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

"""Signal class for Luminescence spectral data (1D).
"""

from hyperspy._signals.signal1d import Signal1D
from hyperspy._signals.lazy import LazySignal
from hyperspy.axes import DataAxis
from lumispy.signals.common_luminescence import CommonLumi
from lumispy.utils.axes import axis2eV
from lumispy.utils.axes import data2eV
from lumispy.utils.axes import axis2invcm
from lumispy.utils.axes import data2invcm
from lumispy.utils.axes import nm2invcm

from inspect import getfullargspec


class LumiSpectrum(Signal1D, CommonLumi):
    """General 1D Luminescence signal class.
    """
    _signal_type = "Luminescence"
    _signal_dimension = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def to_eV(self,inplace=True,jacobian=True):
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
        if not 'axis' in getfullargspec(DataAxis)[0]:
            raise ImportError('Conversion to energy axis works only '
                         'if the non_uniform_axis branch of HyperSpy is used.')

        evaxis,factor = axis2eV(self.axes_manager.signal_axes[0])
        
        # in place conversion
        if inplace:
            if jacobian:
                self.data = data2eV(self.isig[::-1].data, factor,
                            self.axes_manager.signal_axes[0].axis, evaxis.axis)
            else:
                self.data = self.isig[::-1].data
            self.axes_manager.remove(-1)
            self.axes_manager._axes.append(evaxis)
        # create and return new signal
        else:
            if jacobian:
                s2data = data2eV(self.isig[::-1].data, factor,
                            self.axes_manager.signal_axes[0].axis, evaxis.axis)
            else:
                s2data = self.isig[::-1].data
            if self.data.ndim == 1:
                s2 = Signal1D(s2data, axes=(evaxis.get_axis_dictionary(),))
            elif self.data.ndim == 2:
                s2 = Signal1D(s2data, axes=
                     (self.axes_manager.navigation_axes[0].get_axis_dictionary(),
                     evaxis.get_axis_dictionary(), ))
            else:
                s2 = Signal1D(s2data, axes=
                     (self.axes_manager.navigation_axes[1].get_axis_dictionary(),
                     self.axes_manager.navigation_axes[0].get_axis_dictionary(),
                     evaxis.get_axis_dictionary(), ))
            s2.set_signal_type(self.metadata.Signal.signal_type)
            s2.metadata = self.metadata
            return s2
            
            
    def to_invcm(self,inplace=True,jacobian=True):
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
        
        Example
        -------
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
        if not 'axis' in getfullargspec(DataAxis)[0]:
            raise ImportError('Conversion to wavenumber axis works only'
                        ' if the non_uniform_axis branch of HyperSpy is used.')

        invcmaxis,factor = axis2invcm(self.axes_manager.signal_axes[0])
        
        # in place conversion
        if inplace:
            if jacobian:
                self.data = data2invcm(self.isig[::-1].data, factor,
                        self.axes_manager.signal_axes[0].axis, invcmaxis.axis)
            else:
                self.data = self.isig[::-1].data
            self.axes_manager.remove(-1)
            self.axes_manager._axes.append(invcmaxis)
        # create and return new signal
        else:
            if jacobian:
                s2data = data2invcm(self.isig[::-1].data, factor,
                        self.axes_manager.signal_axes[0].axis, invcmaxis.axis)
            else:
                s2data = self.isig[::-1].data
            if self.data.ndim == 1:
                s2 = Signal1D(s2data, axes=(invcmaxis.get_axis_dictionary(),))
            elif self.data.ndim == 2:
                s2 = Signal1D(s2data, axes=
                    (self.axes_manager.navigation_axes[0].get_axis_dictionary(),
                    invcmaxis.get_axis_dictionary(), ))
            else:
                s2 = Signal1D(s2data, axes=
                    (self.axes_manager.navigation_axes[1].get_axis_dictionary(),
                    self.axes_manager.navigation_axes[0].get_axis_dictionary(),
                    invcmaxis.get_axis_dictionary(), ))
            s2.set_signal_type(self.metadata.Signal.signal_type)
            s2.metadata = self.metadata
            return s2


    def to_invcm_relative(self,laser,inplace=True,jacobian=True):
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
        
        Example
        -------
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
        if not 'axis' in getfullargspec(DataAxis)[0]:
            raise ImportError('Conversion to wavenumber axis works only'
                        ' if the non_uniform_axis branch of HyperSpy is used.')

        invcmaxis,factor = axis2invcm(self.axes_manager.signal_axes[0])
        
        # convert to relative wavenumber scale
        if self.axes_manager.signal_axes[0].units == 'µm':
            invcmlaser=nm2invcm(1000*laser)
        else:
            invcmlaser=nm2invcm(laser)
        absaxis = invcmaxis.axis[::-1]
        invcmaxis.axis = invcmlaser - absaxis
        
        # in place conversion
        if inplace:
            if jacobian:
                self.data = data2invcm(self.data, factor,
                        self.axes_manager.signal_axes[0].axis, absaxis)
            #else:
            #    self.data = self.isig[::-1].data
            self.axes_manager.remove(-1)
            self.axes_manager._axes.append(invcmaxis)
        # create and return new signal
        else:
            if jacobian:
                s2data = data2invcm(self.data, factor,
                        self.axes_manager.signal_axes[0].axis, absaxis)
            else:
                s2data = self.data
            if self.data.ndim == 1:
                s2 = Signal1D(s2data, axes=(invcmaxis.get_axis_dictionary(),))
            elif self.data.ndim == 2:
                s2 = Signal1D(s2data, axes=
                    (self.axes_manager.navigation_axes[0].get_axis_dictionary(),
                    invcmaxis.get_axis_dictionary(), ))
            else:
                s2 = Signal1D(s2data, axes=
                    (self.axes_manager.navigation_axes[1].get_axis_dictionary(),
                    self.axes_manager.navigation_axes[0].get_axis_dictionary(),
                    invcmaxis.get_axis_dictionary(), ))
            s2.set_signal_type(self.metadata.Signal.signal_type)
            s2.metadata = self.metadata
            return s2


    def background_subtraction(self, background, inplace=False):
        """
        Subtract the background to the signal in all navigation axes.
        TO DO: Make it compatible with non-matching wavelengths

        Parameters
        ---------------
        background : array
           An array with the background intensity values. Length of array must
           match signal_axes size.

        inplace : boolean
            If False, it returns a new object with the transformation. If True,
            the original object is transformed, returning no object.

        Returns
        ---------------
        signal : LumiSpectrum
            A background subtracted signal.
        """

        if not inplace:
            self_subtracted = self.map(lambda s, bkg: s - bkg, bkg=background, inplace=False)
            self_subtracted.metadata.set_item("Signal.background_subtracted", True)
            self_subtracted.metadata.set_item("Signal.background", background)
            return self_subtracted
        else:
            self.metadata.set_item("Signal.background_subtracted", True)
            self.metadata.set_item("Signal.background", background)
            return self.map(lambda s, bkg: s - bkg, bkg=background, inplace=True)


class LazyLumiSpectrum(LazySignal, LumiSpectrum):
    _lazy = True

    pass
