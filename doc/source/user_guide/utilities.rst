.. _utilities-label:

Utility functions
*****************

This section summarizes various useful functions implemented in LumiSpy.


.. _join_spectra-label:

Join spectra
============

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


.. _scale_normalize-label:

Scaling and normalizing signal data
===================================

For comparative plotting or a detailed analysis, the intensity of spectra may
need to be either scaled by the respective integration times or
normalized. The luminescence signal classes provide these functionalities in the
methods :py:meth:`~.signals.common_luminescence.CommonLumi.scale_by_exposure` and 
:py:meth:`~.signals.common_luminescence.CommonLumi.normalize`.

Both functions can operate directly on the signal (``inplace=True``), but as default
a new signal is returned.

The **scaling** function can use the ``integration_time`` (unit: seconds) provided in the
:ref:`metadata_structure` (`metadata.Acqusition_instrument.Detector.integration_time`).
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


.. _remove_negative-label:

Replacing negative data values
==============================

Log-scale plotting fails in the presence of negative values in the dataset 
(e.g. introduced after background removal). In this case, the utility function
:py:meth:`~.signals.common_luminescence.CommonLumi.remove_negative` replaces
all negative values in the data array by a ``basevalue`` (default ``basevalue=1``).
The default operational mode is ``inplace=False``.

.. code-block:: python

    >>> s.remove_negative(0.1)


.. _spectral_map_utils-label:

Utilities for spectral maps
===========================

The function :py:meth:`~.signals.common_luminescence.CommonLumi.crop_edges`
removes the specified number of pixels from all four edges of a spectral map.
It is a convenience wrapper for :external:py:meth:`hyperspy.signal.BaseSignal.inav`.

.. code-block:: python

    >>> s.crop_edges(crop_px=2)

TODO: add possibility to crop different amounts of pixels on different sides


.. _unit_conversion-label:

Unit conversion
===============

For convenience, LumiSpy provides functions that convert between different
units commonly used for the signal axis. Namely,

- :py:func:`~.utils.axes.nm2eV`
- :py:func:`~.utils.axes.eV2nm`
- :py:func:`~.utils.axes.nm2invcm`
- :py:func:`~.utils.axes.invcm2nm`

For the energy axis, the conversion uses the correct permittivity of air.


.. _grating_equation-label:

Solving the grating equation
============================

TODO: Add a paragraph about the functionality of
:py:func:`~.utils.axes.solve_grating_equation`
