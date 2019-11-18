#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2019 The hyperspy_cl developers
#
# This file is part of hyperspy_cl.
#
# hyperspy_cl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# hyperspy_cl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with hyperspy_cl.  If not, see <http://www.gnu.org/licenses/>.

"""Signal class for cathodoluminescence spectral data acquired in STEM.

"""

import numpy as np

from hyperspy_cl.signals.cl import CLSpectrum
from hyperspy._signals.lazy import LazySignal


class CLSTEMSpectrum(CLSpectrum):
    _signal_type = "cl_spectrum"

    def __init__(self, *args, **kwargs):
        self, args, kwargs = push_metadata_through(self, *args, **kwargs)
        super().__init__(*args, **kwargs)

    def as_lazy(self, *args, **kwargs):
        """Create a copy of the Diffraction1D object as a
        :py:class:`~hyperspy_cl.signals.diffraction1d.LazyDiffraction1D`.

        Parameters
        ----------
        copy_variance : bool
            If True variance from the original Diffraction1D object is copied to
            the new LazyDiffraction1D object.

        Returns
        -------
        res : :py:class:`~hyperspy_cl.signals.diffraction1d.LazyDiffraction1D`.
            The lazy signal.
        """
        res = super().as_lazy(*args, **kwargs)
        res.__class__ = LazyDiffraction1D
        res.__init__(**res._to_dictionary())
        return res

    def decomposition(self, *args, **kwargs):
        super().decomposition(*args, **kwargs)
        self.__class__ = Diffraction1D


class LazyCLSTEMSpectrum(LazySignal, CLSTEMSpectrum):

    _lazy = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compute(self, *args, **kwargs):
        super().compute(*args, **kwargs)
        self.__class__ = CLSTEMSpectrum
        self.__init__(**self._to_dictionary())

    def decomposition(self, *args, **kwargs):
        super().decomposition(*args, **kwargs)
        self.__class__ = LazyCLSTEMSpectrum
