import numpy as np


def com(spectrum_intensities, wavelengths):
    """Finds the centroid (center of mass) of a peak in the spectrum from the wavelength (or pixel number) and the intensity at each pixel value.
    Parameters
    ----------
    spectrum_intensities : array
        An array with the intensities of the spectrum.
    wavelengths: array
        An array with the wavelength for each intensity value.

    Returns
    -------
    center_of_mass : float
        The centroid of the spectrum.

    Examples
    --------
    # Assume we have a spectrum with wavelengths and intensities
    >>> wavelengths = [200, 300, 400, 500, 600, 700]
    >>> intensities = [1, 2, 3, 2, 1, 0]

    >>> center_of_mass = com(wavelengths, intensities)
    >>> print(center_of_mass)  # Outputs: [400.0]
    """
    if len(spectrum_intensities) != len(wavelengths):
        raise ValueError(
            f"The length of the spectrum array {len(spectrum_intensities)} must match the length of the wavelength array {len(wavelengths)}."
        )

    wavelengths = np.array(wavelengths)
    intensities = np.array(spectrum_intensities)
    center_of_mass = np.sum(wavelengths * intensities) / np.sum(intensities)
    return [center_of_mass]
