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
import pytest

from inspect import getfullargspec

from lumispy.signals.cl_spectrum import CLSpectrum


param_list_signal_mask = [
    ([900, 500], [False, False, False, True, True, True, True, True, True, False]),
    (
        [[500, 100], [700, 1]],
        [False, True, True, False, True, False, False, False, False, False],
    ),
    (
        [[200, 100], [600, 300]],
        [True, True, True, True, True, False, False, False, False, False],
    ),
]


class TestCLSpectrum:
    def test__make_signal_mask(self):
        s = CLSpectrum(np.ones(10))
        s.axes_manager.signal_axes[0].scale = 100.5
        s.axes_manager.signal_axes[0].offset = 300
        for peak_list, mask_test in param_list_signal_mask:
            mask = s._make_signal_mask(peak_list)
            np.testing.assert_allclose(mask, mask_test)

    def test_remove_spikes(self):
        s = CLSpectrum(np.ones((2, 3, 30)))
        np.random.seed(1)
        s.add_gaussian_noise(1e-5)
        # Add three spikes
        s.data[1, 0, 1] += 2
        s.data[0, 2, 29] += 1

        if not "threshold" in getfullargspec(s.spikes_removal_tool)[0]:
            try:
                s.remove_spikes()
            except ImportError:
                pytest.skip("HyperSpy version doesn't support spike removal.")

        with pytest.raises(AttributeError):
            s.remove_spikes(luminescence_roi=[1], signal_mask=[1])

        with pytest.warns(UserWarning, match="Threshold value: 1.00"):
            s1 = s.remove_spikes()

        np.testing.assert_almost_equal(s1.data[1, 0, 1], 1, decimal=5)
        np.testing.assert_almost_equal(s1.data[0, 2, 29], 1, decimal=5)

        lum_roi = [1, 1]
        s4 = s.remove_spikes(luminescence_roi=lum_roi, threshold=0.5)
        np.testing.assert_almost_equal(s4.data[1, 0, 1], 3, decimal=5)
        np.testing.assert_almost_equal(s4.data[0, 2, 29], 1, decimal=5)

        s.remove_spikes(inplace=True, threshold=0.5)
        np.testing.assert_almost_equal(s.data[1, 0, 1], 1, decimal=5)
        np.testing.assert_almost_equal(s.data[0, 2, 29], 1, decimal=5)
        # TODO: test if histogram is shown as a plot if show_diagnosis_histogram=True.
