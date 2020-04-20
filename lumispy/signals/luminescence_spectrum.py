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

import numpy as np

from hyperspy._signals.signal1d import Signal1D
from hyperspy._signals.lazy import LazySignal
from lumispy.signals.common_luminescence import CommonLumi


class LumiSpectrum(Signal1D, CommonLumi):
    """General 1D Luminescence signal class.
    ----------
    background : array
        Array containing [wavelength, background].
    """
    _signal_type = "Luminescence_Spectrum"
    _signal_dimension = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background = None

    def as_lazy(self, *args, **kwargs):
        """Create a copy of the Signal1D object as a
        :py:class:`~lumispy.signals.cl.LumiSpectrum`.

        Parameters
        ----------
        copy_variance : bool
            If True variance from the original LumiSpectrum object is copied to
            the new LazyLumiSpectrum object.

        Returns
        -------
        res : :py:class:`~lumispy.signals.cl.LumiSpectrum`.
            The lazy signal.
        """
        res = super().as_lazy(*args, **kwargs)
        res.__class__ = LazyLumiSpectrum
        res.__init__(**res._to_dictionary())
        return res

    def decomposition(self, *args, **kwargs):
        super().decomposition(*args, **kwargs)
        self.__class__ = LumiSpectrum


class LazyLumiSpectrum(LazySignal, LumiSpectrum):
    _lazy = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compute(self, *args, **kwargs):
        super().compute(*args, **kwargs)
        self.__class__ = LumiSpectrum
        self.__init__(**self._to_dictionary())

    def decomposition(self, *args, **kwargs):
        super().decomposition(*args, **kwargs)
        self.__class__ = LazyLumiSpectrum
