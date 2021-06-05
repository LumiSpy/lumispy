# -*- coding: utf-8 -*-
# Copyright 2019-2021 The LumiSpy developers
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

import hyperspy
import numpy as np
import pytest

from lumispy.signals import CLSEMSpectrum


class TestCLSEMSpectrum:
    @pytest.mark.skipif(
        hyperspy.__version__ == "1.6.2", reason="Broken with hyperspy 1.6.2"
    )
    @pytest.mark.parametrize("nx, ny", [(10, 20), (20, 10)])
    def test_correct_grating_shift(self, nx, ny):
        calx, corg, fov = 1e-10, 1e-10, 1e-10
        s = CLSEMSpectrum(np.random.random(nx * ny * 100).reshape(ny, nx, 100))

        garray = np.arange(
            (-corg / 2) * calx / (fov * nx) * 1000 * nx,
            (corg / 2) * calx / (fov * nx) * 1000 * nx,
            corg * calx / (fov * nx) * 1000,
        )
        barray = np.full((ny, nx), garray)

        s2 = s.deepcopy()
        s.correct_grating_shift(calx, corg, fov)
        s2.shift1D(barray)
        np.testing.assert_allclose(s2.data, s.data)

    @pytest.mark.skipif(
        hyperspy.__version__ == "1.6.2", reason="Broken with hyperspy 1.6.2"
    )
    def test_double_correct_grating_shift(self):
        s = CLSEMSpectrum(np.ones((10, 10, 10)))
        s.correct_grating_shift(1e-10, 1e-10, 1e-10)
        with pytest.raises(BaseException):
            s.correct_grating_shift(1, 1, 1)
