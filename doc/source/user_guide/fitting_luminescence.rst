.. _fitting_luminescence:

Fitting luminescence data
*************************

LumiSpy is compatible with `HyperSpy model fitting 
<https://hyperspy.org/hyperspy-doc/current/user_guide/model.html>`_.
It can fit using both `uniform and and non-uniform axes
<https://hyperspy.org/hyperspy-doc/current/user_guide/axes.html#types-of-data-axes>`_ 
(e.g. energy scale). A general introduction can be found in the `HyperSpy user guide
<https://hyperspy.org/hyperspy-doc/current/user_guide/model.html>`_.

TODO: Note on advantages of fitting signals in the ``eV`` axis (not restricted
to Gaussians). See e.g. [Wang]__

TODO: Show how to extract the *modeled signal* with all/one component.

See also the `LumiSpy demo notebooks <https://github.com/LumiSpy/lumispy-demos>`_
for examples of data fitting.

.. _fitting_variance:

Signal variance (noise)
=======================

TODO: Documentation on variance handling in the context of fitting,
in particular using :external:py:meth:`hyperspy.signal.BaseSignal.estimate_poissonian_noise_variance()`

.. rubric:: References

.. [Wang]_ Y. Wang and P. D. Townsend, J. Luminesc. **142**, 202
    (2013). `doi:10.1016/j.jlumin.2013.03.052 <https://doi.org/10.1016/j.jlumin.2013.03.052>`_

