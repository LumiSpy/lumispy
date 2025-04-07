import numpy as np
from hyperspy.axes import FunctionalDataAxis


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

    # Check for the type of hyperspy.axis
    if type(signal_axis) == FunctionalDataAxis:
        xs = signal_axis.axis

    elif hasattr(signal_axis, "axis"):
        xs = signal_axis.axis

    elif type(signal_axis) in (list, np.ndarray, tuple):
        # Check for dimensionality
        if len(spectrum_intensities) != len(signal_axis):
            raise ValueError(
                f"The length of the spectrum array {len(spectrum_intensities)} must match "
                "the length of the wavelength array {len(signal_axis)}."
            )
        # Calculate value interpolating between index_com 0 and 1
        xs = np.array(signal_axis)
    else:
        raise ValueError("The parmeter `signal_axis` must be a HyperSpy Axis object.")

    com_val = np.sum(xs * spectrum_intensities) / np.sum(spectrum_intensities)
    return com_val
