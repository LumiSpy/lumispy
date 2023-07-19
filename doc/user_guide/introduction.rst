.. _HyperSpy: https://hyperspy.org
.. |HyperSpy| replace:: **HyperSpy** 

.. _introduction:

Introduction
************

What is LumiSpy
===============

**LumiSpy** is an open-source python library aimed at helping with the analysis
of luminescence spectroscopy data. The development started mainly with
photoluminescence (PL), cathodoluminescence (CL), electroluminescence (EL) and
Raman spectroscopy in mind. Besides the standard continuous-excitation spectral
data, the idea is to provide tools also for the analysis of time-resolved
(transient) measurements. However, LumiSpy may prove useful also for other optical
measurements, such as absorption or transmission spectroscopy, scanning optical
near field miscroscopy (SNOM), as well as fourier-transform infrared
spectroscopy (FTIR).

**LumiSpy** is an extension to the python package |HyperSpy|_
that facilitates hyperspectral data analysis, i.e. maps or linescans where a
spectrum is collected at each pixel. Or more general, multidimensional datasets
that can be described as multidimensional arrays of a given signal, as illustrated
by the following figure:

.. image:: images/hyperspy-datacube.svg
  :width: 700
  :alt: Illustration of hyperspectral datasets in different dimensionalities.

To facilitate working with these datasets, HyperSpy distinguishes between
`navigation and signal dimensions <https://hyperspy.org/hyperspy-doc/current/user_guide/getting_started.html#the-navigation-and-signal-dimensions>`_
that can be addressed separately and thus, for example, operations on a single
spectrum can be easily mapped to a whole dataset.

..
    Eith HyperSpy 2.0 update link above to :external+hyperspy:doc:`navigation and signal dimensions <navigation-signal-dimensions>`

Notable features that **HyperSpy** provides are:

- :external+hyperspy:doc:`base signal classes <user_guide/signal>`
  for the handling of (multidimensional) spectral data,
- the necessary tools for loading :external+hyperspy:ref:`various data file formats
  <io>`,
- :external+hyperspy:doc:`analytical tools <user_guide/signal1d>`
  that exploit the multidimensionality of datasets,
- a user-friendly and powerful framework for :external+hyperspy:ref:`model fitting
  <model-label>` that
  provides many standard functions and can be easily extended to custom ones,
- :external+hyperspy:ref:`machine learning <ml-label>`
  algorithms that can be useful, e.g. for denoising data,
- efficient handling of :external+hyperspy:ref:`big datasets <big-data-label>`,
- functions for :external+hyperspy:ref:`data visualization  <visualization-label>`
  both to evaluate datasets during the analysis and provide interactive
  operation for certain functions, as well as for plotting of data,
- extracting subsets of data from multidimensional datasets via 
  :external+hyperspy:ref:`regions of interest <roi-label>` and a powerful
  numpy-style :external+hyperspy:ref:`indexing mechanism <signal.indexing>`,
- handling of :external+hyperspy:ref:`non-uniform data axes <Axes_types>`
  (introduced in the :external+hyperspy:ref:`v1.7 release 
  <changes_1.7.0>`).

**LumiSpy** provides in particular:

- additional :ref:`signal_types` specifically for luminescence spectra and
  transients,
- transformation to :ref:`non-uniform signal axes <signal_axis>` for use of other
  common units, such as eV (electron volt) and wavenumbers (Raman shift),
- additional :ref:`signal tools <signal_tools>` such as data normalization and scaling,
- various :ref:`utility functions <utilities>` useful in luminescence spectroscopy
  data analysis, such as joining multiple spectra along the signal axis, 
  unit conversion, etc.

**LumiSpy** should facilitate an easy and reproducible analysis of single
spectra or spectral images.


.. _signal_types:

Signal types
============

As an extension to HyperSpy, LumiSpy provides several signal types extending the
:external+hyperspy:ref:`base classes available in HyperSpy
<signal_subclasses_table-label>`. When the LumiSpy library is installed, these
additional signal types are directly available to HyperSpy. To print all available
specialised :external:py:class:`hyperspy.signal.BaseSignal` subclasses installed
in your system call the :external:py:func:`hyperspy.utils.print_known_signal_types`
function:

.. code-block:: python

    >>> import hyperspy.api as hs
    >>> hs.print_known_signal_types()

The different subclasses are characterized by the ``signal_type`` metadata
attribute. Some additional properties are summarized in the table below.
Depending on the use case, certain functions will only be available for some
signal types (or inheriting) signal types.

