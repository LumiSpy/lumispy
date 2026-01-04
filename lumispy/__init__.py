# -*- coding: utf-8 -*-
# Copyright 2019-2025 The LumiSpy developers
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


import importlib

from importlib.metadata import version
from pathlib import Path
from typing import Any


# rresolve version
__version__ = version("lumispy")

# For development version, `setuptools_scm` will be used at build time
# to get the dev version, in case of missing vcs information (git archive,
# shallow repository), the fallback version defined in pyproject.toml will
# be used

# If we have an editable installed from a git repository try to use
# `setuptools_scm` to find a more accurate version:
# `importlib.metadata` will provide the version at installation
# time and for editable version this may be different

# we only do that if we have enough git history, e.g. not shallow checkout
_root = Path(__file__).resolve().parents[1]
if (_root / ".git").exists() and not (_root / ".git/shallow").exists():
    try:
        # setuptools_scm may not be installed
        from setuptools_scm import get_version

        __version__ = get_version(_root)
    except ImportError:  # pragma: no cover
        # setuptools_scm not install, we keep the existing __version__
        pass


__all__ = [
    "__version__",
    "components",
    "signals",
    "utils",
]


# Map exported names that will be resolved lazily
_lazy_modules = {
    "signals": "lumispy.signals",
    "components": "lumispy.components",
    "utils": "lumispy.utils",
}

# Map top-level utility names to their submodule and attribute name
_lazy_attributes = {
    # name: (module, attribute)
    "nm2eV": ("lumispy.utils.axes", "nm2eV"),
    "eV2nm": ("lumispy.utils.axes", "eV2nm"),
    "nm2invcm": ("lumispy.utils.axes", "nm2invcm"),
    "invcm2nm": ("lumispy.utils.axes", "invcm2nm"),
    "join_spectra": ("lumispy.utils.axes", "join_spectra"),
    "to_array": ("lumispy.utils.io", "to_array"),
    "savetxt": ("lumispy.utils.io", "savetxt"),
}


def __getattr__(name: str) -> Any:
    """Lazy-load subpackages and selected attributes on demand."""
    # Lazy subpackages
    if name in _lazy_modules:
        mod = importlib.import_module(_lazy_modules[name])
        globals()[name] = mod
        return mod

    # Lazy attributes (forward from submodules)
    if name in _lazy_attributes:
        mod_name, attr = _lazy_attributes[name]
        mod = importlib.import_module(mod_name)
        val = getattr(mod, attr)
        globals()[name] = val
        return val

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(list(__all__) + list(_lazy_attributes.keys()))
