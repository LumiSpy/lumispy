# -*- coding: utf-8 -*-
# Copyright 2019 The LumiSpy developers
#
# This file is part of LumiSpy.
#
# LumiSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LumiSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LumiSpy.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

exec(open('lumispy/release_info.py').read())  # grab version info


setup(
    name='lumispy',
    version=version,
    description='Luminescence spectroscopy data analysis with HyperSpy.',
    authors='The LumiSpy Developers',
    #author_email=email,
    license=license,
    url="https://github.com/lumispy/lumispy",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    keywords = ['CL',
            'PL',
            'EL',
            'TRCL',
            'TRPL',
            'luminescence',
            'spectroscopy',
            'imaging',
            'spectrum image',
            'cathodoluminescence',
            'photoluminescence',
            'electroluminescence',
            'STEM',
            'SEM',
            'curve fitting',
            'data analysis',
            'hyperspectral',
            'hyperspectrum',
            'multidimensional',
            'lumispy',
            'hyperspy',
            'microscopy',
            'numpy',
            'python',
            'scipy'],

    packages=find_packages(),
    # adjust the tabbing
    install_requires=[
        'numpy',
        'scipy',
        'hyperspy >= 1.5.2',        # earlier versions incompatible with numpy >= 1.17.0
    ],
    extras_require={"tests": ["pytest>=5.0"],
                    "coverage": ["pytest-cov>=2.8.1", "codecov"]},,
    package_data={
        "lumispy": ["*.py", "hyperspy_extension.yaml"],
    },
    entry_points={'hyperspy.extensions': ['lumispy = lumispy']},
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/lumispy/lumispy/issues',
        'Source': 'https://github.com/lumispy/lumispy',
    },
    )
