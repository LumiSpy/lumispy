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
    _signal_type = "CL_SEM"

    def correct_grating_shift(self, cal_factor_x_axis, corr_factor_grating):
        """"
        Applies shift caused by the grating offset wrt the scanning centre.
        Authorship: Gunnar Kusch (gk419@cam.ac.uk)

        :param cal_factor_x_axis: The navigation correction factor.
        :param corr_factor_grating: The grating correction factor.
        """


        # Avoid correcting for this shift twice (first time it fails, so except
        # block runs. Second time, try succeeds, so except block is skipped):
        try:
            self.metadata.Signal.grating_corrected == True
        except Exception:
            # Get all relevant parameters
            md = self.metadata

            nx = md.Acquisition_instrument.SEM.resolution_x
            ny = md.Acquisition_instrument.SEM.resolution_y
            grating = md.Acquisition_instrument.Spectrometer.grating
            fov = md.Acquisition_instrument.SEM.FOV
            acquisition_system = md.Acquisition_instrument.acquisition_system

            # Correction of the Wavelength Shift along the X-Axis
            calax = cal_factor_x_axis / (fov * nx)
            garray = np.arange((-corr_factor_grating / 2) * calax * 1000 * (nx),
                               (corr_factor_grating / 2) * calax * 1000 * (nx), corr_factor_grating * calax
                               * 1000)  # (Total Variation, Channels, Step)
            barray = np.full((nx, ny), garray)

            self.shift1D(barray)

            # Store modification in metadata
            md.set_item("Signal.grating_corrected", True)
        else:
            raise Exception("You already corrected for the grating shift.")


class LazyCLSEMSpectrum(LazySignal, CLSEMSpectrum):
    _lazy = True

    pass
