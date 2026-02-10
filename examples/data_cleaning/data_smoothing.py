"""
Data Smoothing
==================

This example shows how to smooth a dataset.
"""

# %%
# Load the data
import lumispy as lum

cl1 = lum.data.asymmetric_peak_map()
cl1 = cl1.remove_background(signal_range=(550.0, 620.0), background_type="Offset")
cl1 = cl1.isig[:-3]
cl1.spikes_removal_tool(interactive=False)

cl3 = lum.data.asymmetric_peak_map()
cl3 = cl3.remove_background(signal_range=(550.0, 620.0), background_type="Offset")
cl3 = cl3.isig[:-3]
cl3.spikes_removal_tool(interactive=False)

# %%
# Display the original data

cl1.inav[0, 0].plot()

# %%
# The current dataset is quite noisy. As the peak is broad in comparison with the spectral resolution.
# One way to improve that is by rebinning the data along the signal axis:

cl2 = cl1.rebin(scale=[1, 1, 2])

# %%
# Display the smoothed data

cl2.inav[0, 0].plot()

# %%
# Another way to smooth

cl3.smooth_lowess(smoothing_parameter=0.1, number_of_iterations=2)

# %%
# Display the data

cl3.inav[0, 0].plot()

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 3
# sphinx_gallery_end_ignore
