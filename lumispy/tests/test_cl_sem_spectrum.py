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

from unittest import TestCase
from numpy import allclose, arange, full, ones
from numpy.random import random

from lumispy.signals import CLSEMSpectrum

param_list = [(1e-10, 1e-10, 1e-10, 10, 10),
              (1e-10, 1e-10, 1e-10, 20, 10),
              (1e-10, 1e-10, 1e-10, 10, 20),]


class TestCLSEMSpectrum(TestCase):

    def test_correct_grating_shift(self):
        for calx, corg, fov, nx, ny in param_list:
            with self.subTest():
                s = CLSEMSpectrum(ones((nx, ny, 100)) * random())
                garray = arange((-corg / 2) * calx / (fov * nx) * 1000 * nx,
                                   (corg / 2) * calx / (fov * nx) * 1000 * nx,
                                   corg * calx / (fov * nx) * 1000)
                barray = full((ny, nx), garray)
                s2 = s.deepcopy()
                s.correct_grating_shift(calx, corg, fov)
                s2.shift1D(barray)
                assert allclose(s2.data, s.data)

    def test_double_correct_grating_shift(self):
        s = CLSEMSpectrum(ones((10, 10, 10)))
        s.correct_grating_shift(1e-10, 1e-10, 1e-10)
        self.assertRaises(Exception, s.correct_grating_shift, 1, 1, 1)

