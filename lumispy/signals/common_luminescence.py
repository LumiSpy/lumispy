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

"""
Signal class for luminescence data (BaseSignal class)
-----------------------------------------------------
"""

from logging import warning
from numpy import isnan, array, abs
from warnings import warn


class CommonLumi:
    """**General luminescence signal class (dimensionless)**"""

    def crop_edges(self, crop_range, crop_units="pixel"):
        """Crop the amount of pixels from the four edges of the scanning
        region, from out the edges inwards. Cropping can happen uniformily or by specifying the croping range for each axis or each side.

        Parameters
        ----------
        crop_range : int, float, tuple
            Amount of pixels to be cropped. If an number or a 1-tuple is passed, all sides are cropped by the same amount. If a 2-tuple is passed (crop_x, crop_y), a different amount of pixels is cropped from the x and y directions, respectively. If a 4-tuple is passed (crop_left, crop_bottom, crop_right, crop_top), a different amount of pixels is cropped from each edge individually.

        crop_units : str
            Select in which units cropping happens. It can be in `pixel` units (default), or in `percent`/`%` units.

        Returns
        -------
        signal_cropped : CommonLuminescence
            A smaller cropped CL signal object.
        """

        units_accepted = ("px", "pixel", "percent", "%")
        if crop_units.lower() not in units_accepted:
            raise ValueError(
                "The param crop_units only accepts `pixel` units or `percent`."
            )

        w = self.axes_manager.shape[0]
        h = self.axes_manager.shape[1]
        crop_range_type = type(crop_range)

        if crop_range_type in (int, float):
            crop_vals = [crop_range] * 4
        elif crop_range_type is tuple:
            if len(crop_range) == 2:
                crop_vals = (list(crop_range) * 2,)
                crop_vals = crop_vals[0]
            elif len(crop_range) == 4:
                crop_vals = list(crop_range)
            else:
                raise ValueError(
                    f"The crop_range tuple must be either a 2-tuple (x,y) or a 4-tuple (left, bottom, right, top). You provided a {len(crop_range)}-tuple."
                )
        else:
            raise ValueError(
                f"The crop_range value must be a number or a tuple, not a {crop_range_type}"
            )

        # Negative means reverse indexing
        crop_vals = array(crop_vals) * [1, -1, -1, 1]

        # Convert percentages to pixel units
        if crop_units.lower() in units_accepted[-2:]:
            crop_vals = crop_vals * array([w, h] * 2)
            crop_vals = crop_vals.astype(int)

        # Remove 0 for None
        crop_ids = [x if x != 0 else None for x in crop_vals]

        # Crop accordingly
        signal_cropped = self.inav[
            crop_ids[0] : crop_ids[2], crop_ids[3] : crop_ids[1]
        ]

        # Check if cropping went too far
        if 0 in signal_cropped.axes_manager.navigation_shape:
            warn(
                "The pixels to be cropped surpassed the width/height of the signal navigation axes.",
                UserWarning,
            )

        # Store transformation in metadata (or update the value if already previously transformed)
        try:
            signal_cropped.metadata.Signal.cropped_edges += abs(crop_vals)
        except AttributeError:
            signal_cropped.metadata.set_item(
                "Signal.cropped_edges", abs(crop_vals)
            )

        return signal_cropped

    def remove_negative(self, basevalue=1, inplace=False):
        """Sets all negative values to 'basevalue', e.g. for logarithmic scale
        plots.

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

    def scale_by_exposure(
        self, integration_time=None, inplace=False, **kwargs
    ):
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
            raise AttributeError(
                "Data was normalized and cannot be scaled."
            )
        elif self.metadata.Signal.get_item(
            "scaled"
        ) or self.metadata.Signal.get_item("quantity") == (
            "Intensity (counts/s)" or "Intensity (Counts/s)"
        ):
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
        if (
            s.metadata.get_item("Signal.quantity")
            == "Intensity (Counts)"
        ):
            s.metadata.Signal.quantity = "Intensity (Counts/s)"
            print(s.metadata.Signal.quantity)
        if (
            s.metadata.get_item("Signal.quantity")
            == "Intensity (counts)"
        ):
            s.metadata.Signal.quantity = "Intensity (counts/s)"
        if not inplace:
            return s

    def normalize(
        self, pos=float("nan"), element_wise=False, inplace=False
    ):
        """Normalizes data to value at `pos` along signal axis, defaults to
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
        if isnan(pos):
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
