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

error_backgrounds = [
    ([np.linspace(0, 49, num=10, dtype="float64"), np.ones(50)], AttributeError),
    ([[1, 1], [1, 1], [1, 1]], AttributeError),
    # ([np.linspace(0, 48, num=10, dtype="float64"), np.ones(50)], AttributeError),
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
        for bkg, error in error_backgrounds:
            with pytest.raises(error):
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
