# -*- coding: utf-8 -*-
# Copyright 2019-2022 The LumiSpy developers
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

"""
Signal class for cathodoluminescence spectral data
--------------------------------------------------
"""

from inspect import getfullargspec
import numpy as np
from warnings import warn

from hyperspy._signals.lazy import LazySignal
from hyperspy.signal_tools import SpikesRemoval

from lumispy.signals import LumiSpectrum


class CLSpectrum(LumiSpectrum):
    """**General 1D cathodoluminescence signal class.**"""

    _signal_type = "CL"
    _signal_dimension = 1

    def _make_signal_mask(self, luminescence_roi):
        """Creates a mask from the peak position and peak widths of the
        luminescence spectrum.

        Parameters
        ----------
        luminescence_roi: array
            In the form of an array of pairwise elements
            [[peak1_x, peak1_width], [peak2_x, peak2_width],...].

        Returns
        -------
        array
            A `signal_mask`.
        """

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
            signal_mask[index_min : index_max + 1] *= 0

        return np.invert(signal_mask.astype("bool"))

    def remove_spikes(
        self,
        threshold="auto",
        show_diagnosis_histogram=False,
        inplace=False,
        luminescence_roi=None,
        signal_mask=None,
        add_noise=False,
        navigation_mask=None,
        interactive=False,
        **kwargs
    ):

        if luminescence_roi is not None and signal_mask is not None:
            raise AttributeError(
                "Only either `luminescence_roi` or the `signal_mask` can be an input."
            )

        if luminescence_roi is not None and signal_mask is None:
            signal_mask = self._make_signal_mask(luminescence_roi)

        if show_diagnosis_histogram:
            self.spikes_diagnosis(
                navigation_mask=navigation_mask, signal_mask=signal_mask, **kwargs
            )
        if inplace:
            signal = self
        else:
            signal = self.deepcopy()

        spikes_removal = signal.spikes_removal_tool(
            signal_mask=signal_mask,
            navigation_mask=navigation_mask,
            threshold=threshold,
            interactive=interactive,
            add_noise=add_noise,
            **kwargs
        )

        if threshold == "auto":
            warn(
                "Threshold value: {:.2f}".format(spikes_removal.threshold), UserWarning
            )

        if inplace:
            return
        else:
            return signal

    REMOVE_SPIKES_DOCSTRINGS = """HyperSpy-based spike removal tool adapted to
        LumiSpy to run non-interactively and without noise addition by default.
        %s
        
        Other Parameters
        ----------------
        show_diagnosis_histogram: bool
            Plot or not the derivative histogram to show the magnitude of the spikes present.
        inplace: bool
            If False, a new signal object is created and returned. If True, the original signal object is modified.
        luminescence_roi: array
            The peak position and peak widths of the peaks in the luminescence spectrum.
            In the form of an array of pairwise elements [[peak1_x, peak1_width], [peak2_x, peak2_width],...]
            in the units of the signal axis. It creates a signal_mask protecting the peak regions.
            To be used instead of `signal_mask`.

        Returns
        -------
        None or CLSpectrum
            Depends on inplace, returns or overwrites the CLSpectrum after spike removal.
        """
    remove_spikes.__doc__ = REMOVE_SPIKES_DOCSTRINGS % (
        LumiSpectrum.spikes_removal_tool.__doc__
    )


class LazyCLSpectrum(LazySignal, CLSpectrum):
    """**General lazy 1D cathodoluminescence signal class.**"""

    _lazy = True

    pass


"""SEM specific signal class for Cathodoluminescence spectral data.
"""


class CLSEMSpectrum(CLSpectrum):
    """**1D scanning electron microscopy cathodoluminescence signal class.**"""

    _signal_type = "CL_SEM"

    def correct_grating_shift(
        self, cal_factor_x_axis, corr_factor_grating, sem_magnification, **kwargs
    ):
        """Applies shift caused by the grating offset wrt the scanning centre.
        Authorship: Gunnar Kusch (gk419@cam.ac.uk)

        Parameters
        ----------
        cal_factor_x_axis
            The navigation correction factor.
        corr_factor_grating
            The grating correction factor.
        sem_magnification
            The SEM (real) magnification value.
            For the Attolight original metadata, take the `SEM.Real_Magnification` value
        kwargs
            The parameters passed to `hyperspy.align1D()` function like:
            interpolation_method ('linear', 'nearest', 'zero', 'slinear', 'quadratic, 'cubic')
            parallel: Bool
            crop, expand, fill_value ...

        """

        # Don't correct for grating shift if this is already corrected
        if self.metadata.get_item("Signal.grating_corrected") is True:
            raise RuntimeError("The grating shift has already been corrected.")
        else:
            # Get all relevant parameters
            (nx, ny) = self.axes_manager.navigation_shape[:2]
            fov = sem_magnification

            # Correction of the Wavelength Shift along the X-Axis
            calax = cal_factor_x_axis / (fov * nx)
            # (Total Variation, Channels, Step)
            garray = np.arange(
                (-corr_factor_grating / 2) * calax * 1000 * nx,
                (corr_factor_grating / 2) * calax * 1000 * nx,
                corr_factor_grating * calax * 1000,
            )
            barray = np.full((ny, nx), garray)

            self.shift1D(barray, **kwargs)

            # Store modification in metadata
            self.metadata.set_item("Signal.grating_corrected", True)


class LazyCLSEMSpectrum(LazySignal, CLSEMSpectrum):
    """**Lazy 1D scanning electron microscopy cathodoluminescence signal class.**"""

    _lazy = True

    pass


"""STEM specific signal class for Cathodoluminescence spectral data.
"""


class CLSTEMSpectrum(CLSpectrum):
    """**1D scanning transmission electron microscopy cathodoluminescence signal class.**"""

    _signal_type = "CL_STEM"

    pass


class LazyCLSTEMSpectrum(LazySignal, CLSTEMSpectrum):
    """**Lazy 1D scanning transmission electron microscopy cathodoluminescence signal class.**"""

    _lazy = True

    pass
