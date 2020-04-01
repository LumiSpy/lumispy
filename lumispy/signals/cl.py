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

from hyperspy._signals.signal1d import Signal1D
from hyperspy._signals.lazy import LazySignal


class CLSpectrum(Signal1D):
    """General 1D CL signal class.
    ----------
    background : array
        Array containing [wavelength, background].
    """
    _signal_type = "CL"
    _signal_dimension = 1


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background = None

    def as_lazy(self, *args, **kwargs):
        """Create a copy of the Signal1D object as a
        :py:class:`~lumispy.signals.cl.CLSpectrum`.

        Parameters
        ----------
        copy_variance : bool
            If True variance from the original CLSpectrum object is copied to
            the new LazyCLSpectrum object.

        Returns
        -------
        res : :py:class:`~lumispy.signals.cl.CLSpectrum`.
            The lazy signal.
        """
        res = super().as_lazy(*args, **kwargs)
        res.__class__ = LazyCLSpectrum
        res.__init__(**res._to_dictionary())
        return res

    def decomposition(self, *args, **kwargs):
        super().decomposition(*args, **kwargs)
        self.__class__ = CLSpectrum

    def crop_edges(self, crop_px):
        """
        Crop the amount of pixels from the four edges of the scanning region, from out the edges inwards.

        Parameters
        ---------------
        crop_px : int
            Amount of pixels to be cropped on each side individually.

        Returns
        ---------------
        signal_cropped : CLSpectrum
            A smaller cropped CL signal object. If inplace is True, the original object is modified and no CLSpectrum is returned.
        """

        width = self.axes_manager.shape[0]
        height = self.axes_manager.shape[1]

        if crop_px*2 > width or crop_px*2 > height:
            raise ValueError("The pixels to be cropped cannot be larger than half the width or the length!")
        else:
            signal_cropped = self.inav[crop_px +1: width -crop_px +1, crop_px +1: height-crop_px +1]

        #Store transformation in metadata (or update the value if already previously transformed)

        try:
            px_already_cropped = signal_cropped.metadata.Signal.cropped_edges
            signal_cropped.metadata.Signal.cropped_edges = px_already_cropped + crop_px
        except:
            signal_cropped.metadata.set_item("Signal.cropped_edges", crop_px)

        return signal_cropped

    def background_subtraction(self, background=None, inplace=False):
        """
        Subtract the background to the signal in each pixel.
        If background is manually input of function as argument, it will be subtracted if it matches the x axis wavelenght values.
        Otherwise, if no background is passed, it will check on the metadata.
        If background is in metadata, it subtracts it without need to manually input background (background is automatically saved upon load_hyp() if the bakground file is found in the same folder as the data).
        Otherwise it raises an Error.

        Parameters
        ---------------
        background : numpy.array[wavelength, bkg]
            OPTIONAL: Bakground array with two columns: [wavelenght, bkg]. Length of array must match signal_axes size.

        inplace : boolean
            If False, it returns a new object with the transformation. If True, the original object is transformed, returning no object.

        Returns
        ---------------
        signal_cropped : CLSpectrum
            A smaller cropped CL signal object. If inplace is True, the original object is modified and no CLSpectrum is returned.
        """
        def subtract_self(signal, bkg):
            """
            Dummy function to be used in self.map below.
            """
            return signal - bkg


        if background is not None:
            if (background[0]).all() == (self.axes_manager.signal_axes[0].axis).all():
                bkg = background[1]

            else:
                raise ValueError('The background x axis provided as external argument is does not match the signal wavelenght x axis values.')
        else:
            if self.background != None:
                if (self.background[0]).all() == (self.axes_manager.signal_axes[0].axis).all():
                    bkg = self.background[1]

                else:
                    raise ValueError('The background x axis wavelenght values from the signal.bakground axis do not match the signal wavelenght x axis values.')
            else:
                raise ValueError('No background defined on the signal.background NOR as an input of this function.')

        if inplace == False:
            self_subtracted = self.map(subtract_self, bkg=bkg, inplace=False)
            self_subtracted.metadata.set_item("Signal.background_subtracted", True)
            return self_subtracted
        else:
            self.metadata.set_item("Signal.background_subtracted", True)
            return self.map(subtract_self, bkg=bkg, inplace=True)

    def cosmic_rays_subtraction(self, extra_percent=50, inplace=False, **kwargs):
        """
        Masks the cosmic rays away

        Parameters
        -----------
        extra_percent : float
            Extra percent of intensity added to the maximum value of the mean spectrum, which is used to threshold. Default is an extra 500% (x5) to the maximum intensity value of the mean spectrum.

        inplace : bool
            If False, a new signal object is created and returned. If True, the original signal object is modified.
        """

        def get_threshold(self, extra_percent):
            #Get the max threshold from the mean spectrum maximum
            max_threshold = max(self.mean().data)
            #Add an extra % of threshold
            max_threshold = max_threshold * extra_percent
            return max_threshold

        def remove_cosmic_ray(spectrum, threshold, mean_spectrum):
            #Remove cosmic ray leaving the spectrum pixel as normal noise
            #TO DO: Modify noise creation to be relative to actual real noise.
            if max(spectrum.data) > threshold:
                import statistics
                mean = statistics.mean(mean_spectrum.data)
                stdev = statistics.stdev(mean_spectrum.data)
                noise = np.random.normal(mean, stdev, spectrum.shape[0])
                spectrum.data = noise
            return spectrum


        threshold = get_threshold(self, extra_percent)
        mean_spectrum = self.mean()

        if inplace == False:
            signal_filtred = self.map(remove_cosmic_ray, threshold=threshold, mean_spectrum=mean_spectrum, show_progressbar=True, inplace=False)
            signal_filtred.metadata.set_item("Signal.cosmic_rays_subtracted_extra_percent", extra_percent)
            return signal_filtred
        else:
            self.metadata.set_item("Signal.cosmic_rays_subtracted_extra_percent", extra_percent)
            return self.map(remove_cosmic_ray, threshold=threshold, mean_spectrum=mean_spectrum, show_progressbar=True, inplace=True)


class LazyCLSpectrum(LazySignal, CLSpectrum):

    _lazy = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compute(self, *args, **kwargs):
        super().compute(*args, **kwargs)
        self.__class__ = CLSpectrum
        self.__init__(**self._to_dictionary())

    def decomposition(self, *args, **kwargs):
        super().decomposition(*args, **kwargs)
        self.__class__ = LazyCLSpectrum
