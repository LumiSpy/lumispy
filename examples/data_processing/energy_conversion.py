"""
Energy Conversion
=================
This example demonstrates the usage of the energy conversion function 
:meth:`~.signals.common_luminescence.CommonLumi.to_eV`.

.. _LS_to_eV: https://docs.lumispy.org/en/stable/user_guide/signal_axis.html
"""

# %%
# Load exemplary data:
import lumispy as lum

s = lum.data.asymmetric_peak_map()

# %%
# The signal can be transformed from nm to eV using the 
# :meth:`~.signals.common_luminescence.CommonLumi.to_eV` 
# function. To see the implementation see `doc <LS_to_eV_>`__.
s.plot()  # original signal in nm
s_eV = s.to_eV(inplace=False)  # conversion to eV
s_eV.plot()  # plot transformed signal in eV

# %%
# In this example, the noise at low energies increases as the intensity is corrected by a :ref:`jacobian`.
# A signal axis with the units μm to eV using the :meth:`~.signals.common_luminescence.CommonLumi.to_eV` function.

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 4
# sphinx_gallery_end_ignore
