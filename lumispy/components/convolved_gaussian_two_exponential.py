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


class ConvGaussTwoExp(hs.model.components1D.Expression):
    r"""Analytical convolution of Gaussian instrument response function and two
    exponential decay functions.

    .. math::

        f(x) = \frac{h_1}{2} \cdot \exp\left[\frac{\sigma^2}{2\tau^2_1} - \frac{x - t_0}{\tau_1}\right] \cdot
        \left[\operatorname{erfc}\left(\frac{\sigma^2 - \tau_1(x - t_0)}{\sqrt{2}\sigma\tau_1}\right)\right] +
        \frac{h_2}{2} \cdot \exp\left[\frac{\sigma^2}{2\tau^2_2} - \frac{x - t_0}{\tau_2}\right] \cdot
        \left[\operatorname{erfc}\left(\frac{\sigma^2 - \tau_2(x - t_0)}{\sqrt{2}\sigma\tau_2}\right)\right]

    =============== ==============
     Variable        Parameter
    =============== ==============
     :math:`h_1`     height1
     :math:`h_2`     height2
     :math:`t_0`     t0
     :math:`\sigma`  sigma
     :math:`\tau_1`  tau1
     :math:`\tau_2`  tau2
    =============== ==============

    Parameters
    ----------
    height1: float
        Height parameter of the first exponential.
    height2: float
        Height parameter of the second exponential.
    t0: float
        Location parameter.
    sigma: float
        Scale (width) parameter of the Gaussian distribution.
    tau1: float
        Decay parameter (lifetime) of the first exponential function.
    tau2: float
        Decay parameter (lifetime) of the second exponential function.

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
        height1=1.0,
        height2=1.0,
        t0=0.0,
        sigma=10.0,
        tau1=100.0,
        tau2=80.0,
        module=["numpy", "scipy"],
        **kwargs,
    ):
        super().__init__(
            expression="1/2*height1*exp(sigma**2/(2*tau1**2)-((x-t0)/tau1))*\
                    erfc((sigma**2-tau1*(x-t0))/(sqrt(2)*sigma*tau1))+\
                    1/2*height2*exp(sigma**2/(2*tau2**2)-((x-t0)/tau2))*\
                    erfc((sigma**2-tau2*(x-t0))/(sqrt(2)*sigma*tau2))",
            name="ConvGaussTwoExp",
            height1=height1,
            height2=height2,
            t0=t0,
            sigma=sigma,
            tau1=tau1,
            tau2=tau2,
            position="t0",
            module=module,
            **kwargs,
        )
        #
        self._id_name = "bfda25c1-c1f5-4ff8-86d5-94cc659152d4"

        # Boundaries
        self.height1.bmin = 0.0
        self.height1.bmax = None

        self.height2.bmin = 0.0
        self.height2.bmax = None

        self.sigma.bmin = 1e-12
        self.sigma.bmax = None

        self.tau1.bmin = 1.0
        self.tau1.bmax = None

        self.tau2.bmin = 1.0
        self.tau2.bmax = None

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
        return (
            self.height1.value * self.tau1.value + self.height2.value * self.tau2.value
        )

    @property
    def A1(self):
        return self.height1.value * self.tau1.value

    @A1.setter
    def A1(self, value):
        self.height1.value = value / self.tau1.value

    @property
    def A2(self):
        return self.height2.value * self.tau2.value

    @A2.setter
    def A2(self, value):
        self.height2.value = value / self.tau2.value
