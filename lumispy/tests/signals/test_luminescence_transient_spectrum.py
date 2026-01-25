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

import numpy as np

from lumispy.signals import LumiTransientSpectrum, LumiSpectrum, LumiTransient


class TestLumiTransientSpectrum0D:
    def setup_method(self, method):
        ax0 = {"name": "Time", "units": "ps", "size": 10}
        ax1 = {"name": "Wavelength", "units": "nm", "size": 10}
        self.s = LumiTransientSpectrum(np.ones(100).reshape(10, 10), axes=[ax0, ax1])

    def test_slice_wavelength(self):
        s2 = self.s.isig[:, 5]
        assert s2.axes_manager[-1].units == "nm"
        assert type(s2) == LumiSpectrum

    def test_slice_energy(self):
        s2 = self.s.to_eV(inplace=False)
        s3 = s2.isig[:, 5]
        assert s3.axes_manager[-1].units == "eV"
        assert type(s3) == LumiSpectrum

    def test_slice_time(self):
        s2 = self.s.isig[5, :]
        assert s2.axes_manager[-1].units == "ps"
        assert type(s2) == LumiTransient

    def test_sum_wl(self):
        s2 = self.s.sum(axis="Wavelength")
        assert s2.axes_manager[-1].units == "ps"
        assert type(s2) == LumiTransient

    def test_sum_E(self):
        s2 = self.s.to_eV(inplace=False)
        s3 = s2.sum(axis="Energy")
        assert s3.axes_manager[-1].units == "ps"
        assert type(s3) == LumiTransient

    def test_sum_t(self):
        s2 = self.s.sum(axis="Time")
        assert s2.axes_manager[-1].units == "nm"
        assert type(s2) == LumiSpectrum

    def test_max_wl(self):
        s2 = self.s.max(axis="Wavelength")
        assert s2.axes_manager[-1].units == "ps"
        assert type(s2) == LumiTransient

    def test_max_t(self):
        s2 = self.s.max(axis="Time")
        assert s2.axes_manager[-1].units == "nm"
        assert type(s2) == LumiSpectrum

    def test_spec2nav(self):
        s2 = self.s.spec2nav()
        assert s2.axes_manager[0].units == "nm"
        assert s2.axes_manager[-1].units == "ps"
        assert type(s2) == LumiTransient

    def test_time2nav(self):
        s2 = self.s.time2nav()
        assert s2.axes_manager[0].units == "ps"
        assert s2.axes_manager[-1].units == "nm"
        assert type(s2) == LumiSpectrum


class TestLumiTransientSpectrum2D:
    def setup_method(self, method):
        nav = {"size": 10, "navigate": True}
        ax0 = {"name": "Time", "units": "ps", "size": 10}
        ax1 = {"name": "Wavelength", "units": "nm", "size": 10}
        self.s = LumiTransientSpectrum(
            np.ones(10000).reshape(10, 10, 10, 10), axes=[nav, nav, ax0, ax1]
        )

    def test_slice_wavelength(self):
        s2 = self.s.isig[:, 5]
        assert s2.axes_manager[-1].units == "nm"
        assert type(s2) == LumiSpectrum

    def test_slice_energy(self):
        s2 = self.s.to_eV(inplace=False)
        s3 = s2.isig[:, 5]
        assert s3.axes_manager[-1].units == "eV"
        assert type(s3) == LumiSpectrum

    def test_slice_time(self):
        s2 = self.s.isig[5, :]
        assert s2.axes_manager[-1].units == "ps"
        assert type(s2) == LumiTransient

    def test_sum_wl(self):
        s2 = self.s.sum(axis="Wavelength")
        assert s2.axes_manager[-1].units == "ps"
        assert type(s2) == LumiTransient

    def test_sum_E(self):
        s2 = self.s.to_eV(inplace=False)
        s3 = s2.sum(axis="Energy")
        assert s3.axes_manager[-1].units == "ps"
        assert type(s3) == LumiTransient

    def test_sum_t(self):
        s2 = self.s.sum(axis="Time")
        assert s2.axes_manager[-1].units == "nm"
        assert type(s2) == LumiSpectrum

    def test_max_wl(self):
        s2 = self.s.max(axis="Wavelength")
        assert s2.axes_manager[-1].units == "ps"
        assert type(s2) == LumiTransient

    def test_max_t(self):
        s2 = self.s.max(axis="Time")
        assert s2.axes_manager[-1].units == "nm"
        assert type(s2) == LumiSpectrum

    def test_spec2nav(self):
        s2 = self.s.spec2nav()
        assert s2.axes_manager[0].units == "nm"
        assert s2.axes_manager[-1].units == "ps"
        assert type(s2) == LumiTransient

    def test_time2nav(self):
        s2 = self.s.time2nav()
        assert s2.axes_manager[0].units == "ps"
        assert s2.axes_manager[-1].units == "nm"
        assert type(s2) == LumiSpectrum
