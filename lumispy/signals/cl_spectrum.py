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

    def _make_signal_mask(self, luminescence_roi):

        ax = self.axes_manager.signal_axes[0].axis
        signal_mask = np.ones(np.shape(ax))

        if len(np.shape(luminescence_roi)) == 1:
            luminescence_roi = np.array([luminescence_roi])

        for p in luminescence_roi:
            x, w = p
            x_min = x - w / 2
            x_max = x + w / 2
            index_min = np.abs(ax - x_min).argmin()
            index_max = np.abs(ax - x_max).argmin()
            signal_mask[index_min:index_max + 1] *= 0

        return np.invert(signal_mask.astype('bool'))

    def remove_spikes(self, threshold='auto', add_noise=True, noise_type='poisson',
                      show_diagnosis_histogram=False, inplace=False, luminescence_roi=None, signal_mask=None,
                      navigation_mask=None, default_spike_width=5, **kwargs):
        """
        Hyperspy-based spike removal function.
        If a GUI interactive spike removal tool is desired, use `s.spikes_removal_tool()` instead.

        :param threshold: 'auto' or int
            The derivative magnitude threshold above which to find spikes.
            If `int` set the threshold value use for the detecting the spikes.
            If `auto`, determine the threshold value as being the first zero
            value in the histogram obtained from the
            :py:meth:`~hyperspy.signals._signal1d.Signal1D.spikes_diagnosis`
            method.
        :param add_noise: bool
            Whether to add noise to the interpolated part of the spectrum.
            The noise properties defined in the Signal metadata are used if present,
             otherwise 'poisson' shot noise is used as a default.
        :param noise_type: str
            By default 'poission' shoot noise is used if `add_noise` is True.
            Noise types: "white", "heteroscedastic" or "poisson".
        :param show_diagnosis_histogram: bool
            Plot or not the derivative histogram to show the magnitude of the spikes present.
        :param inplace: bool
            If False, a new signal object is created and returned. If True, the original signal object is modified.
        :param luminescence_roi: array
            The peak position and peak widths of the peaks in the luminescence spectrum.
            In the form of an array of pairwise elements [[peak1_x, peak1_width], [peak2_x, peak2_width],...]
            in the units of the signal axis. It creates a signal_mask protecting the peak regions.
            To be used instead of `signal_mask`.
        :param signal_mask: boolean array
            Restricts the operation to the signal locations not marked as True (masked).
        :param navigation_mask: boolean array
            Restricts the operation to the navigation locations not marked as True (masked).
        :param default_spike_width: int
            Width over which to do the interpolation when removing all spike.
        :param kwargs: dict
            Keyword arguments pass to `hyperspy.signal.signal.BaseSignal.get_histogram`.

        :return: None or CLSpectrum
            Depends on inplace, returns or overwrites the CLSpectrum after spike removal.
        """
        if luminescence_roi is not None and signal_mask is None:
            signal_mask = self._make_signal_mask(luminescence_roi)

        if show_diagnosis_histogram:
            self.spikes_diagnosis(navigation_mask=navigation_mask, signal_mask=signal_mask,
                                  **kwargs)
        if inplace:
            signal = self
        else:
            signal = self.deepcopy()

        spikes_removal = SpikesRemoval(signal, navigation_mask, signal_mask, threshold,
                                       default_spike_width, add_noise, )

        spikes_removal.noise_type == noise_type

        if threshold == 'auto':
            print('Threshold value found: {}'.format(spikes_removal.threshold))
        spikes_removal.remove_all_spikes()
        if inplace:
            return
        else:
            return signal


class LazyCLSpectrum(LazySignal, CLSpectrum):
    _lazy = True

    pass
