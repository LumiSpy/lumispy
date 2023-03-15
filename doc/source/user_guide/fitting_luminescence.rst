.. _fitting_luminescence:

Fitting luminescence data
*************************

LumiSpy is compatible with :external+hyperspy:ref:`HyperSpy model fitting 
<user_guide/model>`.
It can fit using both :external+hyperspy:ref:`uniform and and non-uniform axes
<Axes_types>`_ 
(e.g. energy scale). A general introduction can be found in the
:external+hyperspy:ref:`HyperSpy user guide <user_guide/model>`.

.. Note::
    The :ref:`jacobian` may affect the shape, in particular of broader peaks.
    It is therefore highly recommended to convert luminescence spectra from
    wavelength to the :ref:`energy axis <energy_axis>` prior to any fitting
    to obtain the true emission energy.
    See e.g. [Wang]_ and [Mooney]_.

TODO: Show how to extract the *modeled signal* with all/one component.

See also the `LumiSpy demo notebooks <https://github.com/LumiSpy/lumispy-demos>`_
for examples of data fitting.

.. _fitting_variance:

Signal variance (noise)
=======================

TODO: Documentation on variance handling in the context of fitting,
in particular using :external:py:meth:`estimate_poissonian_noise_variance()
<hyperspy.signal.BaseSignal.estimate_poissonian_noise_variance>`
 
See [Tappy]_
