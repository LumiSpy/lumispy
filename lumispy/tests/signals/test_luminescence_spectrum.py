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

from lumispy.signals.luminescence_spectrum import LumiSpectrum
from numpy.testing import assert_allclose

backgrounds = [
    ([np.ones(50)], [np.zeros(50, dtype="float64")]),
    (
        [np.linspace(0, 49, num=50, dtype="float64"), np.ones(50)],
        [np.zeros(50, dtype="float64")],
    ),
    (
        [np.linspace(0, 50, num=30, dtype="float64"), np.ones(30)],
        [np.zeros(50, dtype="float64")],
    ),
    (LumiSpectrum(np.ones(50)), [np.zeros(50, dtype="float64")]),
]


class TestLumiSpectrum:
    def test_remove_background_from_file(self):
        for bkg, output in backgrounds:
            s = LumiSpectrum(np.ones(50))
            s2 = s.remove_background_from_file(bkg, inplace=False)
            s.remove_background_from_file(bkg, inplace=True)
            assert np.allclose(s.data, output)
            assert np.allclose(s2.data, output)
            assert s.metadata.Signal.background_subtracted is True
            assert hasattr(s.metadata.Signal, "background")

    def test_errors_raise(self):
        s = LumiSpectrum(np.ones(50))
        with pytest.raises(AttributeError):
            bkg = np.array([[1, 1], [1, 1], [1, 1]])
            s.remove_background_from_file(bkg)
        # Test that a GUI is opened if s.remove_background_from_file is passed without a background
        # s.remove_background_from_file()
        # Test double background removal
        s.remove_background_from_file(backgrounds[0][0], inplace=True)
        with pytest.raises(RecursionError):
            s.remove_background_from_file(backgrounds[0][0])

    def test_warnings(self):
        pytest.importorskip("hyperspy_gui_ipywidgets")
        s = LumiSpectrum(np.ones(50))
        with pytest.warns(SyntaxWarning, match="Using the Hyperspy"):
            s.remove_background_from_file(background=None, display=False)

    def test_deprecation_warning(self):
        s = LumiSpectrum(np.ones(50))
        with pytest.warns(DeprecationWarning, match="deprecated"):
            s.remove_background_from_file(background=backgrounds[0][0])

    def test_px_to_nm_grating_solver(self):
        s = LumiSpectrum(np.ones(10))
        ax = s.axes_manager.signal_axes[0]
        ax.offset = 200
        ax.scale = 10

        s_copy = s.px_to_nm_grating_solver(
            3,
            -20,
            300,
            25,
            600,
            150,
        )
        s.px_to_nm_grating_solver(3, -20, 300, 25, 600, 150, inplace=True)

        assert s_copy.axes_manager.signal_axes[0].name == "Wavelength"
        assert s_copy.axes_manager.signal_axes[0].units == "nm"
        assert s.axes_manager.signal_axes[0].name == "Wavelength"
        assert s.axes_manager.signal_axes[0].units == "nm"

        assert_allclose(s_copy.axes_manager.signal_axes[0].axis[0], 368.614, atol=0.1)
        assert_allclose(s_copy.axes_manager.signal_axes[0].axis[-1], 768.249, atol=0.1)
        assert_allclose(s.axes_manager.signal_axes[0].axis[0], 368.614, atol=0.1)
        assert_allclose(s.axes_manager.signal_axes[0].axis[-1], 768.249, atol=0.1)
