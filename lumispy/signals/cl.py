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

    def crop_edges(self, crop_px, inplace = False):
        """
        Crop the amount of pixels from the four edges of the scanning region, from out the edges inwards.

        Parameters
        ---------------
        crop_px : int
            Amount of pixels to be cropped on each side individually.

        inplace : boolean
            If False, it returns a new object with the transformation. If True, the original object is transformed, returning no object.

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
            signal_cropped.metadata.set_item("Signal.cropped_edges", crop_px)

        if inplace == True:
            self = signal_cropped
            return self
        else:
            return signal_cropped


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
