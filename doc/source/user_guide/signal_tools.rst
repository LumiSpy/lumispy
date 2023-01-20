.. _signal_tools:

Signal tools
************

This section summarizes functions operating on the signal data. Besides those
implemented in LumiSpy, it highlights functions from HyperSpy that are
particularly useful for luminescence spectroscopy data.


.. _scale_normalize:

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

.. _peak_props:

Peak positions and properties
=============================

.. _find_peaks:

Peak identification
-------------------

HyperSpy provides functions to finde the positions of maxima or minima in a
dataset:

- ``indexmax()`` - return the index of the maximum value along a given axis.
- ``indexmin()`` - return the index of the minimum value along a given axis.
- ``valuemax()`` - return the position of the maximum value along a given axis in
  calibrated units.
- ``valuemin()`` - return the position of the minimum value along a given axis in
  calibrated units.

These functions take the `axis` keyword to define along which axis to perform the
operation.

A much more powerful method to identify peaks is using the peak finding routine
based on the downward zero-crossings of the first derivative of a signal:
:external+hyperspy:meth:`find_peaks1D_ohaver <hyperspy._signals.signal1d.Signal1D.find_peaks1D_ohaver>`.

All of these functions can be performed for a subset of the dataset:

.. code-block:: python

    >>> peaks = s.find_peaks1D_ohaver()
    >>> peaks = s.isig[100:-100].find_peaks1D_ohaver()

.. _peak_width:

Peak Width
----------

For asymmetric peaks, `fitted functions <fitting_luminescence>` may not provide
an accurate description of the peak, in particular the peak width. The function
:external+hyperspy:meth:`estimate_peak_width <hyperspy._signals.signal1d.Signal1D.estimate_peak_width>`
determines the width of a peak at a certain fraction of its maximum value.


Signal statistics and analytical operations
===========================================

Standard statistical operations can be performed on the data or a subset of the
data, notably these include ``max``, ``min``, ``sum``, ``mean``, ``std``, ``var``.

Integration along a specified signal axis is performed using the function 
``integrate1D()``.

These functions take the ``axis`` keyword to define along which axis to perform the
operation.

.. code-block:: python

    >>> area = s.integrate1D(axis=0)

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

