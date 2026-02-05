"""
Region of Interest (ROI)
========================
This example demonstrates how to use ROIs from Hyperspy. ROIs are used to select a subset of the data for further analysis. It can be done interactively aswell as non interactively.
For more information about ROIs see the `documentation <HS_roi_>`__.

.. _HS_roi: https://hyperspy.org/hyperspy-doc/current/reference/api.roi.html#module-hyperspy.api.roi
.. _HS_plot_spectra: https://hyperspy.org/hyperspy-doc/current/reference/api.plot/index.html#hyperspy.api.plot.plot_spectra
"""

# %%
# Loading exemplementary data:
import hyperspy.api as hs
import lumispy as lum

s = lum.data.asymmetric_peak_map()

# %%
# Interactive ROI
# ---------------
#
# To use ROIs we first have to plot the signal. After that we can plot the ROI which will extract a line scan from the map.
line_roi1 = hs.roi.Line2DROI()  # define the ROI
s.axes_manager["x"].index = 20
s.axes_manager["y"].index = 10
s.plot()
# plot the ROI and extract the line scan
profile1 = line_roi1.interactive(s, color="red")

# %%
# Return value of the ROI
# -----------------------
#
# The ROI returns a BaseSignal containing the line scan, in this case its stored in ``profile``. The shape of the signal is determined by the type of ROI and the signal it is applied to.
# To plot all the spectra from the linescan we got, we can use `hs.plot.plot_spectra() <HS_plot_spectra_>`__.
hs.plot.plot_spectra(profile1)

# %%
# Non-Interactive ROI
# -------------------
#
# For non-interactove ROIs we have to specify the type of ROI we want to use. In this case we'll use
# ``Line2DROI(x1=, y1=, x2=, y2=, linewidth=)``.
# First we need to define the ROI:
line_roi2 = hs.roi.Line2DROI(1.08, 0.36, 0.76, 0.52, 0)
profile2 = line_roi2(s)
hs.plot.plot_spectra(profile2)

# %%
# sphinx_gallery_thumbnail_number = 4
