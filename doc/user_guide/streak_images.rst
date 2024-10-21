.. _streak_images:

Working with streak images
**************************

LumiSpy has implemented handling of streak camera images, which are a special
subclass of :class:`hyperspy.api.signals.Signal2D` as the two signal axes have
different units: Namely, wavelength (or energy) and time. The signal class is 
:class:`~.signals.luminescence_transientspec.LumiTransientSpectrum`. An important
feature is that also for streak camera images (or linescans/maps of these), the
wavelength axis can be transformed to e.g. a :ref:`energy_axis`.

.. Note::

    For streak images, not all tools available for :class:`hyperspy.api.signals.Signal2D`
    will work. However, in particular
    :external+hyperspy:ref:`peak_finding-label`
    can be helpful to identify local maxima in the images.


Transition to one-dimensional signals
=====================================

When transitioning from a streak image to a one-dimensional signal, LumiSpy
uses the axes units of the new signal (whether it is time units or not) to
assign the correct 1D signal class: Either :class:`~.signals.luminescence_spectrum.LumiSpectrum` or
:class:`~.signals.luminescence_transient.LumiTransient`. Such a reduction of the signal dimensionality
can be done for example by slicing the signal with
:external+hyperspy:ref:`numpy-style indexing <signal.indexing>` or by using
functions such as :external:meth:`~hyperspy.api.signals.BaseSignal.sum`
and :external:meth:`~hyperspy.api.signals.BaseSignal.integrate1D`

In the following image, the spectrum summed over all times is obtained from the
streak image by:

.. code-block:: python

    >>> import lumispy as lum
    >>> import numpy as np
    ...
    >>> data = np.arange(10*20).reshape(10, 20)
    ...
    >>> s = lum.signals.LumiTransientSpectrum(data)
    >>> s.axes_manager[-1].name = "Time"
    >>> s.axes_manager[-1].units = "ns"
    >>> s.axes_manager[-2].name = "Wavelength"
    >>> s.axes_manager[-2].units = "nm"
    >>> s.sum(axis='Time')
    >>> # Or alternatively:
    >>> s.sum(axis=-1)

Similarly, the transient summed over all wavelengths is obtained by:

.. code-block:: python

    >>> s.sum(axis='Wavelength')
    >>> # Or alternatively:
    >>> s.sum(axis=-2)

.. image:: images/streakmap.svg
  :width: 700
  :alt: Plot of a streak camera image and its one-dimensional representations
        obtained by summing over either the wavelength or time dimensions.
