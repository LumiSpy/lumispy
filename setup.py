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

from setuptools import setup, find_packages

release_info = {}  # grab release info
with open("lumispy/release_info.py") as f:
    exec(f.read(), release_info)

with open("README.md") as f:  # grab readme
    long_description = f.read()

setup(
    name="lumispy",
    version=release_info["version"],
    description=release_info["description"],
    author=release_info["author"],
    license=release_info["license"],
    platforms=release_info["platforms"],
    url=release_info["url"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Software Development :: Libraries",
    ],
    keywords=release_info["keywords"],
    packages=find_packages(),
    # adjust the tabbing
    install_requires=[
        "hyperspy >= 1.7",  # earlier versions do not provide non-uniform axes
        "numpy",
        "scipy",
    ],
    extras_require={
        "tests": ["pytest>=5.0"],
        "coverage": ["pytest-cov", "codecov"],
        "build-doc": [
            "sphinx>=4.3.0",
            "sphinx_rtd_theme>=0.5.1",
            "sphinx-copybutton",
        ],
    },
    package_data={
        "lumispy": ["*.py", "hyperspy_extension.yaml"],
    },
    entry_points={"hyperspy.extensions": ["lumispy = lumispy"]},
    project_urls={  # Optional
        "Bug Reports": "https://github.com/lumispy/lumispy/issues",
        "Source": "https://github.com/lumispy/lumispy",
    },
)
