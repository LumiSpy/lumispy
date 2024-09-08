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

