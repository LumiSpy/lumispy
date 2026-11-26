"""
Energy conversion
=================

This example shows how to convert the signal axis from wavelength to energy
using :meth:`~.signals.common_luminescence.CommonLumi.to_eV`. See the
:ref:`signal_axis` section of the user guide for details.
"""

# %%
import lumispy as lum

# Load an example spectrum image.
s = lum.data.asymmetric_peak_map()

# %%
# Plot the original spectrum and convert its signal axis from nm to eV.
# inplace=False preserves the original signal.
s.plot()
s_eV = s.to_eV(inplace=False)
s_eV.plot()

# %%
# The intensity is rescaled by the :ref:`jacobian` during conversion,
# which also increases the apparent noise at low energies in this example.
# The conversion also supports wavelength axes expressed in µm.

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 4
# sphinx_gallery_end_ignore
