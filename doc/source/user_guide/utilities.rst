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


.. _spectral_map_utils:

Utilities for spectral maps
==============================

The function :py:meth:`~.signals.common_luminescence.CommonLumi.crop_edges`
removes the specified number of pixels from all four edges of a spectral map.
It is a convenience wrapper for the ``inav`` :external+hyperspy:ref:`method in
HyperSpy <signal.indexing>`.

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
============================

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

This function also works for non-linear axes. For the :external:py:class:`hyperspy.axes.FunctionalDataAxis`, the centroid is extrapolated based on the function used to create the non-uniform axis. For :external:py:class:`hyperspy.axes.DataAxis`, a linear interpolation between the axes points at the center of mass is assumed, but this behaviour can be changed with the `kwargs` of :external:py:meth:`scipy.interpolate.interp1d` function.

.. code-block:: python

    >>> s = lum.signals.LumiSpectrum([[[1, 2, 3, 2, 1, 0]]*2]*3)
    >>> s
    LumiSpectrum <2,3|5>

    >>> ax = s.axes_manager.signal_axes[0]
    >>> ax.offset = 200
    >>> ax.scale = 100

    >>> com = s.centroid()
    >>> com
    BaseSignal <2,3|>
    >>> com.data[0,0] 
    400.

.. Note::

    This function only works for a single peak. If you have multiple peaks, slice the signal beforehand or use the slice parameter (which follows the ``s.isig[:]`` convention).

.. Note::

    This function is good at identifying non-symmetric peaks with shoulders. Such changes would not be reflected in the peak maximum.
