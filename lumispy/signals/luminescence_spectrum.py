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


from inspect import getfullargspec

class LumiSpectrum(Signal1D, CommonLumi):
    """General 1D Luminescence signal class.
    """
    _signal_type = "Luminescence"
    _signal_dimension = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_eV(self,inplace=True):
        """Converts signal axis of 1Dsignal to non-linear energy axis (eV) 
        using wavelength dependent permittivity of air. Assumes WL in units of 
        nm unless the axis units are specifically set to µm.
        
        The intensity is converted from counts/nm (counts/µm) to counts/meV by 
        doing a Jacobian transformation, see e.g. Wang and Townsend, J. Lumin. 142, 
        202 (2013).
    
        
        Input parameters
        ----------------
        inplace : boolean
            If `False`, a new signal object is created and returned. Otherwise 
            (default) the operation is performed on the existing signal object.
        
        Note
        ----
        Setting non linear scale instead of offset and scale work only for 
        the non_uniform_axis branch of hyperspy.
    
        """
        
        # Check if non_uniform_axis is available in hyperspy version
        if not 'axis' in getfullargspec(DataAxis)[0]:
            raise NotImplementedError('Conversion to energy axis works only if '
                                'the non_uniform_axis branch of hyperspy is used.')

        evaxis,factor = axis2eV(self.axes_manager.signal_axes[0])
        
        if inplace:
            self.data = data2eV(self.isig[::-1].data, factor,
                            self.axes_manager.signal_axes[0].axis, evaxis.axis)
            self.axes_manager.remove(-1)
            self.axes_manager._axes.append(evaxis)
        else:
            s2data = data2eV(self.isig[::-1].data, factor,
                            self.axes_manager.signal_axes[0].axis, evaxis.axis)
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
            return s2
            # Use current signal object instead of Signal1D
            # Copy metadata to new signal object


class LazyLumiSpectrum(LazySignal, LumiSpectrum):
    _lazy = True

    pass
