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
    >>> s = lum.utils.join_spectra((s1,s2))


.. _spectral_map_utils:

Cropping multiple signals in the navigation axis 
================================================

The function :py:meth:`~.utils.axes.crop_edges`
removes the specified number of pixels or % from the four edges of a spectral map,
from the edges inwards. It takes a list of `Signals` and cropping can happen
uniformly on all sides or by specifying the cropping range for each axis or each
side. If the navigation axes shape across the list of signals is different, all
signals can be rebinned to match the shape of the first signal in the list.
It is a convenience wrapper for the ``inav`` `method in HyperSpy
<https://hyperspy.org/hyperspy-doc/current/user_guide/signal.html#indexing>`_.

.. code-block:: python

    >>> signals = [cl_map, sem_image]
    >>> signals
    [CLSpectrum <256,256|1024>, Signal2D <128,128|1>]
    >>> signals_cropped = lum.utils.crop_edges(signals, crop_range=5, crop_units="%", rebin_nav=True)
    >>> signals_cropped
    [CLSpectrum <243,243|1024>, Signal2D <243,243|1>]

.. Note::

    Many scanning luminescence techniques result in edge defects at the edges of the scanned region.
    This function enables the same cropping of the navigation axis for a list of signals in the same
    region to correct for such defect.

.. Note::

    Before version `0.2.2` this function belonged to the class `CommonLumi` as :py:meth:`~.signals.common_luminescence.CommonLumi.crop_edges`. This use is now deprecated.