.. _lumispy_subclasses_table:

.. table:: LumiSpy subclasses and their basic attributes.

    +-------------------------------------------------------------------------+------------------+---------------+---------+---------------------------------------------------------------------------+
    |  BaseSignal subclass                                                    | signal_dimension |  signal_type  |  dtype  |  aliases                                                                  |
    +=========================================================================+==================+===============+=========+===========================================================================+
    |  :py:class:`~.signals.luminescence_spectrum.LumiSpectrum`               |        1         |  Luminescence |  real   | LumiSpectrum, LuminescenceSpectrum                                        |
    +-------------------------------------------------------------------------+------------------+---------------+---------+---------------------------------------------------------------------------+
    |  :py:class:`~.signals.cl_spectrum.CLSpectrum`                           |        1         |       CL      |  real   | CLSpectrum, cathodoluminescence                                           |
    +-------------------------------------------------------------------------+------------------+---------------+---------+---------------------------------------------------------------------------+
    |  :py:class:`~.signals.cl_spectrum.CLSEMSpectrum`                        |        1         |     CL_SEM    |  real   | CLSEM, cathodoluminescence SEM                                            |
    +-------------------------------------------------------------------------+------------------+---------------+---------+---------------------------------------------------------------------------+
    |  :py:class:`~.signals.cl_spectrum.CLSTEMSpectrum`                       |        1         |    CL_STEM    |  real   | CLSTEM, cathodoluminescence STEM                                          |
    +-------------------------------------------------------------------------+------------------+---------------+---------+---------------------------------------------------------------------------+
    |  :py:class:`~.signals.el_spectrum.ELSpectrum`                           |        1         |       EL      |  real   | ELSpectrum, electroluminescence                                           |
    +-------------------------------------------------------------------------+------------------+---------------+---------+---------------------------------------------------------------------------+
    |  :py:class:`~.signals.pl_spectrum.PLSpectrum`                           |        1         |       PL      |  real   | PLSpectrum, photoluminescence                                             |
    +-------------------------------------------------------------------------+------------------+---------------+---------+---------------------------------------------------------------------------+
    |  :py:class:`~.signals.luminescence_transient.LumiTransient`             |        1         |   Transient   |  real   | TRLumi, TR luminescence, time-resolved luminescence                       |
    +-------------------------------------------------------------------------+------------------+---------------+---------+---------------------------------------------------------------------------+
    |  :py:class:`~.signals.luminescence_transientspec.LumiTransientSpectrum` |        2         | TransientSpec |  real   | TRLumiSpec, TR luminescence spectrum, time-resolved luminescence spectrum |
    +-------------------------------------------------------------------------+------------------+---------------+---------+---------------------------------------------------------------------------+

The hierarchy of the LumiSpy signal types and their inheritance from HyperSpy
is summarized in the following diagram:

|   └── :external:py:class:`hyperspy.signal.BaseSignal`
|       ├── :external:py:class:`hyperspy._signals.signal1d.Signal1D`
|       │   └── :py:class:`~.signals.luminescence_spectrum.LumiSpectrum`
|       │   │   ├── :py:class:`~.signals.cl_spectrum.CLSpectrum`
|       │   │   │   ├── :py:class:`~.signals.cl_spectrum.CLSEMSpectrum` 
|       │   │   │   └── :py:class:`~.signals.cl_spectrum.CLSTEMSpectrum` 
|       │   │   ├── :py:class:`~.signals.el_spectrum.ELSpectrum`
|       │   │   └── :py:class:`~.signals.pl_spectrum.PLSpectrum`
|       │   └── :py:class:`~.signals.luminescence_transient.LumiTransient`
|       └── :py:class:`hyperspy.signal.Signal2D`
|           └── :py:class:`~.signals.luminescence_transientspec.LumiTransientSpectrum`
|
|


Where are we heading?
=====================

LumiSpy is under active development, and as a user-driven project, we welcome
contributions (see :ref:`contributing_label`) to the code and documentation,
but also bug reports and feature requests from any users. Don't hesitate
to join the discussions!

Currrently, we have implemented the base functionality that extends 
:external+hyperspy:ref:`HyperSpy's capabilities <user_guide-label>`
to additional signal classes. In the near future, the following functions
should be developed:

- handling of transient (time-resolved) data,
- reading of common PL data formats (see :external+rsciio:ref:`supported-formats` of RosettaSciIO),
- more dedicated analysis functionalities,
- ...
