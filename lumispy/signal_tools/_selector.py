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
Selector class
-------------------------------------------------
"""

import traits.api as t

from hyperspy.roi import SpanROI
from hyperspy.exceptions import SignalDimensionError


class IntervalsSelectorInMap(t.HasTraits):
    intervals = t.List(SpanROI)

    color_list = ["blue", "orange", "green", "red", "yellow"]

    def __init__(self, signal, interval_count, dim):
        self.signal = signal
        self.interval_count = interval_count
        self.dim = dim
        if dim == "time":
            self.dim_idx = 1
        elif dim == "spec":
            self.dim_idx = 0
        self.intervals = []

        if self.signal.axes_manager.signal_dimension != 2:
            raise SignalDimensionError(self.signal.axes_manager.signal_dimension, 2)

        if self.signal._plot is None or not self.signal._plot.is_active:
            self.signal.plot()

        for i in range(interval_count):
            share = (i + 0.5) / interval_count
            left = (
                (share - (0.4 / interval_count))
                * self.signal.axes_manager[self.dim_idx].size
                * self.signal.axes_manager[self.dim_idx].scale
            ) + self.signal.axes_manager[self.dim_idx].offset
            right = (
                share
                * self.signal.axes_manager[self.dim_idx].size
                * self.signal.axes_manager[self.dim_idx].scale
            ) + self.signal.axes_manager[self.dim_idx].offset
            self.intervals.append(SpanROI(left=left, right=right))

        for i in range(interval_count):
            self.intervals[i].interactive(
                self.signal,
                axes=self.signal.axes_manager[self.dim_idx],
                color=self.color_list[i % len(self.color_list)],
            )
