# -*- coding: utf-8 -*-
# Copyright 2019-2025 The LumiSpy developers
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
Signal class for luminescence transient data (2D)
-------------------------------------------------
"""

import pint

from hyperspy.signals import Signal1D, Signal2D
from hyperspy.docstrings.signal import OPTIMIZE_ARG

from lumispy.signals import LumiSpectrum, LumiTransient
from lumispy.signals.common_luminescence import CommonLumi
from lumispy.signals.common_transient import CommonTransient


class TransientSpectrumCasting(Signal1D, CommonLumi, CommonTransient):
    """**Hidden signal class**
    1D version of ``TransientSpectrum`` signal class for casting
    ``LumiTransientSpectrum` to either ``Luminescence`` or ``Transient``
    when the signal dimensionality is reduced.

    Example:
    --------

    >>> s = LumiTransientSpectrum(np.random.random((10, 10, 10, 10))) * 2
    >>> s.axes_manager.signal_axes[-1].units = 'ps'
    >>> s.axes_manager.signal_axes[0].units = 'nm'
    >>> s.sum(axis=-1)
    >>> s
    <LumiSpectrum, title: , dimensions: (10, 10|10)>
    """

    _signal_type = "TransientSpectrum"
    _signal_dimension = 1

    def __init__(self, *args, **kwargs):
        ureg = pint.UnitRegistry()
        if (
            hasattr(self, "axes_manager")
            and ureg(self.axes_manager.signal_axes[-1].units).dimensionality
            == ureg("s").dimensionality
        ):
            self.set_signal_type("Transient")
        else:
            self.set_signal_type("Luminescence")


class LumiTransientSpectrum(Signal2D, CommonLumi, CommonTransient):
    """**2D luminescence signal class (spectrum+transient/time resolved dimensions)**"""

    _signal_type = "TransientSpectrum"
    _signal_dimension = 2

    def spec2nav(self, optimize=True):
        """Return the streak image as signal with the spectral axis as navigation
        axis and the time axis as signal axis. For efficient iteration over
        transients as a function of the spectral positions (e.g. for fitting
        transients). By default, the method ensures that the data is stored optimally,
        hence often making a copy of the data.

        Parameters
        ----------
        %s

        Returns
        -------
        signal : LumiSpectrum
            A signal of type ``LumiTransient``.

        See Also
        --------
        lumispy.signals.LumiTransientSpectrum.time2nav
        hyperspy.api.signals.BaseSignal.transpose
        """
        s = self.transpose(signal_axes=[-1], optimize=optimize)
        return s

    spec2nav.__doc__ %= (OPTIMIZE_ARG,)

    def time2nav(self, optimize=True):
        """Return the streak image as signal with the time axis as navigation
        axis and the spectral axis as signal axis. For efficient iteration over
        spectra as a function of time (e.g. for fitting spectra). By default, the
        method ensures that the data is stored optimally, hence often making a copy
        of the data.

        Parameters
        ----------
        %s

        Returns
        -------
        signal : LumiSpectrum
            A signal of type ``LumiSpectrum``.

        See Also
        --------
        lumispy.signals.LumiTransientSpectrum.time2nav
        hyperspy.api.signals.BaseSignal.transpose
        """
        s = self.transpose(signal_axes=[-2], optimize=optimize)
        return s

    time2nav.__doc__ %= (OPTIMIZE_ARG,)
