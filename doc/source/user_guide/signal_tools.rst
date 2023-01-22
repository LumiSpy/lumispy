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

HyperSpy provides functions to find the positions of maxima or minima in a
dataset:

- :external+hyperspy:meth:`indexmax() <hyperspy.signal.BaseSignal.indexmax>` - 
  return the index of the maximum value along a given axis.
- :external+hyperspy:meth:`indexmin() <hyperspy.signal.BaseSignal.indexmin>` - 
  return the index of the minimum value along a given axis.
- :external+hyperspy:meth:`valuemax() <hyperspy.signal.BaseSignal.valuemax>` - 
  return the position/coordinates of the maximum value along a given axis in
  calibrated units.
- :external+hyperspy:meth:`valuemin() <hyperspy.signal.BaseSignal.valuemin>` - 
  return the position/coordinates of the minimum value along a given axis in
  calibrated units.

These functions take the ``axis`` keyword to define along which axis to perform
the operation and return a new signal containing the result.

A much more powerful method to identify peaks is using the **peak finding routine**
based on the downward zero-crossings of the first derivative of a signal:
:external+hyperspy:meth:`find_peaks1D_ohaver() <hyperspy._signals.signal1d.Signal1D.find_peaks1D_ohaver>`.
This function can find multiple peaks in a dataset and has a number of parameters
for fine-tuning the sensitivity, etc.

All of these functions can be performed for a subset of the dataset:

.. code-block:: python

    >>> peaks = s.find_peaks1D_ohaver()
    >>> peaks = s.isig[100:-100].find_peaks1D_ohaver()

.. _peak_width:

Peak Width
----------

For asymmetric peaks, :ref:`fitted functions <fitting_luminescence>` may not provide
an accurate description of the peak, in particular the peak width. The function
:external+hyperspy:meth:`estimate_peak_width() <hyperspy._signals.signal1d.Signal1D.estimate_peak_width>`
determines the **width of a peak** at a certain fraction of its maximum value. The
default value ``factor=0.5`` returns the full width at half maximum (FWHM).

.. code-block:: python

    >>> s.remove_background()
    >>> width = s.estimate_peak_width(factor=0.3)


.. _centroid:

Calculating the centroid of a spectrum (centre of mass)
-------------------------------------------------------


The function :py:meth:`~.signals.luminescence_spectrum.LumiSpectrum.centroid`
(based on the utility function :py:func:`~.utils.signals.com`) is an alternative to
finding the position of the maximum intensity of a peak, useful in particular for
non-symmetric peaks with pronounced shoulders.
It finds the centroid (center of mass) of a peak in the spectrum from the signal axis
units (or pixel number) and the intensity at each pixel value. It basically represents a
"weighted average" of the peak as such:

.. math::

    com = \frac{\sum{x_i I_i}}{\sum{I_i}},

where :math:`x_i` is the wavelength (or pixel number) at which the
intensity of the spectrum :math:`I_i` is measured.

This function also works for non-linear axes. For the
:external:py:class:`hyperspy.axes.FunctionalDataAxis`, the centroid is extrapolated
based on the function used to create the non-uniform axis. For
:external:py:class:`hyperspy.axes.DataAxis`, a linear interpolation between the
axes points at the center of mass is assumed, but this behaviour can be changed
with the `kwargs` of :external:py:meth:`scipy.interpolate.interp1d` function.

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

    This function only works for a single peak. If you have multiple peaks,
    slice the signal beforehand or use the slice parameter (which follows the
    ``s.isig[:]`` convention).

.. Note::

    The :ref:`jacobian` may affect the shape, in particular of broader peaks.
    It is therefore highly recommended to convert luminescence spectra from
    wavelength to the :ref:`energy axis <energy_axis>` prior to determining
    the centroid to determine the true emission energy.
    See e.g. [Wang]_ and [Mooney]_.

Signal statistics and analytical operations
===========================================

**Standard statistical operations** can be performed on the data or a subset of the
data, notably these include 
:external+hyperspy:meth:`max() <hyperspy.signal.BaseSignal.max>`,
:external+hyperspy:meth:`min() <hyperspy.signal.BaseSignal.min>`,
:external+hyperspy:meth:`sum() <hyperspy.signal.BaseSignal.sum>`,
:external+hyperspy:meth:`mean() <hyperspy.signal.BaseSignal.mean>`,
:external+hyperspy:meth:`std() <hyperspy.signal.BaseSignal.std>`, and
:external+hyperspy:meth:`var() <hyperspy.signal.BaseSignal.var>`. Variations of
all these functions exist that ignore missing values (NaN) if present, e.g.
:external+hyperspy:meth:`nanmax() <hyperspy.signal.BaseSignal.mnanax>`.

**Integration** along a specified signal axis is performed using the function 
:external+hyperspy:meth:`integrate1D() <hyperspy.signal.BaseSignal.integrate1D()>`.

The numerical **derivative** of a signal can be calculated using the function
:external+hyperspy:meth:`derivative() <hyperspy.signal.BaseSignal.derivative()>`,
while the *n*-th order **discrete difference** can be calculated using
:external+hyperspy:meth:`diff() <hyperspy.signal.BaseSignal.diff()>`.

These functions take the ``axis`` keyword to define along which axis to perform
the operation and return a new signal containing the result:

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
