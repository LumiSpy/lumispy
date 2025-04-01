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

import math

import numpy as np
import hyperspy.api as hs

sqrt2pi = math.sqrt(2 * math.pi)
sigma2fwhm = 2 * math.sqrt(2 * math.log(2))


class ConvGaussianExponential(hs.model.components1D.Expression):
    r"""Analytical convolution of Gaussian instrument response function and
    exponential decay function.

    .. math::

        f(x) = \frac{h}{2} \cdot \exp\left[(x - t_0 - \frac{\sigma^2}{2\tau})\tau^{-1}\right]
               \cdot \left[1 + \erf(\frac{x - t_0 - \sigma^2/\tau}{\sqrt{2}\sigma})right]

    =============== =============
     Variable        Parameter
    =============== =============
     :math:`h`       height
     :math:`t_0`     t0
     :math:`\sigma`  sigma
     :math:`\tau`    tau
    =============== =============

    Parameters
    ----------
    height : float
        Height parameter.
    t0 : float
        Location parameter.
    sigma : float
        Scale (width) parameter of the Gaussian distribution.
    tau : float
        Decay parameter (lifetime) of the exponential function.
    **kwargs
        Extra keyword arguments are passed to the
        :py:class:`~._components.expression.Expression` component.

    Attributes
    ----------
    fwhm : float
        Convenience attribute to get and set the full width at half maximum.
    A : float
        Convenience attribute to get and set the area and defined for
        compatibility with `Gaussian` component.
    """

    def __init__(
        self,
        height=1,
        t0=0.0,
        sigma=20,
        tau=100,
        module=["numpy", "scipy"],
        compute_gradients=False,
        **kwargs,
    ):
        super().__init__(
            expression="1/2*height*exp(-((x-t0) - sigma**2/(2*tau))/tau)*\
                        (1 + erf(((x-t0) - sigma**2/tau)/(sqrt(2)*sigma)))",
            name="ConvGaussianExponential",
            height=height,
            t0=t0,
            sigma=sigma,
            tau=tau,
            position="t0",
            autodoc=False,
            module=module,
            compute_gradients=compute_gradients,
            **kwargs,
        )

        # Boundaries
        self.height.bmin = 0.0
        self.height.bmax = None

        self.sigma.bmin = 1.0
        self.sigma.bmax = None

        self.tau.bmin = 1.0
        self.tau.bmax = None

        self.isbackground = False
        self.convolved = True

    
    @property
    def fwhm(self):
        return self.sigma.value * sigma2fwhm

    @fwhm.setter
    def fwhm(self, value):
        self.sigma.value = value / sigma2fwhm

    @property
    def A(self):
        return self.height.value * self.sigma * sqrt2pi

    @A.setter
    def A(self, value):
        self.height.value = value / (self.sigma * sqrt2pi)
