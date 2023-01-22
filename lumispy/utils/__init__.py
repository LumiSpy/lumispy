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

from .axes import (
    nm2eV,
    eV2nm,
    axis2eV,
    data2eV,
    var2eV,
    nm2invcm,
    invcm2nm,
    axis2invcm,
    data2invcm,
    var2invcm,
    solve_grating_equation,
)

#
# navigation axis manipulation
#


def crop_edges(
    S,
    crop_range=None,
    crop_units="pixels",
    rebin_nav=False,
    *,
    crop_px=None,
):
    """
    Cropping along the navigation axes of a list of signal objects.
    Crop the amount of pixels from the four edges of the scanning
    region, from the edges inwards. Cropping can happen uniformly on all
    sides or by specifying the cropping range for each axis or each side. If the navigation axes shape is different, all signals can be rebinned to match the shape of the first signal in the list.

    Parameters
    ----------
    S : list of HyperSpy Signal objects with the same navigation axes or a single HyperSpy Signal object.
    crop_range : int, float, tuple
        Number of pixels or percentage (between 0 and 1) of image width/height to be cropped.
        If a number or a tuple of size 1 is passed, all sides are cropped by the
        same amount. If a tuple of size 2 is passed (``crop_x``, ``crop_y``), a different
        amount of pixels/percentage is cropped from the x and y directions,
        respectively. If a tuple of size 4 is passed (``crop_left``, ``crop_bottom``,
        ``crop_right``, ``crop_top``), a different amount of pixels/percentage is
        cropped from each edge individually.
    crop_units : str
        Select in which units cropping happens. Value can be either ``pixels``/``px`` (default),
        or ``percent``/``%``. All values are rounded downwards.
    rebin_nav : bool
        If the navigation axes shape is different between signals in the list S, all signals will be rebinned to match the shape of the first signal in the list.

    Returns
    -------
    S_cropped : Signal or list of Signals
        A list of smaller, cropped Signal objects or a cropped single Signal if only one signal object is passed as input.
    """
    # Deprecation warning (for compatibility with ``crop_px``)
    if crop_range is not None and crop_px is not None:
        warn(
            "Both ``crop_range`` and the deprecated ``crop_px`` were passed. Only ``crop_range`` is being used.",
            DeprecationWarning,
            2,
        )
    elif crop_px is not None:
        warn(
            "``crop_px`` is deprecated; use ``crop_range`` instead.",
            DeprecationWarning,
            2,
        )
        crop_range = crop_px
        crop_units = "pixels"
    elif crop_range is None:
        crop_range = 0

    # Check that S is a list
    no_list = False
    if type(S) is not list:
        no_list = True
        S = [S]

    # Check for units specified
    units_accepted = ("px", "pixel", "pixels", "percent", "%")
    if crop_units.lower() not in units_accepted:
        raise ValueError(
            "The parameter ``crop_units`` only accepts the strings ``pixels``/``px`` or ``percent``/``%`` as values."
        )

    # Check all signals in list are compatible (same range)
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
    if crop_range_type in (int, float):
        crop_vals = [crop_range] * n
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
            f"The crop_range value must be a number or a tuple, not a {crop_range_type}"
        )

    # Negative means reverse indexing
    if line_scan:
        crop_vals = np.array(crop_vals) * [1, -1]
    else:
        crop_vals = np.array(crop_vals) * [1, -1, -1, 1]

    S_cropped = []
    for s in S:
        w = s.axes_manager.navigation_shape[0]
        h = s.axes_manager.navigation_shape[1] if not line_scan else None

        crop_vals_s = crop_vals
        # Convert percentages to pixel units
        if crop_units.lower() in units_accepted[-2:]:
            if any(np.abs(crop_vals) > 1):
                crop_vals_s = crop_vals_s / 100

            crop_vals_s *= np.array([w, h] * (n // 2))
            crop_vals_s = crop_vals_s.astype(int)

        # Remove 0 for None
        crop_ids = [x if x != 0 else None for x in crop_vals_s]

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
            signal_cropped.metadata.Signal.cropped_edges += abs(crop_vals_s)
        else:
            signal_cropped.metadata.set_item("Signal.cropped_edges", abs(crop_vals_s))
        S_cropped.append(signal_cropped)

    if no_list:
        return S_cropped[0]
    else:
        return S_cropped


#
# spectrum axis manipulation
#

def join_spectra(S, r=50, scale=True, average=False, kind="slinear"):
    """Takes list of Signal1D objects and returns a single object with all
    spectra joined. Joins spectra at the center of the overlapping range.
    Scales spectra by a factor determined as average over the range
    `center -/+ r` pixels. Works both for uniform and non-uniform axes
    (FunctionalDataAxis is converted into a non-uniform DataAxis).

    Parameters
    ----------
    S : list of Signal1D objects (with overlapping signal axes)
    r : int, optional
        Number of pixels left/right of center (default `50`) defining the range
        over which to determine the scaling factor, has to be less than half
        of the overlapping pixels. Change the size of `r` or use `average=True`
        if the function induces a step in the intensity.
    scale : boolean, optional
        If `True` (default), the later spectra in the list are scaled by a
        factor determined over `center -/+ r` pixels. If `False`, spectra are
        joined without scaling, which will likely induce a step unless
        `average=True`.
    average : boolean, optional
        If `True`, the contribution of the two signals is continuously graded
        within the range defined by `r` instead of joining at the center of
        the range (default).
    kind : str, optional
        Interpolation method (default 'slinear') to use when joining signals
        with a uniform signal axes. See `scipy.interpolate.interp1d` for
        options.

    Returns
    -------
    A new Signal1D object containing the joined spectra (properties are copied
    from first spectrum).

    Examples
    --------

    >>> s1 = hs.signals.Signal1D(np.ones(32))
    >>> s2 = hs.signals.Signal1D(np.ones(32)*2)
    >>> s2.axes_manager.signal_axes[0].offset = 25
    >>> lum.join_spectra([s1,s2],r=2)
    <Signal1D, title: , dimensions: (|57)>
    """

    # Test that spectra overlap
    for i in range(1, len(S)):
        if (
            S[i - 1].axes_manager.signal_axes[0].axis.max()
            < S[i].axes_manager.signal_axes[0].axis.min()
        ):
            raise ValueError("Signal axes not overlapping")
    # Make sure that r is of type int
    if not type(r) is int:
        r = int(r)

    # take first spectrum as basis
    S1 = S[0].deepcopy()
    axis = S1.axes_manager.signal_axes[0]
    for i in range(1, len(S)):  # join following spectra
        S2 = S[i].deepcopy()
        axis2 = S2.axes_manager.signal_axes[0]
        omax = axis.axis.max()  # define overlap range
        omin = axis2.axis.min()
        ocenter = (omax + omin) / 2  # center of overlap range
        # closest index to center of overlap first spectrum
        ind1 = axis.value2index(ocenter)
        # closest index to center of overlap second spectrum
        ind2 = axis2.value2index(ocenter)
        # Test that r is not too large
        if (axis.size - ind1 - 1) <= r:
            raise ValueError("`r` is too large")
        # calculate mean deviation over defined range ignoring nan/zero values
        init = np.empty(S2.isig[ind2 - r : ind2 + r].data.shape)
        init[:] = np.nan
        # Do scaling of following signals
        if scale:
            if (
                axis.axis[ind1 - r : ind1 + r] == axis2.axis[ind2 - r : ind2 + r]
            ).all():
                factor = np.nanmean(
                    np.ma.masked_invalid(
                        np.divide(
                            S1.isig[ind1 - r : ind1 + r].data,
                            S2.isig[ind2 - r : ind2 + r].data,
                            out=init,
                            where=S2.isig[ind2 - r : ind2 + r].data != 0,
                        )
                    ),
                    axis=-1,
                )
            else:  # interpolate to get factor at same positions
                ind2r1 = axis2.value2index(axis.axis[ind1 - r])
                ind2r2 = axis2.value2index(axis.axis[ind1 + r])
                f = interp1d(
                    axis2.axis[ind2r1 - 1 : ind2r2 + 1],
                    S2.isig[ind2r1 - 1 : ind2r2 + 1].data,
                    kind=kind,
                )
                factor = np.nanmean(
                    np.ma.masked_invalid(
                        np.divide(
                            S1.isig[ind1 - r : ind1 + r].data,
                            f(axis.axis[ind1 - r : ind1 + r]),
                            out=init,
                            where=S2.isig[ind2 - r : ind2 + r].data != 0,
                        )
                    ),
                    axis=-1,
                )
            if (factor < 0).any():
                raise ValueError(
                    "One of the signals has a negative mean"
                    " value in the overlapping range. Try to set"
                    " `scale=False` and `average=True`."
                )
            S2.data = (S2.data.T * factor).T  # scale 2nd spectrum by factor
        # Make sure the corresponding values are in correct order
        if axis.axis[ind1] >= axis2.axis[ind2]:
            ind2 += 1
            # for UniformDataAxis
        if (not "axis" in getfullargspec(DataAxis)[0]) or (
            axis.is_uniform and axis2.is_uniform
        ):
            # join axis vectors
            axis.size = axis.axis[: ind1 + 1].size + np.floor(
                (axis2.axis[-1] - axis.axis[ind1]) / axis.scale
            )
            # join data vectors interpolating to a common uniform axis
            if average:  # average over range
                if r == 1:
                    raise ValueError(
                        "Averaging can not be performed for r=1. "
                        "Set average=False or r>1."
                    )
                ind2r = axis2.value2index(axis.axis[ind1 - r])
                length = axis.axis[ind1 - r : ind1 + r].size
                grad = 1 / (length - 1)
                vect = np.arange(length)
                f = interp1d(
                    axis2.axis[ind2r - 1 :],
                    S2.isig[ind2r - 1 :].data,
                    kind=kind,
                )
                S1.data = np.hstack(
                    (
                        S1.isig[: ind1 - r].data,
                        (1 - grad * vect) * S1.isig[ind1 - r : ind1 + r].data
                        + grad * vect * f(axis.axis[ind1 - r : ind1 + r]),
                        f(axis.axis[ind1 + r :]),
                    )
                )
            else:  # just join at center of overlap
                f = interp1d(axis2.axis[ind2:], S2.isig[ind2:].data, kind=kind)
                S1.data = np.hstack(
                    (S1.isig[: ind1 + 1].data, f(axis.axis[ind1 + 1 :]))
                )
        else:  # for DataAxis/FunctionalDataAxis (non uniform)
            # convert FunctionalDataAxes or UniformDataAxis to DataAxes
            if hasattr(axis, "_expression") or axis.is_uniform:
                axis.convert_to_non_uniform_axis()
            # 2nd axis does not need to be converted, because it contains axis vector
            # join axis vectors
            axis.axis = np.hstack((axis.axis[: ind1 + 1], axis2.axis[ind2:]))
            axis.size = axis.axis.size
            if average:  # average over range
                f1 = interp1d(
                    S[i - 1].axes_manager.signal_axes[0].axis[ind1 - 1 : ind1 + r + 1],
                    S1.isig[ind1 - 1 : ind1 + r + 1].data,
                    kind=kind,
                )
                f2 = interp1d(
                    axis2.axis[ind2 - r - 1 : ind2 + 1],
                    S2.isig[ind2 - r - 1 : ind2 + 1].data,
                    kind=kind,
                )
                length1 = axis.axis[ind1 - r : ind1 + 1].size
                grad1 = 0.5 / (length1 - 1)
                vect1 = np.arange(length1)
                length2 = axis2.axis[ind2 : ind2 + r].size
                if length2 == 1:
                    grad2 = 0.5
                else:
                    grad2 = 0.5 + 0.5 / (length2 - 1)
                vect2 = np.arange(length2)
                S1.data = np.hstack(
                    (
                        S1.isig[: ind1 - r].data,
                        (1 - grad1 * vect1) * S1.isig[ind1 - r : ind1 + 1].data
                        + grad1 * vect1 * f2(axis.axis[ind1 - r : ind1 + 1]),
                        (1 - grad2 * vect2) * f1(axis2.axis[ind2 : ind2 + r])
                        + grad2 * vect2 * S2.isig[ind2 : ind2 + r].data,
                        S2.isig[ind2 + r :].data,
                    )
                )
            else:  # just join at center of overlap
                S1.data = np.hstack((S1.isig[: ind1 + 1].data, S2.isig[ind2:].data))
    return S1
