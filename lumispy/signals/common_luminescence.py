# -*- coding: utf-8 -*-
# Copyright 2019-2021 The LumiSpy developers
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

"""Signal class for Luminescence data (BaseSignal class).
"""

from numpy import isnan
from warnings import warn


class CommonLumi:
    """General Luminescence signal class (dimensionless).
    ----------
    """

    def crop_edges(self, crop_px):
        """
        Crop the amount of pixels from the four edges of the scanning region, from out the edges inwards.

        Parameters
        ----------
        crop_px : int
            Amount of pixels to be cropped on each side individually.

        Returns
        -------
        signal_cropped : CommonLuminescence
            A smaller cropped CL signal object. If inplace is True, the original
            object is modified and no LumiSpectrum is returned.
        """

        width = self.axes_manager.shape[0]
        height = self.axes_manager.shape[1]

        if crop_px * 2 > width or crop_px * 2 > height:
            raise ValueError(
                "The pixels to be cropped cannot be larger than half the width or the length!"
            )
        else:
            signal_cropped = self.inav[
                crop_px + 1 : width - crop_px + 1, crop_px + 1 : height - crop_px + 1
            ]

        # Store transformation in metadata (or update the value if already previously transformed)

        try:
            signal_cropped.metadata.Signal.cropped_edges += crop_px
        except AttributeError:
            signal_cropped.metadata.set_item("Signal.cropped_edges", crop_px)

        return signal_cropped

    def remove_negative(self, basevalue=1, inplace=True):
        """Sets all negative values to 'basevalue', e.g. for logarithmic scale
        plots.

        Parameters:
        -----------
        basevalue : float
            Value by which negative values are replaced (default = 1).
        inplace : boolean
            If `False`, a new signal object is created and returned. Otherwise
            (default) the operation is performed on the existing signal object.

        Notes:
        ------
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

    def scale_by_exposure(self, exposure=float("nan"), inplace=False):
        """Scale data in spectrum by exposure (e.g. convert counts to counts/s).

        Parameters:
        -----------
        exposure : float
            Exposure time in s. If not given, the function tries to find
            'exposure' or 'dwell_time' in the metadata (for the moment only at
            Gatan specific nodes).
        inplace : boolean
            If `False` (default), a new signal object is created and returned.
            If `True`, the operation is performed on the existing signal object.

        Notes:
        ------
        Sets `metadata.Signal.scaled` to `True`. If intensity units is 'counts',
        replaces them by 'counts/s'.
        """
        # Check metadata tags that would prevent scaling
        if self.metadata.Signal.get_item("normalized"):
            raise AttributeError("Data was normalized and cannot be scaled.")
        elif self.metadata.Signal.get_item("scaled") or self.metadata.Signal.get_item(
            "quantity"
        ) == ("Intensity (counts/s)" or "Intensity (Counts/s)"):
            raise AttributeError("Data was already scaled.")

        # Make sure exposure is given or contained in metadata
        if isnan(exposure):
            # use nested_get from hyperspy when it is available
            if self.metadata.has_item("Acquisition_instrument.CL.exposure"):
                exposure = float(
                    self.metadata.get_item("Acquisition_instrument.CL.exposure")
                )
            elif self.metadata.has_item("Acquisition_instrument.CL.dwell_time"):
                exposure = float(
                    self.metadata.get_item("Acquisition_instrument.CL.dwell_time")
                )
            else:
                raise AttributeError(
                    "Exposure not given and can not be "
                    "extracted automatically from metadata."
                )
        if inplace:
            s = self
        else:
            s = self.deepcopy()
        s.data = s.data / exposure
        s.metadata.Signal.scaled = True
        if s.metadata.get_item("Signal.quantity") == "Intensity (Counts)":
            s.metadata.Signal.quantity = "Intensity (Counts/s)"
            print(s.metadata.Signal.quantity)
        if s.metadata.get_item("Signal.quantity") == "Intensity (counts)":
            s.metadata.Signal.quantity = "Intensity (counts/s)"
        if not inplace:
            return s

    def normalize(self, pos=float("nan"), element_wise=False, inplace=False):
        """Normalizes data to value at `pos` along signal axis, defaults to
        maximum value.

        Can be helpful for e.g. plotting, but does not make sense to use
        on signals that will be used as input for further calculations!

        Parameters:
        -----------
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

        Notes:
        ------
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
