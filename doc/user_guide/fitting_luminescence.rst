.. _fitting_luminescence:

Fitting luminescence data
*************************

LumiSpy is compatible with :external+hyperspy:ref:`HyperSpy model fitting 
<model-label>`.
It can fit using both :external+hyperspy:ref:`uniform and and non-uniform axes
<Axes_types>` 
(e.g. energy scale). A general introduction can be found in the
:external+hyperspy:ref:`HyperSpy user guide <model-label>`.

A detailed example is given in the ``Fitting_tutorial`` in the 
`HyperSpy demos repository <https://github.com/hyperspy/hyperspy-demos>`_.
See also the `LumiSpy demo notebooks <https://github.com/LumiSpy/lumispy-demos>`_
for examples of data fitting.

.. Note::
    The :ref:`jacobian` may affect the shape, in particular of broader peaks.
    It is therefore highly recommended to convert luminescence spectra from
    wavelength to the :ref:`energy axis <energy_axis>` prior to any fitting
    to obtain the true emission energy.
    See e.g. [Wang]_ and [Mooney]_.

TODO: Show how to extract the *modeled signal* with all/one component.



.. _fitting_variance:

Signal variance (noise)
=======================

TODO: Documentation on variance handling in the context of fitting,
in particular using :external:meth:`estimate_poissonian_noise_variance()
<hyperspy.api.signals.BaseSignal.estimate_poissonian_noise_variance>`
 
For a detailed discussion, see [Tappy]_
