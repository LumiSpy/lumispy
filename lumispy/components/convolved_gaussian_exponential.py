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

import hyperspy.api as hs

sigma2fwhm = 2 * np.sqrt(2 * np.log(2))


class ConvGaussExp(hs.model.components1D.Expression):
    r"""Analytical convolution of Gaussian instrument response function and
    exponential decay function.

    .. math::

        f(x) = \frac{h}{2} \cdot \exp\left[\frac{\sigma^2}{2\tau^2} - \frac{x - t_0}{\tau}\right] \cdot \left[\operatorname{erfc}\left(\frac{\sigma^2 - \tau(x - t_0)}{\sqrt{2}\sigma\tau}\right)\right]

    =============== ==============
     Variable        Parameter
    =============== ==============
     :math:`h`       height
     :math:`t_0`     t0
     :math:`\sigma`  sigma
     :math:`\tau`    tau
    =============== ==============

    Parameters
    ----------
    height: float
        Height parameter.
    t0: float
        Location parameter.
    sigma: float
        Scale (width) parameter of the Gaussian distribution.
    tau: float
        Decay parameter (lifetime) of the exponential function.
    **kwargs
        Extra keyword arguments that are passed to the
        :py:class:`hyperspy._components.expression.Expression` component.

    Attributes
    ----------
    fwhm: float
        Convenience attribute to get and set the full width at half maximum.
    A: float
        Convenience attribute to get and set the area and defined for
        compatibility with `Gaussian` component.
    """

    def __init__(
        self,
        height=1.0,
        t0=0.0,
        sigma=10.0,
        tau=100.0,
        module=["numpy", "scipy"],
        **kwargs,
    ):
        super().__init__(
            expression="1/2*height*exp(sigma**2/(2*tau**2)-((x-t0)/tau))*\
                    erfc((sigma**2-tau*(x-t0))/(sqrt(2)*sigma*tau))",
            name="ConvGaussExp",
            height=height,
            t0=t0,
            sigma=sigma,
            tau=tau,
            position="t0",
            module=module,
            **kwargs,
        )
        # Id for hyperspy
        self._id_name = "049a5740-389b-4d7a-bab9-a6a7afc5c498"

        # Boundaries
        self.height.bmin = 0.0
        self.height.bmax = None

        self.sigma.bmin = 1e-12
        self.sigma.bmax = None

        self.tau.bmin = 1.0
        self.tau.bmax = None

        self.isbackground = False
        self.convolved = False

    @property
    def fwhm(self):
        return self.sigma.value * sigma2fwhm

    @fwhm.setter
    def fwhm(self, value):
        self.sigma.value = value / sigma2fwhm

    @property
    def A(self):
        return self.height.value * self.tau.value

    @A.setter
    def A(self, value):
        self.height.value = value / self.tau.value
