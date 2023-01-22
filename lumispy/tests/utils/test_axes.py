# -*- coding: utf-8 -*-
# Copyright 2019-2022 The LumiSpy developers
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

from numpy import arange
from numpy.testing import assert_allclose
from pytest import warns

from lumispy import nm2eV, eV2nm, nm2invcm, invcm2nm
from lumispy.utils.axes import _n_air


def test__n_air():
    wl = arange(800) * 2 + 150
    with warns(UserWarning, match="The wavelength"):
        n = _n_air(wl)
    assert n[0] == _n_air(185)
    assert n[-1] == _n_air(1700)
    with warns(UserWarning):
        assert _n_air(180) == _n_air(185)
    with warns(UserWarning):
        assert _n_air(1705) == _n_air(1700)
    assert_allclose(_n_air(200), 1.00032406)
    assert_allclose(_n_air(500), 1.00027896)


def test_nm2eV():
    assert_allclose(nm2eV(200), 6.19720164)
    assert_allclose(nm2eV(300), 4.13160202)


def test_eV2nm():
    assert_allclose(eV2nm(2), 619.74951462)
    assert_allclose(eV2nm(3), 413.16411768)


def test_nm2invcm():
    assert nm2invcm(250) == 4e4
    assert nm2invcm(400) == 25e3


def test_invcm2nm():
    assert invcm2nm(4e4) == 250
    assert invcm2nm(25e3) == 400