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


import functools
from importlib.metadata import version
from pathlib import Path


@functools.cache
def _get_version():
    version_ = version("hyperspy")
    # For development version, `setuptools_scm` will be used at build time
    # to get the dev version, in case of missing vcs information (git archive,
    # shallow repository), the fallback version defined in pyproject.toml will
    # be used

    # if we have a editable install from a git repository try to use
    # `setuptools_scm` to find a more accurate version:
    # `importlib.metadata` will provide the version at installation
    # time and for editable version this may be different

    # we only do that if we have enough git history, e.g. not shallow checkout
    _root = Path(__file__).resolve().parents[1]
    if (_root / ".git").exists() and not (_root / ".git/shallow").exists():
        try:
            # setuptools_scm may not be installed
            from setuptools_scm import get_version

            version_ = get_version(_root)
        except ImportError:  # pragma: no cover
            # setuptools_scm not install, we keep the existing __version__
            pass

    return version_


__version__ = _get_version()
