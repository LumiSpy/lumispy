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
from hyperspy.axes import FunctionalDataAxis
from scipy.ndimage import center_of_mass
from scipy.interpolate import interp1d
from warnings import warn

CROP_EDGES_DOCSTRING = """
    Crop the amount of pixels from the four edges of the scanning
    region, from the edges inwards.

    Cropping can happen uniformly on all sides or by specifying the
    cropping range for each axis or each side independently.

    If the shape of the navigation axes differs between the signals,
    all signals can be rebinned to match the shape of the first 
    signal in the list.
    """

CROP_EDGES_PARAMETERS = """
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


def com(spectrum_intensities, signal_axis, **kwargs):
    """Finds the centroid (center of mass) of a peak in the spectrum based
    from the intensity at each pixel value and its respective signal axis.

    Parameters
    ----------
    spectrum_intensities : array
        An array with the intensities of the spectrum.
    signal_axis: hyperspy.axes.BaseDataAxis subclass
        A HyperSpy signal axis class containing an array with the wavelength/
        energy for each intensity/signal value.
    kwargs : dictionary
        For the scipy.interpolate.interp1d function.

    Returns
    -------
    center_of_mass : float
        The centroid of the spectrum.

    Examples
    --------
    # Assume we have a spectrum with wavelengths and intensities
    >>> wavelengths = [200, 300, 400, 500, 600, 700]
    >>> intensities = [1, 2, 3, 2, 1, 0]
    >>> from hyperspy.axes import DataAxis
    >>> signal_axis = DataAxis(axis=wavelengths)

    >>> center_of_mass = com(intensities, signal_axis)
    >>> print(center_of_mass)  # Outputs: [400.0]
    """

    def _interpolate_signal(axis_array, index, **kwargs):
        """
        Wrapper for `hs.axes.index2value` that linearly interpolates between
        values should the index passed not be a integer. Using the kwargs, the
        interpolation method can be changed.
        """
        rem = index % 1
        index = int(index // 1)
        if rem == 0:
            return axis_array[int(index)]
        else:
            y = [axis_array[index], axis_array[index + 1]]
            x = [0, 1]
            fx = interp1d(x, y, **kwargs)
            return float(fx(rem))

    # Find center of mass wrt array index
    index_com = float(center_of_mass(spectrum_intensities)[0])

    # Check for the type of hyperspy.axis
    if type(signal_axis) == FunctionalDataAxis:
        # Calculate value y from x[index_com]
        x = _interpolate_signal(signal_axis.x.axis, index_com)
        kwargs = {}
        for kwarg in signal_axis.parameters_list:
            kwargs[kwarg] = getattr(signal_axis, kwarg)
        com_val = signal_axis._function(x, **kwargs)

    elif hasattr(signal_axis, "axis"):
        # Calculate value interpolating between index_com 0 and 1
        com_val = _interpolate_signal(signal_axis.axis, index_com)
    elif type(signal_axis) in (list, np.ndarray, tuple):
        # Check for dimensionality
        if len(spectrum_intensities) != len(signal_axis):
            raise ValueError(
                f"The length of the spectrum array {len(spectrum_intensities)} must match "
                "the length of the wavelength array {len(signal_axis)}."
            )
        # Calculate value interpolating between index_com 0 and 1
        com_val = _interpolate_signal(np.array(signal_axis), index_com)
    else:
        raise ValueError("The parmeter `signal_axis` must be a HyperSpy Axis object.")

    return com_val


#
# navigation axis manipulation
#


def crop_edges(
    S,
    crop_range=None,
    rebin_nav=False,
    **kwargs,
):
    """Crop edges along the navigation axes of a signal or of a list of signal objects.

    Crop the amount of pixels from the four edges of the scanning
    region, from the edges inwards.

    Cropping can happen uniformly on all sides or by specifying the
    cropping range for each axis or each side independently.

    If the shape of the navigation axes differs between the signals,
    all signals can be rebinned to match the shape of the first
    signal in the list.

    Parameters
    ----------
    S : Signal or list of Signals
        HyperSpy signal object(s) that should be cropped.
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

    Returns
    -------
    S_cropped : Signal or list of Signals
        A list of smaller, cropped Signal objects or a cropped single Signal
        if only one signal object is passed as input.
    """

    def range_formatting(str_list):
        if len(str_list) == 2:
            px = S[0].inav[: str_list[0]].axes_manager.navigation_shape[0]
            px_list = [px, -px]
        else:
            # Pairwaise formatting with [top, left, right, bottom] when len(str_list) == 4
            px_x = S[0].inav[: str_list[0], :].axes_manager.navigation_shape[0]
            px_y = S[0].inav[:, : str_list[1]].axes_manager.navigation_shape[1]
            px_list = [px_x, -px_y, -px_x, px_y]
        return np.array(px_list, dtype=int)

    # Deprecation warning (for compatibility with ``crop_px``)
    if "crop_px" in kwargs and crop_range is not None:
        warn(
            "Both ``crop_range`` and the deprecated ``crop_px`` were passed. Only ``crop_range`` is being used.",
            DeprecationWarning,
            2,
        )
    elif "crop_px" in kwargs:
        warn(
            "``crop_px`` is deprecated; use ``crop_range`` instead.",
            DeprecationWarning,
            2,
        )
        crop_range = int(kwargs["crop_px"])
    elif crop_range is None:
        crop_range = 0

    # Check that S is a list
    no_list = False
    if type(S) is not list:
        no_list = True
        S = [S]

    # Check all signals in list are compatible (same range) and rebin
    nav_shape = S[0].axes_manager.navigation_shape
    for i, s in enumerate(S):
        if i == 0:
            continue
        if len(nav_shape) != len(s.axes_manager.navigation_shape):
            raise ValueError(
                "The signal list contains a mix of navigation axes dimensions which cannot be broadcasted."
            )
        if nav_shape != s.axes_manager.navigation_shape:
            if not rebin_nav:
                warn(
                    f"The navivigation axes of the first signal in index = 0 and in index = {i} have different shapes of {nav_shape} and {s.axes_manager.navigation_shape} respectively. This may cause errors during cropping. You can turn `rebin_nav` to True to rebin navigation axes.",
                    UserWarning,
                )
            if rebin_nav:
                scale = np.array(s.axes_manager.navigation_shape) / np.array(nav_shape)
                signal_dim = len(s.axes_manager.signal_shape)
                scale = np.append(scale, [1] * signal_dim)
                S[i] = s.rebin(scale=scale)

    # Check for the size of the navigation axis
    line_scan = False
    nav_shape = s.axes_manager.navigation_shape
    if len(nav_shape) == 1:
        line_scan = True
    elif len(nav_shape) > 2:
        raise NotImplementedError(
            "`crop_edges` is not supported for navigation axes with more than 2 dimensions."
        )

    crop_range_type = type(crop_range)
    # Create a list of [top, left, right, bottom] or for line_scan only [left, right]
    n = 2 if line_scan else 4
    if crop_range_type in (int, float, str):
        crop_vals = [crop_range] * n
        crop_range = [crop_range]
    elif crop_range_type is tuple:
        if len(crop_range) == 2:
            crop_vals = (list(crop_range) * (n // 2),)
            crop_vals = crop_vals[0]
        elif len(crop_range) == 4 and not line_scan:
            crop_vals = list(crop_range)
        else:
            raise ValueError(
                f"The ``crop_range`` tuple must be either a 2-tuple (x,y) or a 4-tuple (left, bottom, right, top). You provided a {len(crop_range)}-tuple. For line scans, the tuple must be a 2-tuple (left, right)."
            )
    else:
        raise ValueError(
            f"The crop_range value must be a number, a string, or a tuple, not a {crop_range_type}"
        )

    # Negative means reverse indexing
    if type(crop_vals[0]) is int:
        if line_scan:
            crop_vals = np.array(crop_vals) * [1, -1]
        else:
            crop_vals = np.array(crop_vals) * [1, -1, -1, 1]
    else:
        # Check if input was already fine or if str/float needs to be reformatted
        if (len(crop_range) == 4) or (len(crop_range) == 2 and line_scan):
            # Shuffle order from [left, bottom, right, top] to [top, left, right, bottom]
            # crop_vals = [crop_vals[3], crop_vals[0], crop_vals[2], crop_vals[1]]
            pass
        else:
            crop_vals = range_formatting(crop_vals)

    S_cropped = []
    for s in S:

        # Remove 0 for None
        crop_ids = [x if x != 0 else None for x in crop_vals]

        # Crop accordingly
        if line_scan:
            signal_cropped = s.inav[crop_ids[0] : crop_ids[1]]
        else:
            signal_cropped = s.inav[
                crop_ids[0] : crop_ids[2], crop_ids[3] : crop_ids[1]
            ]

        # Check if cropping went too far
        if 0 in signal_cropped.axes_manager.navigation_shape:
            raise IndexError(
                "The pixels to be cropped surpassed the width/height of the signal navigation axes."
            )

        # Store transformation in metadata (or update the value if already previously transformed)
        if signal_cropped.metadata.has_item("Signal.cropped_edges"):
            signal_cropped.metadata.Signal.cropped_edges = np.vstack(
                (signal_cropped.metadata.Signal.cropped_edges, crop_vals)
            )
        else:
            signal_cropped.metadata.set_item("Signal.cropped_edges", crop_vals)
        S_cropped.append(signal_cropped)

    if no_list:
        return S_cropped[0]
    else:
        return S_cropped
