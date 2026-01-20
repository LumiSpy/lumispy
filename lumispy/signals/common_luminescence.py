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

"""
Signal class for luminescence data (BaseSignal class)
-----------------------------------------------------
"""

import numpy as np
from warnings import warn
from lumispy.utils.signals import crop_edges

from lumispy import nm2invcm
from lumispy.utils import (
    axis2eV,
    data2eV,
    var2eV,
    axis2invcm,
    data2invcm,
    var2invcm,
)


class CommonLumi:
    """**General luminescence signal class (dimensionless)**"""

    def crop_edges(self, crop_range=None, crop_px=None, rebin_nav=False, **kwargs):
        """Crop edges along the navigation axes of the signal object.

        Crop the amount of pixels from the four edges of the scanning
        region, from the edges inwards.

        Cropping can happen uniformly on all sides or by specifying the
        cropping range for each axis or each side independently.

        If the shape of the navigation axes differs between the signals,
        all signals can be rebinned to match the shape of the first
        signal in the list.

        Parameters
        ----------
        crop_range : {int | float | str} or tuple of {ints | floats | strs}
            If ``int`` the values are taken as indices.
            If ``float`` the values are converted to indices.
            If ``str``, HyperSpy fancy indexing is used
            (e.g. ``rel0.1`` will crop 10% on each side, or ``100 nm``
            will crop 100 nm on each side).
            If a number or a tuple of size 1 is passed, all sides are cropped
            by the same amount.
            If a tuple of size 2 is passed (``crop_x``, ``crop_y``), a different
            amount is cropped from the x and y directions, respectively.
            If a tuple of size 4 is passed
            (``crop_left``, ``crop_bottom``, ``crop_right``, ``crop_top``),
            a different amount is cropped from each edge individually.
        rebin_nav : bool
            If the shape of the navigation axes differs between the signals,
            all signals can be be rebinned to match the shape of the first signal
            in the list. Note this does not take into account the calibration
            values of the navigation axes.
        kwargs
            To account for the deprecated ``crop_px`` parameter.
        """
        if crop_px is not None:
            warn(
                "The ``crop_px`` parameter is deprecated; use ``crop_range`` instead.",
                DeprecationWarning,
            )
            return crop_edges(self, crop_px=crop_px)

        return crop_edges(self, crop_range=crop_range, rebin_nav=rebin_nav, **kwargs)

    def remove_negative(self, basevalue=1, inplace=False):
        """Set all negative values to 'basevalue', e.g. for logarithmic scale plots.

        Parameters
        ----------
        basevalue : float
            Value by which negative values are replaced (default = 1).
        inplace : boolean
            If `False` (default), a new signal object is created and returned.
            Otherwise, the operation is performed on the existing signal object.

        Notes
        -----
        Sets `metadata.Signal.negative_removed` to `True`.
        """
        if inplace:
            s = self
        else:
            s = self.deepcopy()
        s.data[self.data < 0] = basevalue
        s.metadata.Signal.negative_removed = True
        if not inplace:
            return s

    def scale_by_exposure(self, integration_time=None, inplace=False, **kwargs):
        """Scale data in spectrum by integration time / exposure,
        (e.g. convert counts to counts/s).

        Parameters
        ----------
        integration_time : float
            Integration time (exposure) in s. If not given, the function tries to
            use the 'metadata.Acqusition_instrument.Detector.integration_time'
            field or alternatively find any 'integration_time', 'exposure' or
            'dwell_time' fields in the `original_metadata`.
        inplace : boolean
            If `False` (default), a new signal object is created and returned.
            If `True`, the operation is performed on the existing signal object.

        Notes
        -----
        Sets `metadata.Signal.scaled` to `True`. If intensity units is 'counts',
        replaces them by 'counts/s'.

        .. deprecated:: 0.2
          The `exposure` argument was renamed `integration_time`, and it will
          be removed in LumiSpy 1.0.
        """
        # Check metadata tags that would prevent scaling
        if self.metadata.Signal.get_item("normalized"):
            raise AttributeError("Data was normalized and cannot be scaled.")
        elif self.metadata.Signal.get_item("scaled") or self.metadata.Signal.get_item(
            "quantity"
        ) == ("Intensity (counts/s)" or "Intensity (Counts/s)"):
            raise AttributeError("Data was already scaled.")

        # Make sure integration_time is given or contained in metadata
        if integration_time is None:
            if "exposure" in kwargs:
                integration_time = kwargs["exposure"]
                warn(
                    "The `exposure` argument was renamed `integration_time` "
                    "and it will be removed in LumiSpy 1.0.",
                    DeprecationWarning,
                )
            elif self.metadata.has_item(
                "Acquisition_instrument.Detector.integration_time"
            ):
                integration_time = float(
                    self.metadata.get_item(
                        "Acquisition_instrument.Detector.integration_time"
                    )
                )
            else:
                raise AttributeError(
                    "Integration time (exposure) not given and it is not "
                    "included in the metadata."
                )
        if inplace:
            s = self
        else:
            s = self.deepcopy()
        s.data = s.data / integration_time
        s.metadata.Signal.scaled = True
        if s.metadata.get_item("Signal.quantity") == "Intensity (Counts)":
            s.metadata.Signal.quantity = "Intensity (Counts/s)"
            print(s.metadata.Signal.quantity)
        if s.metadata.get_item("Signal.quantity") == "Intensity (counts)":
            s.metadata.Signal.quantity = "Intensity (counts/s)"
        if not inplace:
            return s

    def normalize(self, pos=float("nan"), element_wise=False, inplace=False):
        """Normalize data to value at `pos` along signal axis, defaults to
        maximum value.

        Can be helpful for e.g. plotting, but does not make sense to use
        on signals that will be used as input for further calculations!

        Parameters
        ----------
        pos : float, int
            If 'nan' (default), spectra are normalized to the maximum.
            If `float`, position along signal axis in calibrated units at which
            to normalize the spectra.
            If `int`, index along signal axis at which to normalize the spectra.
        element_wise: boolean
            If `False` (default), a spectrum image is normalized by a common factor.
            If `True`, each spectrum is normalized individually.
        inplace : boolean
            If `False` (default), a new signal object is created and returned.
            If `True`, the operation is performed on the existing signal object.

        Notes
        -----
        Sets `metadata.Signal.normalized` to `True`. If
        `metadata.Signal.quantity` contains the word 'Intensity', replaces this
        field with 'Normalized intensity'.
        """
        if self.metadata.Signal.get_item("normalized"):
            warn(
                "Data was already normalized previously. Depending on the "
                "previous parameters this function might not yield the "
                "expected result.",
                UserWarning,
            )
        if inplace:
            s = self
        else:
            s = self.deepcopy()
        # normalize on maximum
        if np.isnan(pos):
            if element_wise:
                s = s / s.max(axis=-1)
            else:
                s.data = s.data / s.max(axis=-1).max().data
        # normalize on given position along signal axis
        else:
            if element_wise:
                s = s / s.isig[pos]
            else:
                s.data = s.data / s.isig[pos].max().data
        s.metadata.Signal.normalized = True
        if s.metadata.get_item("Signal.quantity") is not None:
            if s.metadata.Signal.quantity.find("Intensity") != -1:
                s.metadata.Signal.quantity = "Normalized intensity"
        if not inplace:
            return s

    def _reset_variance_linear_model(self):
        """Reset the variance linear model parameters to their default values,
        as they are not applicable any longer after a Jacobian transformation.
        """
        if (
            (
                self.metadata.has_item(
                    "Signal.Noise_properties.Variance_linear_model.gain_factor"
                )
                and self.metadata.Signal.Noise_properties.Variance_linear_model.gain_factor
                != 1
            )
            or (
                self.metadata.has_item(
                    "Signal.Noise_properties.Variance_linear_model.gain_offset"
                )
                and self.metadata.Signal.Noise_properties.Variance_linear_model.gain_offset
                != 0
            )
            or (
                self.metadata.has_item(
                    "Signal.Noise_properties.Variance_linear_model.correlation_factor"
                )
                and self.metadata.Signal.Noise_properties.Variance_linear_model.correlation_factor
                != 1
            )
        ):
            self.metadata.Signal.Noise_properties.Variance_linear_model.gain_factor = 1
            self.metadata.Signal.Noise_properties.Variance_linear_model.gain_offset = 0
            self.metadata.Signal.Noise_properties.Variance_linear_model.correlation_factor = (
                1
            )
            warn(
                "Following the Jacobian transformation, the parameters of the "
                "`Variance_linear_model` are reset to their default values "
                "(gain_factor=1, gain_offset=0, correlation_factor=1).",
                UserWarning,
            )

    def _convert_data(self, newaxis, factor, inplace, jacobian, data2, var2):
        """Utility function to perform the data and variance conversion for
        signal unit transformations.
        """
        # convert data
        if jacobian:
            s2data = np.copy(
                data2(
                    self.isig[::-1].data,
                    factor,
                    newaxis.axis,
                    self.axes_manager.signal_axes[0],
                )
            )
        else:
            s2data = np.copy(self.isig[::-1].data)

        # inplace conversion
        if inplace:
            s2 = self
            s2.data = s2data
        # create new signal object with correct data, axes, metadata
        else:
            s2 = self._deepcopy_with_new_data(
                s2data,
                copy_variance=(not jacobian),
                copy_learning_results=False,
            )
        # convert axis
        oldaxis = self.axes_manager.signal_axes[0]
        axind = self.axes_manager.signal_axes[0].index_in_axes_manager
        # workaround for bug in set_axis that changes wrong axis
        if self.axes_manager.signal_dimension == 2:
            axind += 1
        s2.axes_manager.set_axis(newaxis, axind)
        # convert variance
        if self.metadata.has_item("Signal.Noise_properties.variance"):
            var = self.get_noise_variance()
            if jacobian:
                # if variance is a numeric value, cast into signal object
                if isinstance(var, (float, int)):
                    var = self._deepcopy_with_new_data(
                        np.ones(self.data.shape) * var,
                        copy_variance=False,
                        copy_learning_results=False,
                    )
                s2var = s2._deepcopy_with_new_data(
                    var2(
                        var.isig[::-1].data,
                        factor,
                        newaxis.axis,
                        oldaxis,
                    ),
                    copy_variance=False,
                    copy_learning_results=False,
                )
                s2.set_noise_variance(s2var)
                s2._reset_variance_linear_model()
            else:
                # variance left unchanged, if it is a number and Jacobian not performed
                if isinstance(var, (float, int)):
                    if not inplace:
                        s2.set_noise_variance(self.get_noise_variance())
                else:
                    s2.set_noise_variance(
                        s2._deepcopy_with_new_data(
                            var.isig[::-1].data,
                            copy_variance=False,
                            copy_learning_results=False,
                        )
                    )
        if not inplace:
            return s2
        else:
            return None

    def to_eV(self, inplace=True, jacobian=True):
        """Convert signal axis of 1D signal to non-linear energy axis (eV).

        Uses wavelength dependent refractive index of air. Assumes wavelength
        in units of nm unless the axis units are specifically set to µm.

        The intensity is converted from counts/nm (counts/µm) to counts/meV by
        doing a Jacobian transformation, see e.g. Mooney and Kambhampati, J.
        Phys. Chem. Lett. 4, 3316 (2013), doi:10.1021/jz401508t, which ensures
        that integrated signals are correct also in the energy domain. If the
        variance of the signal is known, i.e.
        `metadata.Signal.Noise_properties.variance` is a signal representing
        the variance, a squared renormalization of the variance is performed.
        Note that if the variance is a number (not a signal instance), it is
        converted to a signal if the Jacobian transformation is performed

        Parameters
        ----------
        inplace : boolean
            If `False`, a new signal object is created and returned. Otherwise
            (default) the operation is performed on the existing signal object.
        jacobian : boolean
            The default is to do the Jacobian transformation (recommended at
            least for luminescence signals), but the transformation can be
            suppressed by setting this option to `False`.

        Examples
        --------
        >>> import numpy as np
        >>> from lumispy import LumiSpectrum
        >>> S1 = LumiSpectrum(np.ones(20), DataAxis(axis = np.arange(200,400,10)), ))
        >>> S1.to_eV()
        """
        evaxis, factor = axis2eV(self.axes_manager.signal_axes[0])

        return self._convert_data(evaxis, factor, inplace, jacobian, data2eV, var2eV)

    TO_INVCM_DOCSTRING = """
The intensity is converted from counts/nm (counts/µm) to counts/cm^-1
by doing a Jacobian transformation, see e.g. Mooney and Kambhampati,
J. Phys. Chem. Lett. 4, 3316 (2013), doi:10.1021/jz401508t, which
ensures that integrated signals are correct also in the wavenumber
domain. If the variance of the signal is known, i.e.
`metadata.Signal.Noise_properties.variance` is a signal representing the
variance, a squared renormalization of the variance is performed.
Note that if the variance is a number (not a signal instance), it is
converted to a signal if the Jacobian transformation is performed

Parameters
----------
inplace : boolean
    If `False`, a new signal object is created and returned. Otherwise
    (default) the operation is performed on the existing signal object.
"""

    TO_INVCM_EXAMPLE = """
Examples
--------
>>> import numpy as np
>>> from lumispy import LumiSpectrum
>>> S1 = LumiSpectrum(np.ones(20), DataAxis(axis = np.arange(200,400,10)), ))
>>> S1.to_invcm()
"""

    def to_invcm(self, inplace=True, jacobian=True):
        r"""Convert signal axis of 1D signal to non-linear wavenumber axis (cm^-1).

        Assumes wavelength in units of nm unless the axis units are
        specifically set to µm.

        %s
        jacobian : boolean
            The default is to do the Jacobian transformation (recommended at
            least for luminescence signals), but the transformation can be
            suppressed by setting this option to `False`.
        %s
        """
        invcmaxis, factor = axis2invcm(self.axes_manager.signal_axes[0])

        return self._convert_data(
            invcmaxis, factor, inplace, jacobian, data2invcm, var2invcm
        )

    to_invcm.__doc__ %= (TO_INVCM_DOCSTRING, TO_INVCM_EXAMPLE)

    TO_INVCMREL_EXAMPLE = """
Examples
--------
>>> import numpy as np
>>> from lumispy import LumiSpectrum
>>> S1 = LumiSpectrum(np.ones(20), DataAxis(axis = np.arange(200,400,10)), ))
>>> S1.to_invcm(laser=325)
"""

    def to_invcm_relative(self, laser=None, inplace=True, jacobian=False):
        r"""Convert signal axis of 1D signal to Raman/Stokes shift.

        The non-linear wavenumber axis (cm^-1) relative
        to the exciting laser wavelength (Raman/Stokes
        shift). Assumes wavelength in units of nm unless the axis units are
        specifically set to µm.

        %s
        laser: float or None
            Laser wavelength in the same units as the signal axis. If None
            (default), checks if it is stored in
            `metadata.Acquisition_instrument.Laser.wavelength`.
        jacobian : boolean
            The default is not to do the Jacobian transformation for Raman
            shifts, but the transformation can be activated by setting this
            option to `True`.
        %s
        """
        # check if laser wavelength is available
        if laser is None:
            if not self.metadata.has_item("Acquisition_instrument.Laser.wavelength"):
                raise AttributeError(
                    "Laser wavelength is neither given in the metadata nor passed"
                    " to the function."
                )
            else:
                laser = self.metadata.get_item(
                    "Acquisition_instrument.Laser.wavelength"
                )
        # check if laser units make sense in respect to signal units
        if (self.axes_manager.signal_axes[0].units == "µm" and laser > 10) or (
            self.axes_manager.signal_axes[0].units == "nm" and laser < 100
        ):
            raise AttributeError(
                "Laser wavelength units do not seem to match the signal units."
            )

        invcmaxis, factor = axis2invcm(self.axes_manager.signal_axes[0])

        # convert to relative wavenumber scale
        if self.axes_manager.signal_axes[0].units == "µm":
            invcmlaser = nm2invcm(1000 * laser)
        else:
            invcmlaser = nm2invcm(laser)
        absaxis = invcmaxis.axis[::-1]
        invcmaxis.axis = invcmlaser - absaxis
        invcmaxis.name = "Raman Shift"

        # replace signal axis after conversion
        # conversion (using absolute scale for Jacobian)
        if inplace:
            self.to_invcm(inplace=inplace, jacobian=jacobian)
            s2 = self
        else:
            s2 = self.to_invcm(inplace=inplace, jacobian=jacobian)
        # replace axis
        axind = self.axes_manager.signal_axes[0].index_in_axes_manager
        # workaround for bug in set_axis that changes wrong axis
        if self.axes_manager.signal_dimension == 2:
            axind += 1
        s2.axes_manager.set_axis(invcmaxis, axind)
        s2.data = s2.isig[::-1].data
        # replace variance axis
        if s2.metadata.has_item("Signal.Noise_properties.variance") and not isinstance(
            s2.get_noise_variance(), (float, int)
        ):
            axind = self.axes_manager.signal_axes[0].index_in_axes_manager
            # workaround for bug in set_axis that changes wrong axis
            if self.axes_manager.signal_dimension == 2:
                axind += 1
            s2.metadata.Signal.Noise_properties.variance.axes_manager.set_axis(
                invcmaxis,
                axind,
            )
            s2.metadata.Signal.Noise_properties.variance.data = (
                s2.metadata.Signal.Noise_properties.variance.isig[::-1].data
            )
        if not inplace:
            return s2
        else:
            return None

    to_invcm_relative.__doc__ %= (
        TO_INVCM_DOCSTRING,
        TO_INVCMREL_EXAMPLE,
    )

    # Alias Method Name
    to_raman_shift = to_invcm_relative
