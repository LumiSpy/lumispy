.. _utilities:

Utility functions
*****************

This section summarizes various useful functions implemented in LumiSpy.


.. _join_spectra:

Join spectra
==========

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
===========================

The function :py:meth:`~.signals.common_luminescence.CommonLumi.crop_edges`
removes the specified number of pixels from all four edges of a spectral map.
It is a convenience wrapper for the ``inav`` :external+hyperspy:ref:`method in
HyperSpy <signal.indexing>`.

.. code-block:: python

    >>> s.crop_edges(crop_px=2)

*[TODO: add possibility to crop different amounts of pixels on different sides]*


.. _unit_conversion:

Unit conversion
===============

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