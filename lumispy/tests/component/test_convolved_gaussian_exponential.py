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

import pytest
import numpy as np
import hyperspy.api as hs

from lumispy.components import ConvGaussExp

sigma2fwhm = 2 * np.sqrt(2 * np.log(2))


class TestConvGaussExp:
    def setup_method(self, method):
        self.s = hs.signals.Signal1D(np.zeros(1024))
        self.s.axes_manager[0].offset = 10
        self.s.axes_manager[0].scale = 0.5
        m = self.s.create_model()
        m.append(ConvGaussExp(height=3, t0=35, sigma=10, tau=100))
        m.assign_current_values_to_all()
        self.m = m

    @pytest.mark.parametrize(("binned"), (True, False))
    def test_fit(self, binned):
        self.m.signal.axes_manager[-1].is_binned = binned
        s = self.m.as_signal()
        assert s.axes_manager[-1].is_binned == binned
        g = ConvGaussExp(height=1.5, t0=20.0, sigma=6.0, tau=60.0)
        m = s.create_model()
        m.append(g)
        m.fit(bounded=True)
        np.testing.assert_allclose(g.height.value, 3.0)
        np.testing.assert_allclose(g.t0.value, 35.0)
        np.testing.assert_allclose(g.sigma.value, 10.0)
        np.testing.assert_allclose(g.tau.value, 100.0)

    def test_util_fwhm_set(self):
        g = ConvGaussExp()
        g.fwhm = 1.0
        np.testing.assert_allclose(g.sigma.value, 1.0 / sigma2fwhm)

    def test_util_fwhm_get(self):
        g = ConvGaussExp(sigma=1.0)
        np.testing.assert_allclose(g.fwhm, 1.0 * sigma2fwhm)

    def test_normalization(self):
        m = self.s.create_model()
        m.append(ConvGaussExp(height=5.0, sigma=1e-12, tau=100.0))
        m.assign_current_values_to_all()
        s = m.as_signal()
        m1 = s.create_model()
        m1.append(ConvGaussExp(sigma=1e-12, t0=0.0))
        m1[0].sigma.free = False
        m1[0].t0.free = False
        m1.fit(bounded=True)
        m2 = s.create_model()
        m2.append(hs.model.components1D.Exponential())
        m2.fit(bounded=True)
        np.testing.assert_allclose(m1[0].height.value, m2[0].A.value, rtol=1e-3)
        np.testing.assert_allclose(m1[0].tau.value, m2[0].tau.value, rtol=1e-3)
