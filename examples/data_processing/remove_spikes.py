"""
Remove Spikes
=============

This example shows how to remove spikes (e.g. from cosmic rays impacting a CCD detector) from a dataset.
"""

# %%
# Load the data
import lumispy as lum

cl1 = lum.data.asymmetric_peak_map()
cl1 = cl1.remove_background(signal_range=(550.0, 620.0), background_type="Offset")
cl1 = cl1.isig[:-3]

# %%
# Display the original data

cl1.inav[29, 0].plot()

# %%
# As seen there is a heavy spike, so lets remove it
# (in an interactive environment, the parameters for spike identification can be adapted and the proposed removal previewed and confirmed for each identified spike individually, see :py:meth:`hyperspy.api.signals.Signal1D.spikes_removal_tool`).

cl1.spikes_removal_tool(interactive=False)

# %%
# Display cleaned data

cl1.inav[29, 0].plot()

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 2
# sphinx_gallery_end_ignore
