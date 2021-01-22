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

"""Signal class for Cathodoluminescence spectral data.

"""

import numpy as np

from hyperspy._signals.lazy import LazySignal
from lumispy.signals.luminescence_spectrum import LumiSpectrum
from hyperspy.signal_tools import SpikesRemoval


class CLSpectrum(LumiSpectrum):
    """General 1D Cathodoluminescence signal class.
    ----------
    """
    _signal_type = "CL"
    _signal_dimension = 1


    def remove_spikes(self, threshold='auto', add_noise=True, noise_type='poisson',
                      show_diagnosis_histogram=False, inplace=False, luminescence_roi=None,
                      default_spike_width=5, navigation_mask=None, signal_mask=None, **kwargs):
        """

        :param luminescence_roi:
        :param inplace:
        :param show_diagnosis_histogram:
        :param noise_type:
        :param threshold:
        :param add_noise:
        :param default_spike_width:
        :param navigation_mask:
        :param signal_mask:
        :param max_num_bins:
        :return:
        """

        if show_diagnosis_histogram:
            self.spikes_diagnosis(navigation_mask=navigation_mask, signal_mask=signal_mask,
                                  **kwargs)
        if inplace:
            signal = self
        else:
            signal = self.deepcopy()

        spikes_removal = SpikesRemoval(signal, navigation_mask, signal_mask, threshold,
                                       default_spike_width, add_noise, )

        spikes_removal.noise_type == noise_type #"white", "heteroscedastic", "poisson"

        if threshold == 'auto':
            print('Threshold value found: {}'.format(spikes_removal.threshold))
        spikes_removal.remove_all_spikes()
        if inplace:
            return
        else:
            return signal

    def cosmic_rays_subtraction(self, extra_percent=50, inplace=False, **kwargs):
        """
        Masks the cosmic rays away
        USE HYPERSPY FUNCTION HERE AND ADAPT IT TO LUMISPY.
        Parameters
        -----------
        extra_percent : float
            Extra percent of intensity added to the maximum value of the mean spectrum, which is used to threshold. Default is an extra 500% (x5) to the maximum intensity value of the mean spectrum.

        inplace : bool
            If False, a new signal object is created and returned. If True, the original signal object is modified.
        """

        def get_threshold(self, extra_percent):
            # Get the max threshold from the mean spectrum maximum
            max_threshold = max(self.mean().data)
            # Add an extra % of threshold
            max_threshold = max_threshold * extra_percent
            return max_threshold

        def remove_cosmic_ray(spectrum, threshold, mean_spectrum):
            # Remove cosmic ray leaving the spectrum pixel as normal noise
            # TO DO: Modify noise creation to be relative to actual real noise.
            if max(spectrum.data) > threshold:
                import statistics
                mean = statistics.mean(mean_spectrum.data)
                stdev = statistics.stdev(mean_spectrum.data)
                noise = np.random.normal(mean, stdev, spectrum.shape[0])
                spectrum.data = noise
            return spectrum

        threshold = get_threshold(self, extra_percent)
        mean_spectrum = self.mean()

        if not inplace:
            signal_filtered = self.map(remove_cosmic_ray, threshold=threshold, mean_spectrum=mean_spectrum,
                                       show_progressbar=True, inplace=False)
            signal_filtered.metadata.set_item("Signal.cosmic_rays_subtracted_extra_percent", extra_percent)
            return signal_filtered
        else:
            self.metadata.set_item("Signal.cosmic_rays_subtracted_extra_percent", extra_percent)
            return self.map(remove_cosmic_ray, threshold=threshold, mean_spectrum=mean_spectrum, show_progressbar=True,
                            inplace=True)


class LazyCLSpectrum(LazySignal, CLSpectrum):
    _lazy = True

    pass
