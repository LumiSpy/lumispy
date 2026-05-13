# -*- coding: utf-8 -*-
# Copyright 2019-2026 The LumiSpy developers
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
import numpy as np
import traits.api as t

from hyperspy.signals import Signal1D, Signal2D
from hyperspy._signals.lazy import LazySignal
from hyperspy.docstrings.signal import OPTIMIZE_ARG
from hyperspy.ui_registry import add_gui_method
from hyperspy.exceptions import SignalDimensionError


from lumispy.signals import LumiSpectrum
from lumispy.signals.common_luminescence import CommonLumi
from lumispy.signals.common_transient import CommonTransient
from lumispy.signal_tools._selector import IntervalsSelectorInMap


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

    def spec2nav_tool(
        self,
        intervals=None,
        boundarys=None,
        interactive=False,
        interval_count=2,
        optimize=True,
        display=True,
        toolkit=None,
    ):

        if interactive is True:
            tool = signal2navInteractive(
                obj=self, interval_count=interval_count, dim="spec"
            )
            tool.gui(display=display, toolkit=toolkit)
            return tool
        else:
            return self.spec2nav(
                intervals=intervals,
                boundarys=boundarys,
                optimize=optimize,
                display=display,
                toolkit=toolkit,
            )

    def spec2nav(self, intervals=None, boundarys=None, optimize=True):
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

        if intervals is None and boundarys is None:
            ls = self.transpose(signal_axes=[-1], optimize=optimize)

        if boundarys is not None and intervals is None:
            new_intervals = []
            new_intervals.append((0, boundarys[0]))
            for current, next in zip(boundarys, boundarys[1:]):
                new_intervals.append((current, next))
            new_intervals.append(
                (
                    boundarys[len(boundarys) - 1],
                    self.axes_manager[1].size * self.axes_manager[1].scale,
                )
            )
            intervals = new_intervals

        if intervals is not None:
            data = np.zeros((len(intervals), self.axes_manager[1].size))
            ls = LumiSpectrum(data)
            ls.axes_manager[0].name = self.axes_manager[0].name
            ls.axes_manager[0].units = self.axes_manager[0].units
            ls.axes_manager[1].name = self.axes_manager[1].name
            ls.axes_manager[1].units = self.axes_manager[1].units

            for i, (t1_in, t2_in) in enumerate(intervals):
                s1 = "%1.1f %s" % (t1_in, self.axes_manager[0].units)
                s2 = "%1.1f %s" % (t2_in, self.axes_manager[0].units)

                tr = self.isig[s1:s2, :].sum(self.axes_manager[0].name)
                ls.data[i] = tr

        return ls

    spec2nav.__doc__ %= (OPTIMIZE_ARG,)

    def time2nav_tool(
        self,
        intervals=None,
        boundarys=None,
        interactive=False,
        interval_count=2,
        optimize=True,
        display=True,
        toolkit=None,
    ):

        if interactive is True:
            tool = signal2navInteractive(
                obj=self, interval_count=interval_count, dim="time"
            )
            tool.gui(display=display, toolkit=toolkit)
            return tool
        else:
            return self.time2nav(
                intervals=intervals,
                boundarys=boundarys,
                optimize=optimize,
                display=display,
                toolkit=toolkit,
            )

    def time2nav(
        self, intervals=None, boundarys=None, optimize=True, display=True, toolkit=None
    ):
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

        if intervals is None and boundarys is None:
            ls = self.transpose(signal_axes=[-2], optimize=optimize)

        if boundarys is not None and intervals is None:
            new_intervals = []
            new_intervals.append((0, boundarys[0]))
            for current, next in zip(boundarys, boundarys[1:]):
                new_intervals.append((current, next))
            new_intervals.append(
                (
                    boundarys[len(boundarys) - 1],
                    self.axes_manager[1].size * self.axes_manager[1].scale,
                )
            )
            intervals = new_intervals

        if intervals is not None:
            data = np.zeros((len(intervals), self.axes_manager[0].size))
            ls = LumiSpectrum(data)
            ls.axes_manager[0].name = self.axes_manager[1].name
            ls.axes_manager[0].units = self.axes_manager[1].units
            ls.axes_manager[1].name = self.axes_manager[0].name
            ls.axes_manager[1].units = self.axes_manager[0].units

            for i, (t1_in, t2_in) in enumerate(intervals):
                t1 = "%1.2f %s" % (t1_in, self.axes_manager[1].units)
                t2 = "%1.2f %s" % (t2_in, self.axes_manager[1].units)

                sp = self.isig[:, t1:t2].sum(self.axes_manager[1].name)
                ls.data[i] = sp

        return ls

    time2nav.__doc__ %= (OPTIMIZE_ARG,)


@add_gui_method(toolkey="lumispy.LumiTransientSpectrum.time2nav_tool")
class signal2navInteractive(IntervalsSelectorInMap):
    result = t.Any()

    def __init__(self, interval_count, dim, obj=None, display=True):
        if isinstance(obj, signal2navInteractive):
            self.signal = obj.signal
        else:
            self.signal = obj
        super().__init__(self.signal, interval_count, dim)
        self.display = display

    def apply_button_clicked(self):

        if self.dim == "time":
            selected_intervals = [
                (round(interval.left), round(interval.right))
                for interval in self.intervals
            ]
            self.result = self.signal.time2nav(intervals=selected_intervals)

        if self.dim == "spec":
            self.result = self.signal.spec2nav(intervals=self.intervals)

    def validate_intervals(self):
        if any(t1 < 0 or t2 < 0 for t1, t2 in self.intervals):
            raise ValueError("negative values in intervals are not allowed")


class LazyLumiTransientSpectrum(LazySignal, LumiTransientSpectrum):
    """**Lazy 2D luminescence signal class (spectral+transient/time resolved dimensions)**"""

    _lazy = True