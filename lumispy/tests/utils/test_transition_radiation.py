# -*- coding: utf-8 -*-
# Copyright 2019-2026 The LumiSpy developers
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
from numpy.testing import assert_allclose
import pytest

from hyperspy.axes import DataAxis
from hyperspy.signals import Signal1D, Signal2D

from lumispy.data import supported_optical_constants
from lumispy.utils.transition_radiation import (
    _HC_EV_NM,
    _interpolate_permittivity,
    _load_optical_data,
    transition_radiation_nm,
)


def test_transition_radiation_returns_calibrated_signals():
    wavelengths_nm = np.array([400.0, 550.0, 800.0])
    angles_deg = np.array([0.0, 30.0, 60.0, 90.0])

    spectrum, angle_resolved = transition_radiation_nm(
        electron_energy=30,
        material_dataset="Al_mcpeak",
        angular_axis=angles_deg,
        spectral_axis=wavelengths_nm,
        return_angle_resolved=True,
    )

    assert isinstance(spectrum, Signal1D)
    assert isinstance(angle_resolved, Signal2D)
    assert spectrum.data.shape == (wavelengths_nm.size,)
    assert angle_resolved.data.shape == (angles_deg.size, wavelengths_nm.size)

    spectrum_axis = spectrum.axes_manager.signal_axes[0]
    angle_resolved_axes = {
        axis.name: axis for axis in angle_resolved.axes_manager.signal_axes
    }
    assert spectrum_axis.name == "Wavelength"
    assert spectrum_axis.units == "nm"
    assert_allclose(spectrum_axis.axis, wavelengths_nm)
    assert angle_resolved_axes["Angle"].units == "deg"
    assert_allclose(angle_resolved_axes["Angle"].axis, angles_deg)
    assert_allclose(
        angle_resolved_axes["Wavelength"].axis,
        wavelengths_nm,
    )

    assert spectrum.metadata.Transition_radiation.electron_energy_keV == 30
    assert angle_resolved.metadata.Transition_radiation.material_dataset == "Al_mcpeak"
    assert np.all(np.isfinite(spectrum.data))
    assert np.all(np.isfinite(angle_resolved.data))
    assert np.all(spectrum.data >= 0)
    assert np.all(angle_resolved.data >= 0)


@pytest.mark.parametrize("material_dataset", supported_optical_constants())
def test_all_bundled_optical_datasets(material_dataset):
    spectrum = transition_radiation_nm(
        material_dataset=material_dataset,
        angular_axis=(0, 90, 181),
        spectral_axis=[400.0, 600.0, 800.0],
    )

    assert spectrum.data.shape == (3,)
    assert np.all(np.isfinite(spectrum.data))
    assert np.all(spectrum.data >= 0)


def test_palik_data_are_used_as_permittivity():
    optical_data = _load_optical_data("Au_palik")
    optical_energy_ev = optical_data.axes_manager.signal_axes[0].axis
    index = optical_energy_ev.size // 2
    wavelength_nm = _HC_EV_NM / optical_energy_ev[index : index + 1]

    interpolated = _interpolate_permittivity(
        wavelength_nm,
        optical_data,
    )

    expected = optical_data.data[index]
    assert optical_data.metadata.OpticalConstants.data_kind == "relative_permittivity"
    assert_allclose(interpolated, expected, rtol=1e-13, atol=0)
    assert not np.isclose(interpolated[0], expected**2)


def test_n_and_k_data_are_converted_to_permittivity():
    optical_data = _load_optical_data("Au_johnson")
    optical_wavelength_um = optical_data.axes_manager.signal_axes[0].axis
    index = optical_wavelength_um.size // 2
    wavelength_nm = optical_wavelength_um[index : index + 1] * 1e3

    interpolated = _interpolate_permittivity(
        wavelength_nm,
        optical_data,
    )

    expected = optical_data.data[index] ** 2
    assert (
        optical_data.metadata.OpticalConstants.data_kind == "complex_refractive_index"
    )
    assert_allclose(interpolated, expected, rtol=1e-13, atol=0)


def test_optical_constants_signal_is_accepted():
    optical_data = _load_optical_data("Al_mcpeak")

    spectrum = transition_radiation_nm(
        material_dataset=optical_data,
        angular_axis=(0, 90, 181),
        spectral_axis=[400.0, 600.0, 800.0],
    )

    assert spectrum.data.shape == (3,)
    assert np.all(np.isfinite(spectrum.data))
    assert np.all(spectrum.data >= 0)


def test_hyperspy_axes_are_accepted():
    angular_axis = DataAxis(axis=np.linspace(0, 90, 91))
    spectral_axis = DataAxis(axis=np.array([400.0, 600.0, 800.0]))

    spectrum = transition_radiation_nm(
        angular_axis=angular_axis,
        spectral_axis=spectral_axis,
    )

    assert_allclose(
        spectrum.axes_manager.signal_axes[0].axis,
        spectral_axis.axis,
    )


@pytest.mark.parametrize(
    "kwargs, error, match",
    [
        (
            {"angular_axis": (90, 0)},
            ValueError,
            "strictly increasing",
        ),
        (
            {"material_dataset": "not-a-dataset"},
            ValueError,
            "Unknown optical constants",
        ),
        (
            {"material_dataset": np.array([1, 2])},
            TypeError,
            "must be a string or a ComplexSignal1D",
        ),
    ],
)
def test_invalid_arguments(kwargs, error, match):
    with pytest.raises(error, match=match):
        transition_radiation_nm(**kwargs)


def test_spectral_extrapolation_warns():
    with pytest.warns(UserWarning, match="beyond the available optical data"):
        spectrum = transition_radiation_nm(
            material_dataset="Au_sc",
            spectral_axis=(150, 1200),
        )

    assert spectrum.data.shape == (200,)
    assert np.all(np.isfinite(spectrum.data))
