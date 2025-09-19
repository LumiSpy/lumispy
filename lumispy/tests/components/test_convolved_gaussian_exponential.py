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

import pytest

import numpy as np
import hyperspy.api as hs

from lumispy.components import ConvGaussExp

sqrt2pi = np.sqrt(2 * np.pi)
sigma2fwhm = 2 * np.sqrt(2 * np.log(2))


def test_function():
    g = ConvGaussExp(height=3, t0=35, sigma=10, tau=100)
    assert g.function(-50) == 0.0
    np.testing.assert_allclose(g.function(35), 1.3874364)


class TestConvGaussExp:
    def setup_method(self, method):
        s = hs.signals.Signal1D(np.zeros(1024))
        s.axes_manager[0].offset = 10
        s.axes_manager[0].scale = 0.5
        m = s.create_model()
        m.append(ConvGaussExp(height=3, t0=35, sigma=10, tau=100))
        m.assign_current_values_to_all()
        self.m = m

    @pytest.mark.parametrize(("binned"), (True, False))
    def test_fit(self, binned):
        self.m.signal.axes_manager[-1].is_binned = binned
        s = self.m.as_signal()
        assert s.axes_manager[-1].is_binned == binned
        g = ConvGaussExp()
        m = s.create_model()
        m.append(g)
        m.fit()
        np.testing.assert_allclose(g.height.value, 3.0)
        np.testing.assert_allclose(g.t0.value, 35.0)
        np.testing.assert_allclose(g.sigma.value, 10.0)
        np.testing.assert_allclose(g.tau.value, 100.0)


def test_util_fwhm_set():
    g1 = ConvGaussExp()
    g1.fwhm = 1.0
    np.testing.assert_allclose(g1.sigma.value, 1.0 / sigma2fwhm)


def test_util_fwhm_get():
    g1 = ConvGaussExp(sigma=1.0)
    np.testing.assert_allclose(g1.fwhm, 1.0 * sigma2fwhm)

