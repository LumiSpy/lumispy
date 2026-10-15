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

from lumispy.components import ConvGaussTwoExp

sigma2fwhm = 2 * np.sqrt(2 * np.log(2))


class TestConvGaussTwoExp:
    def setup_method(self, method):
        s = hs.signals.Signal1D(np.zeros(1024))
        s.axes_manager[0].offset = 10
        s.axes_manager[0].scale = 0.5
        m = s.create_model()
        m.append(
            ConvGaussTwoExp(height1=3, height2=2, t0=35, sigma=10, tau1=100, tau2=80)
        )
        m.assign_current_values_to_all()
        self.m = m

    @pytest.mark.parametrize(("binned"), (True, False))
    def test_fit(self, binned):
        self.m.signal.axes_manager[-1].is_binned = binned
        s = self.m.as_signal()
        assert s.axes_manager[-1].is_binned == binned
        g = ConvGaussTwoExp(
            height1=2.8, height2=1.8, t0=34.0, sigma=9.0, tau1=90.0, tau2=70.0
        )
        m = s.create_model()
        m.append(g)
        m.fit(bounded=True)
        np.testing.assert_allclose(g.t0.value, 35.0)
        np.testing.assert_allclose(g.sigma.value, 10.0)

        expected_components = sorted(
            [
                (100.0, 3.0),
                (80.0, 2.0),
            ]
        )
        fitted_components = sorted(
            [
                (g.tau1.value, g.height1.value),
                (g.tau2.value, g.height2.value),
            ]
        )
        np.testing.assert_allclose(fitted_components, expected_components)

    def test_util_fwhm_set(self):
        g = ConvGaussTwoExp()
        g.fwhm = 1.0
        np.testing.assert_allclose(g.sigma.value, 1.0 / sigma2fwhm)

    def test_util_fwhm_get(self):
        g = ConvGaussTwoExp(sigma=1.0)
        np.testing.assert_allclose(g.fwhm, 1.0 * sigma2fwhm)
