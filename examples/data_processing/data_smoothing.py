"""
Data Smoothing
==============

This example shows how to smooth a dataset.
"""

# %%
# Load the data
import lumispy as lum

cl1 = lum.data.asymmetric_peak_map()
cl1 = cl1.remove_background(signal_range=(550.0, 620.0), background_type="Offset")
cl1 = cl1.isig[:-3]
cl1.spikes_removal_tool(interactive=False)

cl2 = cl1.deepcopy()
cl3 = cl1.deepcopy()

# %%
# Display the original data

cl1.inav[0, 0].plot()

# %%
# The current dataset is quite noisy.
# One way to improve that is by smoothing the data using :py:meth:`hyperspy.api.signals.Signal1D.smooth_lowess`
# (see docstring for detailed explanation of the parameters).

cl1.smooth_lowess(smoothing_parameter=0.1, number_of_iterations=2)

cl1.inav[0, 0].plot()

# %%
# Another algorithm which can be used is :py:meth:`hyperspy.api.signals.Signal1D.smooth_savitzky_golay`.
#
# This way is often better to maintain the shape of the peaks, but it can be less efficient in removing noise.

cl2.smooth_savitzky_golay(window_length=11, polynomial_order=3)

cl2.inav[0, 0].plot()

# %%
# Also :py:meth:`hyperspy.api.signals.Signal1D.smooth_tv` can be used.
#
# This method is very efficient in removing noise while preserving the edges of the peaks.

cl3.smooth_tv(smoothing_parameter=10.0)

cl3.inav[0, 0].plot()

# To evaluate optimum parameters, each of the algorithms is run interactively if at least one parameter is missing in
# the function call and thus the result of the smoothing can be directly previewed while adapting the parameters.

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 4
# sphinx_gallery_end_ignore
