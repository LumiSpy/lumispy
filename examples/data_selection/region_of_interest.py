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

s1 = lum.data.asymmetric_peak_map()
s2 = lum.data.nanoparticles()

# %%
# Interactive ROI
# ---------------
#
# To use ROIs we first have to plot the signal. After that we can plot the ROI which will extract a line scan from the map.
line_roi1 = hs.roi.Line2DROI()  # define the ROI
s1.axes_manager.indices = (20, 10)
s1.plot()
# plot the ROI and extract the line scan
profile1 = line_roi1.interactive(s1, color="red")

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
profile2 = line_roi2(s1)
hs.plot.plot_spectra(profile2)

# %%
# Circle ROI
# ----------
#
# We can also use a circle ROI. The circle ROI is defined by its center and radius. See more ROIs in the `documentation <HS_roi_>`__.

# get axes
ax1 = s2.axes_manager[0]
ax2 = s2.axes_manager[1]

# define start params
cx = 7 * ax1.scale + ax1.offset
cy = 7 * ax2.scale + ax2.offset
r = 5 * ((ax1.scale + ax2.scale) / 2)

# define the ROI
circle_roi = hs.roi.CircleROI(cx=cx, cy=cy, r=r)

# plot the ROI and extract the spectra
s2.axes_manager.indices = (7, 7)
s2.plot()
profile3 = circle_roi.interactive(s2)
hs.plot.plot_spectra(profile3)

# %%
# sphinx_gallery_thumbnail_number = 7
