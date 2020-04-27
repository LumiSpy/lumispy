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

"""Signal class for cathodoluminescence spectral data.

"""

import numpy as np

from lumispy.signals.cl_spectrum import CLSpectrum
from hyperspy._signals.lazy import LazySignal


class CLSEMSpectrum(CLSpectrum):
    _signal_type = "CL_SEM_Spectrum"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def as_lazy(self, *args, **kwargs):
        """Create a copy of the CLSpectrum object as a
        :py:class:`~lumispy.signals.cl.LazyCLSEMSpectrum`.

        Parameters
        ----------
        copy_variance : bool
            If True variance from the original CLSEMSpectrum object is copied
            to the new CLSEMSpectrum object.

        Returns
        -------
        res : :py:class:`~lumispy.signals.cl.CLSEMSpectrum`.
            The lazy signal.
        """
        res = super().as_lazy(*args, **kwargs)
        res.__class__ = LazyCLSEMSpectrum
        res.__init__(**res._to_dictionary())
        return res

    def decomposition(self, *args, **kwargs):
        super().decomposition(*args, **kwargs)
        self.__class__ = CLSEMSpectrum

    def correct_grating_shift(self):
        """"
        Applies shift caused by the grating offset wrt the scanning centre.

        Parameters
        ------------
        self : CLSEMSpectrum
            Metadata should have grating, nx, ny, fov and acquisition_system

        Returns
        ------------
        self: CLSEMSpectrum
            Wavelength shift corrected across the scanning dimension

        Authorship: Gunnar Kusch (gk419@cam.ac.uk)
        """
        from lumispy.io_plugins.attolight import attolight_systems

        # Avoid correcting for this shift twice (first time it fails, so except
        # block runs. Second time, try succeeds, so except block is skipped):
        try:
            self.metadata.Signal.grating_corrected == True
        except:
            # Get all relevant parameters
            md = self.metadata

            nx = md.Acquisition_instrument.SEM.resolution_x
            ny = md.Acquisition_instrument.SEM.resolution_y
            grating = md.Acquisition_instrument.Spectrometer.grating
            fov = md.Acquisition_instrument.SEM.FOV
            acquisition_system = md.Acquisition_instrument.acquisition_system

            cal_factor_x_axis = attolight_systems[acquisition_system]['cal_factor_x_axis']

            # Get the correction factor for the relevant grating (extracted from
            # the acquisition_systems dictionary)
            try:
                corrfactor = attolight_systems[acquisition_system]['grating_corrfactors'][grating]
            except:
                raise Exception("Sorry, the grating is not calibrated yet. "
                                "No grating shift correction can be applied. "
                                "Go to lumispy.io.attolight and "
                                "add the missing grating_corrfactors in the attolight_sysyems dict.")

            # Correction of the Wavelength Shift along the X-Axis
            calax = cal_factor_x_axis / (fov * nx)
            garray = np.arange((-corrfactor / 2) * calax * 1000 * (nx),
                               (corrfactor / 2) * calax * 1000 * (nx), corrfactor * calax
                               * 1000)  # (Total Variation, Channels, Step)
            barray = np.full((nx, ny), garray)

            self.shift1D(barray)

            # Store modification in metadata
            md.set_item("Signal.grating_corrected", True)
        else:
            raise Exception("You already corrected for the grating shift.")


class LazyCLSEMSpectrum(LazySignal, CLSEMSpectrum):
    _lazy = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compute(self, *args, **kwargs):
        super().compute(*args, **kwargs)
        self.__class__ = CLSEMSpectrum
        self.__init__(**self._to_dictionary())

    def decomposition(self, *args, **kwargs):
        super().decomposition(*args, **kwargs)
        self.__class__ = LazyCLSEMSpectrum
