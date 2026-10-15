# -*- coding: utf-8 -*-
# Copyright 2019-2026 The LumiSpy developers

from inspect import signature
import numpy as np
import pytest
import lumispy as lum


def test_AlN_example_data():
    s = lum.data.AlN_Cornell()
    bkg = lum.data.AlN_bkg()
    axis = s.axes_manager.signal_axes[0].axis
    assert isinstance(s, lum.signals.LumiSpectrum)
    assert isinstance(bkg, lum.signals.LumiSpectrum)
    assert s.axes_manager.navigation_dimension == 2
    assert s.axes_manager.signal_axes[0].size == 2048
    assert not s.axes_manager.signal_axes[0].is_uniform
    assert s.axes_manager.signal_axes[0].units == "nm"
    np.testing.assert_array_equal(axis, bkg.axes_manager.signal_axes[0].axis)
    np.testing.assert_allclose(axis[[0, -1]], [107.22683715820312, 852.1829223632812])
    assert np.isfinite(s.data).all()
    assert np.isfinite(bkg.data).all()
    assert np.isfinite(s.data - bkg.data).all()


def test_AlN_background_removal():
    s = lum.data.AlN_Cornell()
    bkg = lum.data.AlN_bkg()

    s = s.mean(axis=(0, 1))

    if "background_signal" not in signature(s.remove_background).parameters:
        pytest.skip("Scalable fixed pattern requires HyperSpy >= 2.5.0")
    corrected = s.remove_background(
        signal_range="full",
        background_type="Scalable fixed pattern",
        background_signal=bkg,
        yscale=False,
    )
    np.testing.assert_allclose(corrected.data, s.data - bkg.data, atol=1e-7)
    np.testing.assert_allclose(s.data[0], 298.51)
