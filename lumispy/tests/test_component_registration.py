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

import inspect
from uuid import UUID

import lumispy.components as lumispy_components
import pytest
from hyperspy.component import Component
from hyperspy.extensions import ALL_EXTENSIONS


def _public_component_classes():
    """Return every component registered in lumispy.components.__all__."""
    component_classes = []

    for name in lumispy_components.__all__:
        obj = getattr(lumispy_components, name)

        assert inspect.isclass(obj), f"`{name}` is not a class."

        assert issubclass(obj, Component), (
            f"`{name}` is not a HyperSpy Component subclass."
        )

        component_classes.append(obj)

    return component_classes


def _registered_lumispy_components():
    """
    Return all LumiSpy components that are registered in HyperSpy and are loaded.
    """
    registered = {}
    package_name = lumispy_components.__name__

    for component_group in ("components1D", "components2D"):
        for component_id, specification in ALL_EXTENSIONS.get(
            component_group, {}
        ).items():
            module = specification["module"]

            is_lumispy_component = module == package_name or module.startswith(
                f"{package_name}."
            )

            if not is_lumispy_component:
                continue

            key = (module, specification["class"])

            assert key not in registered, (
                f"{specification['class']} is registered more than once in HyperSpy extensions."
            )

            registered[key] = (component_group, component_id)

    return registered


def test_component_registration():
    public_components = _public_component_classes()

    expected = {
        (component_class.__module__, component_class.__name__)
        for component_class in public_components
    }

    registered = _registered_lumispy_components()
    registered_keys = set(registered.keys())

    missing_registrations = expected - registered_keys
    obsolete_registrations = registered_keys - expected

    assert not missing_registrations, (
        "These LumiSpy components are missing from "
        "`hyperspy_extension.yaml`:\n"
        + "\n".join(
            f"  - {module}.{class_name}"
            for module, class_name in sorted(missing_registrations)
        )
    )

    assert not obsolete_registrations, (
        "These components are registered in `hyperspy_extension.yaml` but "
        "are not exported by `lumispy.components.__all__`:\n"
        + "\n".join(
            f"  - {module}.{class_name}"
            for module, class_name in sorted(obsolete_registrations)
        )
    )


@pytest.mark.parametrize(
    "component_class",
    _public_component_classes(),
    ids=lambda component_class: component_class.__name__,
)
def test_component_uuid(component_class):
    registered = _registered_lumispy_components()

    component_key = (
        component_class.__module__,
        component_class.__name__,
    )

    _, registered_id = registered[component_key]

    component = component_class()

    assert component._id_name == registered_id
    assert UUID(component._id_name).version == 4
