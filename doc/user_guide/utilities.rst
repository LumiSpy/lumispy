.. _utilities:

Utility functions
*****************

This section summarizes various useful functions implemented in LumiSpy.

.. _join_spectra:

Join spectra
============

In case several spectra (or spectral images) where subsequently recorded for
different, but overlapping spectral windows, LumiSpy provides a utility
:func:`~.utils.axes.join_spectra` to merge these into a single spectrum. The 
main argument is a list of two or more spectral objects. Spectra are joined at
the centre of the overlapping range along the signal axis. To avoid steps in the
intensity, several parameters (see docstring: :func:`~.utils.axes.join_spectra`)
allow to tune the scaling of the later signals with respect to the previous ones.
By default, the scaling parameter is determined as average ratio between the two
signals in the range of +/- 50 pixels around the centre of the overlapping region.

.. code-block:: python

    >>> import lumispy as lum
    >>> s = lum.join_spectra([s1,s2])


.. _exporting_text_files:

Exporting text files
====================

LumiSpy includes a function :meth:`~.signals.luminescence_spectrum.LumiSpectrum.savetxt`
that exports the data of a signal object
(with not more than two axes) to a simple `.txt` (or `.csv`) file. Can facilitate
data transfer to other programs, but no metadata is included. By default,
the axes are saved as first column (and row in 2d case). Set ``axes=False`` to
save the data object only. The function can also ``transpose`` (default ``False``)
the dataset or take a custom ``fmt`` (default ``%.5f``) or delimiter (default
``\t``) string.

.. code-block:: python

    >>> import lumispy as lum
    >>> import numpy as np
    ...
    >>> # Spectrum:
    >>> S = lum.signals.LumiSpectrum(np.arange(5))
    >>> lum.savetxt(S, 'spectrum.txt')
    0.00000	0.00000
    1.00000	1.00000
    2.00000	2.00000
    3.00000	3.00000
    4.00000	4.00000
    ...
    >>> # Linescan:
    >>> L = lum.signals.LumiSpectrum(np.arange(25).reshape((5,5)))
    >>> lum.savetxt(L, 'linescan.txt')
    0.00000	0.00000	1.00000	2.00000	3.00000	4.00000
    0.00000	0.00000	5.00000	10.00000	15.00000	20.00000
    1.00000	1.00000	6.00000	11.00000	16.00000	21.00000
    2.00000	2.00000	7.00000	12.00000	17.00000	22.00000
    3.00000	3.00000	8.00000	13.00000	18.00000	23.00000
    4.00000	4.00000	9.00000	14.00000	19.00000	24.00000

.. _mathematical_utilities:

Mathematical routines
=====================

.. _unit_conversion:

Unit conversion
---------------

For convenience, LumiSpy provides functions that convert between different
units commonly used for the signal axis. Namely,

- :func:`~.utils.axes.nm2eV`
- :func:`~.utils.axes.eV2nm`
- :func:`~.utils.axes.nm2invcm`
- :func:`~.utils.axes.invcm2nm`

For the energy axis, the conversion uses the wavelength-dependent refractive
index of air.


.. _grating_equation:

Solving the grating equation
----------------------------

The function :func:`~.utils.axes.solve_grating_equation` (relationship between
wavelength and pixel position in the detector plane) follows the conventions
described in the tutorial from  `Horiba Scientific
<https://horiba.com/uk/scientific/products/optics-tutorial/wavelength-pixel-position>`_.



Cropping multiple signals in the navigation axis 
================================================

The function :func:`~.utils.signals.crop_edges`
removes a specified amount from the edges of a spectral map, from the edges inwards.
The amount can be given as an integer (pixels), a float (converted to indices), or
a string using HyperSpy’s fancy indexing syntax (e.g. ``rel0.1`` for 10% or 
``100 nm`` for 100 nm). See HyperSpy’s `indexing guide 
<https://hyperspy.org/hyperspy-doc/current/user_guide/signal/indexing.html>`_ for
details. It takes a list of `Signals` and cropping can happen uniformly on all sides
or by individually specifying the cropping range for each axis or each side. If the
navigation axes shape across the list of signals is different, all signals can be
rebinned to match the shape of the first signal in the list. It is a convenience
wrapper for the :external+hyperspy:ref:`inav method in HyperSpy <signal.indexing>`.
The function can also be called as ``s.crop_edges()`` on a single signal object.

.. code-block:: python

    >>> signals = [cl_map, sem_image]
    >>> signals
    [CLSpectrum <256,256|1024>, Signal1D <128,128|1>]
    >>> signals_cropped = lum.utils.crop_edges(signals, crop_range=5, rebin_nav=True)
    >>> signals_cropped
    [CLSpectrum <243,243|1024>, Signal1D <243,243|1>]
    
.. Note::

    Many scanning luminescence techniques result in artefacts at the edges of the scanned region.
    This function enables the same cropping of the navigation axis for a list of signals recorded in
    the same region to correct for such defect.