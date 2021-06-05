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

import numpy as np
from unittest import TestCase
from pytest import raises, warns

from lumispy.signals import LumiSpectrum, LumiTransient


class TestCommonLumi(TestCase):
    def test_crop_edges(self):
        s1 = LumiSpectrum(np.ones((10, 10, 10)))
        s2 = LumiTransient(np.ones((10, 10, 10, 10)))
        s3 = LumiSpectrum(np.ones((3, 3, 10)))
        s1 = s1.crop_edges(crop_px=2)
        s2 = s2.crop_edges(crop_px=2)
        assert s1.axes_manager.navigation_shape[0] == 6
        assert s1.axes_manager.navigation_shape[1] == 6
        assert s2.axes_manager.navigation_shape[0] == 6
        assert s2.axes_manager.navigation_shape[1] == 6
        self.assertRaises(ValueError, s3.crop_edges, crop_px=2)

    def test_remove_negative(self):
        s1 = LumiSpectrum(np.random.random((10, 10, 10))) - 0.3
        s2 = LumiTransient(np.random.random((10, 10, 10, 10))) - 0.3
        s3 = LumiTransient(np.random.random((10, 10, 10, 10))) - 0.3
        s1a = s1.remove_negative(inplace=False)
        s2a = s2.remove_negative(inplace=False)
        s3a = s3.remove_negative(inplace=False, basevalue=0.1)
        assert s3a.metadata.Signal.negative_removed == True
        assert np.all(s1a.data[s1 <= 0] == 1)
        assert np.all(s2a.data[s2 <= 0] == 1)
        assert np.all(s3a.data[s3 <= 0] == 0.1)
        s1.remove_negative(inplace=True)
        s2.remove_negative(inplace=True)
        s3.remove_negative(basevalue=0.1)
        assert s1 == s1a
        assert s2 == s2a
        assert s3 == s3a

    def test_scale_by_exposure(self):
        s1 = LumiSpectrum(np.ones((10, 10, 10)))
        s2 = LumiTransient(np.ones((10, 10, 10, 10)))
        s3 = LumiSpectrum(np.ones((10, 10)))
        s4 = LumiSpectrum(np.ones((10)))
        s2.metadata.set_item("Acquisition_instrument.CL.exposure", 2)
        s3.metadata.set_item("Acquisition_instrument.CL.dwell_time", 0.5)
        s3.metadata.set_item("Signal.quantity", "Intensity (Counts)")
        s4.metadata.set_item("Signal.quantity", "Intensity (counts)")
        s1a = s1.scale_by_exposure(exposure=4)
        s2a = s2.scale_by_exposure()
        s3a = s3.scale_by_exposure()
        s4a = s4.scale_by_exposure(exposure=0.1)
        assert np.all(s1a.data == 0.25)
        assert np.all(s2a.data == 0.5)
        assert np.all(s3a.data == 2)
        assert np.all(s4a.data == 10)
        assert s3a.metadata.Signal.quantity == "Intensity (Counts/s)"
        assert s4a.metadata.Signal.quantity == "Intensity (counts/s)"
        assert s4a.metadata.Signal.scaled == True
        s1.scale_by_exposure(exposure=4, inplace=True)
        s2.scale_by_exposure(inplace=True)
        s3.scale_by_exposure(inplace=True)
        s4.scale_by_exposure(exposure=0.1, inplace=True)
        assert s1 == s1a
        assert s2 == s2a
        assert s3 == s3a
        assert s4 == s4a
        assert s3.metadata.Signal.quantity == "Intensity (Counts/s)"
        assert s4.metadata.Signal.quantity == "Intensity (counts/s)"
        # Test for errors
        s4 = LumiSpectrum(np.ones((10)))
        s4.normalize(inplace=True)
        with raises(AttributeError) as excinfo:
            s4.scale_by_exposure(inplace=True, exposure=0.5)
        assert str(excinfo.value) == "Data was normalized and cannot be " "scaled."
        s5 = LumiSpectrum(np.ones((10)))
        with raises(AttributeError) as excinfo:
            s5.scale_by_exposure(inplace=True)
        assert (
            str(excinfo.value) == "Exposure not given and can not be "
            "extracted automatically from metadata."
        )
        s5.scale_by_exposure(inplace=True, exposure=0.5)
        with raises(AttributeError) as excinfo:
            s5.scale_by_exposure(inplace=True, exposure=0.5)
        assert str(excinfo.value) == "Data was already scaled."

    def test_normalize(self):
        s1 = LumiSpectrum(np.random.random((10, 10, 10))) * 2
        s2 = LumiTransient(np.random.random((10, 10, 10, 10))) * 2
        s3 = LumiSpectrum(np.random.random((10, 10))) * 2
        s4 = LumiSpectrum(np.random.random((10))) * 2
        s4.metadata.set_item("Signal.quantity", "Intensity (counts)")
        s1a = s1.normalize()
        s2a = s2.normalize()
        s3a = s3.normalize()
        s4a = s4.normalize()
        assert s1a.max(axis=[0, 1, 2]).data[0] == 1
        assert s2a.max(axis=[0, 1, 2, 3]).data[0] == 1
        assert s3a.max(axis=[0, 1]).data[0] == 1
        assert s4a.max(axis=[0]).data[0] == 1
        assert s4a.metadata.Signal.quantity == "Normalized intensity"
        assert s4a.metadata.Signal.normalized == True
        s1a = s1.normalize(element_wise=True)
        s2a = s2.normalize(element_wise=True)
        s3a = s3.normalize(element_wise=True)
        s4a = s4.normalize(element_wise=True)
        assert np.all(s1a.max(axis=[2]).data[0] == 1)
        assert np.all(s2a.max(axis=[3]).data[0] == 1)
        assert np.all(s3a.max(axis=[1]).data[0] == 1)
        assert s4a.max(axis=[0]).data[0] == 1
        s1a = s1.normalize(pos=3)
        s2a = s2.normalize(pos=3, element_wise=True)
        s3a = s3.normalize(pos=3, element_wise=True)
        s4a = s4.normalize(pos=3)
        assert s1a.isig[3].max().data[0] == 1
        assert np.all(s2a.isig[3] == 1)
        assert np.all(s3a.isig[3] == 1)
        assert s4a.isig[3].data == 1
        s1.normalize(pos=3, inplace=True)
        s2.normalize(pos=3, element_wise=True, inplace=True)
        s3.normalize(pos=3, element_wise=True, inplace=True)
        s4.normalize(pos=3, inplace=True)
        assert s1a == s1
        assert s2a == s2
        assert s3a == s3
        assert s4a == s4
        assert s4.metadata.Signal.quantity == "Normalized intensity"
        with warns(UserWarning) as warninfo:
            s1.normalize(inplace=True)
        assert len(warninfo) == 1
        assert warninfo[0].message.args[0][:8] == "Data was"
