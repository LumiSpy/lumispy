# -*- coding: utf-8 -*-
# Copyright 2019 The LumiSpy developers
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
from numpy import ones

from lumispy.signals import LumiSpectrum, LumiTransient


class TestCommonLumi(TestCase):

    def test_crop_edges(self):
        s1 = LumiSpectrum(ones((10, 10, 10)))
        s2 = LumiTransient(ones((10, 10, 10, 10)))
        s3 = LumiSpectrum(ones((3, 3, 10)))
        s1 = s1.crop_edges(crop_px=2)
        s2 = s2.crop_edges(crop_px=2)
        assert s1.axes_manager.navigation_shape[0] == 6
        assert s1.axes_manager.navigation_shape[1] == 6
        assert s2.axes_manager.navigation_shape[0] == 6
        assert s2.axes_manager.navigation_shape[1] == 6
        self.assertRaises(ValueError, s3.crop_edges, crop_px=2)
