# -*- coding: utf-8 -*-
# Copyright 2019-2023 The LumiSpy developers
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
from hyperspy._signals.signal2d import Signal2D
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

        assert_allclose(
            s_copy.axes_manager.signal_axes[0].axis[0],
            368.614,
            atol=0.1,
        )
        assert_allclose(
            s_copy.axes_manager.signal_axes[0].axis[-1],
            768.249,
            atol=0.1,
        )
        assert_allclose(s.axes_manager.signal_axes[0].axis[0], 368.614, atol=0.1)
        assert_allclose(s.axes_manager.signal_axes[0].axis[-1], 768.249, atol=0.1)

    def test_center_of_mass(self):
        s = LumiSpectrum([1, 2, 3, 2, 1, 0])
        ax = s.axes_manager.signal_axes[0]
        ax.offset = 200
        ax.scale = 100
        ax.units = "nm"
        ax.name = "Wavelength"
        s.metadata.General.title = "test_signal"

        com = s.centroid()
        assert_allclose(com.data, 400.0, atol=0.1)
        assert (
            com.metadata.General.title
            == f"Centroid map of {ax.name} ({ax.units}) for test_signal"
        )

    def test_center_of_mass_signalrange(self):
        s = LumiSpectrum([100, 100, 1, 2, 3, 2, 1, 0, 100, 100])
        ax = s.axes_manager.signal_axes[0]
        ax.offset = 0
        ax.scale = 100
        ax.units = "nm"
        ax.name = "Wavelength"

        com = s.centroid(signal_range=(2, -2))
        assert_allclose(com.data, 400.0, atol=0.1)
        com = s.centroid(signal_range=(200.0, 800.0))
        assert_allclose(com.data, 400.0, atol=0.1)
        assert com.metadata.General.title == f"Centroid map of {ax.name} ({ax.units})"
        with pytest.raises(TypeError):
            s.centroid(signal_range=(1))
        with pytest.raises(TypeError):
            s.centroid(signal_range="string")
        with pytest.raises(ValueError):
            s.centroid(signal_range=(1, 2, 3))

    def test_centre_of_mass_3d(self):
        s = LumiSpectrum([[[1, 2, 3, 4, 5]] * 3] * 4)
        com = s.centroid()
        assert com.axes_manager.shape == (
            3,
            4,
        )
        assert com.metadata.General.title == f"Centroid map"
        assert type(com) == Signal2D
