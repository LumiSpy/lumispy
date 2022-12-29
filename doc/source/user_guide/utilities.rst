.. _utilities:

Utility functions
*****************

This section summarizes various useful functions implemented in LumiSpy.


.. _join_spectra:

Join spectra
==============================

In case several spectra (or spectral images) where subsequently recorded for
different, but overlapping spectral windows, LumiSpy provides a utility
:py:func:`~.utils.axes.join_spectra` to merge these into a single spectrum. The 
main argument is a list of two or more spectral objects. Spectra are joined at
the centre of the overlapping range along the signal axis. To avoid steps in the
intensity, several parameters (see docstring: :py:func:`~.utils.axes.join_spectra`)
allow to tune the scaling of the later signals with respect to the previous ones.
By default, the scaling parameter is determined as average ratio between the two
signals in the range of +/- 50 pixels around the centre of the overlapping region.

.. code-block:: python

    >>> import lumispy as lum
    >>> s = lum.join_spectra((s1,s2))


.. _scale_normalize:

Scaling and normalizing signal data
==============================

For comparative plotting or a detailed analysis, the intensity of spectra may
need to be either scaled by the respective integration times or
normalized. The luminescence signal classes provide these functionalities in the
methods :py:meth:`~.signals.common_luminescence.CommonLumi.scale_by_exposure` and 
:py:meth:`~.signals.common_luminescence.CommonLumi.normalize`.

Both functions can operate directly on the signal (``inplace=True``), but as default
a new signal is returned.

The **scaling** function can use the ``integration_time`` (unit: seconds) provided in the
:ref:`metadata_structure` (``metadata.Acqusition_instrument.Detector.integration_time``).
Otherwise, the appropriate parameter has to be passed to the function.

.. code-block:: python

    >>> scaled = s.scale_by_exposure(integration_time=0.5, inplace=True)

**Normalization** is performed for the pixel with maximum intensity, Alternatively,
the parameter ``pos`` in calibrated units of the signal axis can be given to
normalize the intensity at this position. Normalization may be convenient for
plotting, but should usually not be performed on signals used as input for further
analysis (therefore the default is ``inplace=False``). 

.. code-block:: python

    >>> s.normalize(pos=450)


.. _remove_negative:

Replacing negative data values
==============================

Log-scale plotting fails in the presence of negative values in the dataset 
(e.g. introduced after background removal). In this case, the utility function
:py:meth:`~.signals.common_luminescence.CommonLumi.remove_negative` replaces
all negative values in the data array by a ``basevalue`` (default ``basevalue=1``).
The default operational mode is ``inplace=False`` (a new signal object is returned).

.. code-block:: python

    >>> s.remove_negative(0.1)


.. _spectral_map_utils:

Utilities for spectral maps
==============================

The function :py:meth:`~.signals.common_luminescence.CommonLumi.crop_edges`
removes the specified number of pixels from all four edges of a spectral map.
It is a convenience wrapper for the ``inav`` `method in HyperSpy
<https://hyperspy.org/hyperspy-doc/current/user_guide/signal.html#indexing>`_.

.. code-block:: python

    >>> s.crop_edges(crop_px=2)

*[TODO: add possibility to crop different amounts of pixels on different sides]*


.. _unit_conversion:

Unit conversion
==============================

For convenience, LumiSpy provides functions that convert between different
units commonly used for the signal axis. Namely,

- :py:func:`~.utils.axes.nm2eV`
- :py:func:`~.utils.axes.eV2nm`
- :py:func:`~.utils.axes.nm2invcm`
- :py:func:`~.utils.axes.invcm2nm`

For the energy axis, the conversion uses the wavelength-dependent refractive
index of air.


.. _grating_equation:

Solving the grating equation
==============================


The function :py:func:`~.utils.axes.solve_grating_equation` follows the
conventions described in the tutorial from 
`Horiba Scientific <https://horiba.com/uk/scientific/products/optics-tutorial/wavelength-pixel-position>`_.


.. _centroid:

Calculating the centroid of a spectrum (centre of mass)
==============================


The function :py:meth:`~.signals.luminescence_spectrum.LumiSpectrum.centroid` (based on the utility function :py:func:`~.utils.signals.com`) is an alternative to finding the max intensity of a peak.
It finds the centroid (center of mass) of a peak in the spectrum from the wavelength (or pixel number) and the intensity at each pixel value. It basically represents a "weighted average" of the peak as such:

.. math::

    com = \frac{\sum{x_i I_i}}{\sum{I_i}},

where :math:`x_i` is the wavelength (or pixel number) at which the intensity of the spectrum :math:`I_i` is measured.

.. code-block:: python

    >>> s = lum.signals.LumiSpectrum([[[1, 2, 3, 2, 1, 0]]*2]*3)
    >>> s
    LumiSpectrum <2,3|5>

    >>> ax = s.axes_manager.signal_axes[0]
    >>> ax.offset = 200
    >>> ax.scale = 100

    >>> com = s.centroid()
    >>> com
    LumiSpectrum <2,3|1>
    >>> com.data[0,0] 
    400.

.. Note::

    This function only works for a single peak. If you have multiple peaks, slice the signal beforehand or use the slice parameter (which follows the ``s.isig[:]`` convention).

.. Note::

    This function is good at identifying non-symmetric peaks with shoulders. Such changes would not be reflected in the peak maximum.
