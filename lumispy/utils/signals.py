import numpy as np
from hyperspy.axes import FunctionalDataAxis
from scipy.ndimage import center_of_mass
from scipy.interpolate import interp1d


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
