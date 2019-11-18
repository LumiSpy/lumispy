#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2019 The hyperspy_cl developers
#
# This file is part of hyperspy_cl.
#
# hyperspy_cl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# hyperspy_cl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with hyperspy_cl.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

exec(open('hyperspy_cl/release_info.py').read())  # grab version info


setup(
    name=name,
    version=version,
    description='Cathodoluminescence analysis with hyperspy.',
    author=author,
    author_email=email,
    license=license,
    url="https://github.com/hyperspy_cl/hyperspy_cl",
    long_description=open('README.rst').read(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],

    packages=find_packages(),
    # adjust the tabbing
    install_requires=[
        'scikit-image >= 0.15.0',   # exclude_border argument in peak_finder laplacian (PR #436)
        'matplotlib >= 3.1.1',     # 3.1.0 failed
        'scikit-learn >= 0.19',     # reason unknown
        'hyperspy >= 1.5.2',        # earlier versions incompatible with numpy >= 1.17.0
    ],
    package_data={
        "": ["LICENSE", "README.rst"],
        "hyperspy_cl": ["*.py", "hyperspy_extension.yaml"],
    },
    entry_points={'hyperspy.extensions': ['hyperspy_cl = hyperspy_cl']},
    )
