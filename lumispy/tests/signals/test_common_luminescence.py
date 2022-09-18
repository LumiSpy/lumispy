# -*- coding: utf-8 -*-
# Copyright 2019-2022 The LumiSpy developers
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
from pytest import raises, mark, skip, warns
from warnings import WarningMessage
from lumispy.signals import LumiSpectrum, LumiTransientSpectrum


class TestCommonLumi:
    @mark.parametrize(("crop_range, output"), ((2, (6,6)), ((2,4), (6,2)), ((1,2,3,4), (6,4)), ((1,2,3), ()), ((1,2,3,4,5), ()), ('s', ()),))
    def test_crop_edges(crop_range, output):
        s1 = LumiSpectrum(np.ones((10, 10, 10)))
        s2 = LumiTransientSpectrum(np.ones((10, 10, 10, 10)))
        
        # Check for bad input range
        if type(crop_range) not in (int, float, tuple):
            with raises(ValueError, match='value must be a number or a tuple'):
                s1.crop_edges(crop_range)

        elif type(crop_range) == tuple:
            if len(crop_range) not in (1,2,4):
                with raises(ValueError, match='tuple must be either a'):
                    s1.crop_edges(crop_range)

        else:
            s1 = s1.crop_edges(crop_range)
            assert s1.axes_manager.navigation_shape[0] == output[0] 
            assert s1.axes_manager.navigation_shape[1] == output[1]

    def test_crop_percent():
        s1 = LumiSpectrum(np.ones((10, 10, 10)))
        s2 = s1.crop_edges(crop_range= 0.1, crop_units='percent')
        assert s1.axes_manager.navigation_shape[0] == 8
        assert s2.axes_manager.navigation_shape[1] == 8

    @mark.parametrize(("crop_units"), ('pixel', 'px', 'PIXEL', 'percent', '%', 'nm'))
    def test_crop_edges_units(crop_units):
        s1 = LumiSpectrum(np.ones((10, 10, 10)))

        # Check for bad units
        if crop_units.lower() not in ('px', 'pixel', 'percent', '%'):
            with raises(ValueError, match='crop_units only accepts'):
                s1.crop_edges(crop_range=1, crop_units=crop_units)
    
    def test_crop_edges_metadata():
        s1 = LumiSpectrum(np.ones((10, 10, 10)))
        s1 = s1.crop_edges(crop_range=2)
        assert s1.metadata.Signal.cropped_edges == (2,2,2,2)
        s1 = s1.crop_edges(crop_range=2)
        assert s1.metadata.Signal.cropped_edges == (4,4,4,4)

    def test_crop_edges_too_far():
        s1 = LumiSpectrum(np.ones((10, 10, 10)))
        with warns(WarningMessage, match="The pixels to"):
            s1 = s1.crop_edges(crop_range=6)
            assert s1.axes_manager.navigation_shape[0] == 0

    def test_remove_negative(self):
        s1 = LumiSpectrum(np.random.random((10, 10, 10))) - 0.3
        s2 = LumiTransientSpectrum(np.random.random((10, 10, 10, 10))) - 0.3
        s3 = LumiTransientSpectrum(np.random.random((10, 10, 10, 10))) - 0.3
        s1a = s1.remove_negative(inplace=False)
        s2a = s2.remove_negative(inplace=False)
        s3a = s3.remove_negative(basevalue=0.1)
        assert s3a.metadata.Signal.negative_removed == True
        assert np.all(s1a.data[s1 <= 0] == 1)
        assert np.all(s2a.data[s2 <= 0] == 1)
        assert np.all(s3a.data[s3 <= 0] == 0.1)
        s1.remove_negative(inplace=True)
        s2.remove_negative(inplace=True)
        s3.remove_negative(basevalue=0.1, inplace=True)
        assert s1 == s1a
        assert s2 == s2a
        assert s3 == s3a

    def test_scale_by_exposure(self):
        s1 = LumiSpectrum(np.ones((10, 10, 10)))
        s2 = LumiTransientSpectrum(np.ones((10, 10, 10, 10)))
        s4 = LumiSpectrum(np.ones((10)))
        s2.metadata.set_item("Acquisition_instrument.Detector.integration_time", 2)
        s2.metadata.set_item("Signal.quantity", "Intensity (Counts)")
        s4.metadata.set_item("Signal.quantity", "Intensity (counts)")
        s1a = s1.scale_by_exposure(integration_time=4)
        s2a = s2.scale_by_exposure()
        s4a = s4.scale_by_exposure(integration_time=0.1)
        assert np.all(s1a.data == 0.25)
        assert np.all(s2a.data == 0.5)
        assert np.all(s4a.data == 10)
        assert s2a.metadata.Signal.quantity == "Intensity (Counts/s)"
        assert s4a.metadata.Signal.quantity == "Intensity (counts/s)"
        assert s4a.metadata.Signal.scaled == True
        s1.scale_by_exposure(integration_time=4, inplace=True)
        s2.scale_by_exposure(inplace=True)
        s4.scale_by_exposure(integration_time=0.1, inplace=True)
        assert s1 == s1a
        assert s2 == s2a
        assert s4 == s4a
        assert s2.metadata.Signal.quantity == "Intensity (Counts/s)"
        assert s4.metadata.Signal.quantity == "Intensity (counts/s)"
        # Test for errors
        s4 = LumiSpectrum(np.ones((10)))
        s4.normalize(inplace=True)
        with raises(AttributeError, match="Data was normalized and"):
            s4.scale_by_exposure(inplace=True, integration_time=0.5)
        s5 = LumiSpectrum(np.ones((10)))
        with raises(AttributeError, match="not included in the"):
            s5.scale_by_exposure(inplace=True)
        s5.scale_by_exposure(inplace=True, integration_time=0.5)
        with raises(AttributeError, match="Data was already scaled."):
            s5.scale_by_exposure(inplace=True, integration_time=0.5)
        # Deprecation test for exposure argument
        s6 = LumiSpectrum(np.ones((10)))
        with warns(DeprecationWarning, match="removed in LumiSpy 1.0"):
            s6.scale_by_exposure(inplace=True, exposure=0.5)
            assert np.all(s6.data == 2)

    def test_normalize(self):
        s1 = LumiSpectrum(np.random.random((10, 10, 10))) * 2
        s2 = LumiTransientSpectrum(np.random.random((10, 10, 10, 10))) * 2
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
        with warns(UserWarning, match="Data was"):
            s1.normalize(inplace=True)
