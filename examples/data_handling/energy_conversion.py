"""
Energy Conversion
=================
This example demonstrates the usage of the energy conversion function ``to_eV``. For the documentation see `doc <LS_energy_conversion_>`__.

.. _LS_energy_conversion: https://docs.lumispy.org/en/stable/user_guide/signal_axis.html
.. _LS_to_eV: https://docs.lumispy.org/en/stable/user_guide/signal_axis.html
"""

# %%
# Load exemplementary data
import lumispy as lum
import numpy as np

s1 = lum.data.nanoparticles()  # unit nm
s2 = lum.data.asymmetric_peak_map()  # unit μm

# %%
# Transforming nm to eV
# ---------------------
# The signal can be transformed from nm to eV using the ``to_eV`` function. To see the implementation see `doc <LS_to_eV>`__.
s1.axes_manager["x"].index = 7
s1.axes_manager["y"].index = 7
s1.plot()  # original signal in nm

s1.data = s1.data.astype(np.float64, copy=False)  # preventing overflow in cast
s1_eV = s1.to_eV(inplace=False)  # conversion to eV
s1_eV.axes_manager["x"].index = 7
s1_eV.axes_manager["y"].index = 7
s1_eV.plot()  # transformed signal in eV

# %%
# Transforming μm to eV
# ---------------------
# The signal can aswell be transformet from μm to eV using the ``to_eV`` function.
s2.plot()  # original signal in μm
s2_eV = s2.to_eV(inplace=False)
s2_eV.plot()  # transformed signal in eV
