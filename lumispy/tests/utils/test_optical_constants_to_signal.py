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

from hyperspy.signals import ComplexSignal1D

from lumispy.utils import optical_constants_to_signal


def _common_dataset(**kwargs):
    dataset = {
        "layout": "combined_n_k",
        "representation": "n_k",
        "file": "optical_constants.txt",
        "loadfile_kwargs": {},
        "coordinate": "wavelength",
        "coordinate_units": "µm",
        "coordinate_column": 0,
        "n_column": 1,
        "k_column": 2,
        "material": "Test material",
        "reference": "Test reference",
    }
    dataset.update(kwargs)
    return dataset


def _assert_signal(
    signal,
    expected_axis,
    expected_data,
    *,
    data_kind,
    quantity,
    axis_name="wavelength",
    axis_units="µm",
):
    axis = signal.axes_manager.signal_axes[0]

    assert isinstance(signal, ComplexSignal1D)
    assert signal.axes_manager.navigation_dimension == 0
    assert signal.axes_manager.signal_dimension == 1
    assert axis.navigate is False
    assert axis.name == axis_name
    assert axis.units == axis_units
    assert_allclose(axis.axis, expected_axis)
    assert_allclose(signal.data, expected_data)

    metadata = signal.metadata.OpticalConstants
    assert metadata.material == "Test material"
    assert metadata.reference == "Test reference"
    assert metadata.spectral_variable == axis_name
    assert metadata.spectral_unit == axis_units
    assert metadata.data_kind == data_kind
    assert signal.metadata.Signal.quantity == quantity
    assert signal.metadata.General.title == (
        f"Test material {quantity.lower()} - Test reference"
    )


def test_combined_n_and_k_are_converted_to_signal(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    np.savetxt(
        "optical_constants.txt",
        [
            [0.7, 2.0, 0.7, 0.2],
            [0.5, 1.5, 0.5, 0.1],
        ],
    )
    dataset = _common_dataset(k_coordinate_column=2, k_column=3)

    signal = optical_constants_to_signal(dataset)

    _assert_signal(
        signal,
        expected_axis=[0.5, 0.7],
        expected_data=[1.5 + 0.1j, 2.0 + 0.2j],
        data_kind="complex_refractive_index",
        quantity="Complex refractive index",
    )


def test_separate_n_and_k_are_converted_to_signal(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    np.savetxt("n.txt", [[0.7, 2.0], [0.5, 1.5]])
    np.savetxt("k.txt", [[0.7, 0.2], [0.5, 0.1]])
    dataset = _common_dataset(
        layout="separate_n_k",
        n_file="n.txt",
        k_file="k.txt",
        k_column=1,
    )

    signal = optical_constants_to_signal(dataset)

    _assert_signal(
        signal,
        expected_axis=[0.5, 0.7],
        expected_data=[1.5 + 0.1j, 2.0 + 0.2j],
        data_kind="complex_refractive_index",
        quantity="Complex refractive index",
    )


def test_combined_permittivity_is_converted_to_signal(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    np.savetxt(
        "optical_constants.txt",
        [
            [3.0, -2.0, 0.4],
            [1.0, -4.0, 0.2],
        ],
    )
    dataset = _common_dataset(
        layout="combined_epsilon",
        representation="epsilon",
        coordinate="Photon energy",
        coordinate_units="eV",
        real_column=1,
        imaginary_column=2,
    )

    signal = optical_constants_to_signal(dataset)

    _assert_signal(
        signal,
        expected_axis=[1.0, 3.0],
        expected_data=[-4.0 + 0.2j, -2.0 + 0.4j],
        data_kind="relative_permittivity",
        quantity="Relative permittivity",
        axis_name="Photon energy",
        axis_units="eV",
    )


def test_unknown_layout_raises():
    dataset = _common_dataset(layout="unknown")

    with pytest.raises(ValueError, match="Unknown dataset layout 'unknown'"):
        optical_constants_to_signal(dataset)


def test_missing_file_raises(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with pytest.raises(FileNotFoundError, match="missing.txt.*was not found"):
        optical_constants_to_signal(_common_dataset(file="missing.txt"))


def test_unreadable_table_raises(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "optical_constants.txt").write_text("not numeric", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="Could not load optical-constants file 'optical_constants.txt'",
    ):
        optical_constants_to_signal(_common_dataset())


def test_missing_configured_column_raises(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    np.savetxt("optical_constants.txt", [[0.5, 1.5], [0.7, 2.0]])

    with pytest.raises(ValueError, match="does not contain all configured columns"):
        optical_constants_to_signal(_common_dataset())


def test_separate_n_and_k_lengths_must_match(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    np.savetxt("n.txt", [[0.5, 1.5], [0.7, 2.0]])
    np.savetxt("k.txt", [[0.5, 0.1]])
    dataset = _common_dataset(
        layout="separate_n_k",
        n_file="n.txt",
        k_file="k.txt",
        k_column=1,
    )

    with pytest.raises(ValueError, match="different lengths"):
        optical_constants_to_signal(dataset)


def test_separate_n_and_k_coordinates_must_match(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    np.savetxt("n.txt", [[0.5, 1.5], [0.7, 2.0]])
    np.savetxt("k.txt", [[0.5, 0.1], [0.8, 0.2]])
    dataset = _common_dataset(
        layout="separate_n_k",
        n_file="n.txt",
        k_file="k.txt",
        k_column=1,
    )

    with pytest.raises(ValueError, match="different coordinate values"):
        optical_constants_to_signal(dataset)


def test_combined_n_and_k_coordinates_must_match(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    np.savetxt(
        "optical_constants.txt",
        [[0.5, 1.5, 0.5, 0.1], [0.7, 2.0, 0.8, 0.2]],
    )
    dataset = _common_dataset(k_coordinate_column=2, k_column=3)

    with pytest.raises(ValueError, match="different coordinate values"):
        optical_constants_to_signal(dataset)


@pytest.mark.parametrize(
    "data, match",
    [
        (
            [[0.0, 1.5, 0.1], [0.7, 2.0, 0.2]],
            "Coordinate values must be positive and finite",
        ),
        (
            [[np.nan, 1.5, 0.1], [0.7, 2.0, 0.2]],
            "Coordinate values must be positive and finite",
        ),
        (
            [[0.5, np.nan, 0.1], [0.7, 2.0, 0.2]],
            "first optical-data component contains non-finite values",
        ),
        (
            [[0.5, 1.5, np.inf], [0.7, 2.0, 0.2]],
            "second optical-data component contains non-finite values",
        ),
        (
            [[0.5, 1.5, 0.1], [0.5, 2.0, 0.2]],
            "Coordinate values must be strictly increasing",
        ),
    ],
)
def test_invalid_table_values_raise(data, match, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    np.savetxt("optical_constants.txt", data)

    with pytest.raises(ValueError, match=match):
        optical_constants_to_signal(_common_dataset())
