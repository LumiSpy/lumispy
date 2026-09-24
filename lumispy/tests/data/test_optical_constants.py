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

from importlib.resources import files

import numpy as np
from numpy.testing import assert_allclose
import pytest

from hyperspy.signals import ComplexSignal1D

from lumispy.data import load_optical_constants, supported_optical_constants


def _packaged_optical_constants():
    directory = files("lumispy.data").joinpath("optical_constants")
    suffix = ".hspy"

    return tuple(
        sorted(
            resource.name.removesuffix(suffix)
            for resource in directory.iterdir()
            if resource.is_file() and resource.name.endswith(suffix)
        )
    )


def test_supported_optical_constants_matches_packaged_files():
    packaged = _packaged_optical_constants()

    assert packaged
    assert supported_optical_constants() == packaged


@pytest.mark.parametrize("name", supported_optical_constants())
def test_load_optical_constants(name):
    signal = load_optical_constants(name)
    axis = signal.axes_manager.signal_axes[0]
    metadata = signal.metadata.OpticalConstants

    assert isinstance(signal, ComplexSignal1D)
    assert signal.axes_manager.navigation_dimension == 0
    assert signal.axes_manager.signal_dimension == 1
    assert signal.data.ndim == 1
    assert signal.data.size > 1
    assert np.iscomplexobj(signal.data)
    assert np.all(np.isfinite(signal.data.real))
    assert np.all(np.isfinite(signal.data.imag))

    assert axis.navigate is False
    assert axis.size == signal.data.size
    assert np.all(np.isfinite(axis.axis))
    assert np.all(axis.axis > 0)
    assert np.all(np.diff(axis.axis) > 0)

    for item in (
        "material",
        "reference",
        "spectral_variable",
        "spectral_unit",
        "data_kind",
    ):
        value = getattr(metadata, item)
        assert isinstance(value, str)
        assert value

    assert axis.name == metadata.spectral_variable
    assert axis.units == metadata.spectral_unit
    assert signal.metadata.Signal.quantity
    assert signal.metadata.General.title


def test_load_optical_constants_accepts_hspy_suffix():
    names = supported_optical_constants()
    assert names
    name = names[0]

    without_suffix = load_optical_constants(name)
    with_suffix = load_optical_constants(f"{name}.hspy")

    assert_allclose(with_suffix.data, without_suffix.data)
    assert_allclose(
        with_suffix.axes_manager.signal_axes[0].axis,
        without_suffix.axes_manager.signal_axes[0].axis,
    )


def test_load_unknown_optical_constants_raises():
    missing_name = "__missing_optical_constants__"
    available = supported_optical_constants()
    assert missing_name not in available

    with pytest.raises(ValueError, match="Unknown optical constants") as error:
        load_optical_constants(missing_name)

    for name in available:
        assert repr(name) in str(error.value)
