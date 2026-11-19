"""
Compare nanoparticle spectra using circular ROIs
================================================

This example uses :external:class:`~hyperspy.api.roi.CircleROI` to select two
nanoparticles in a cathodoluminescence spectrum image and compare their mean
spectra.

Other ROI types are demonstrated in the `HyperSpy ROI gallery
<https://hyperspy.org/hyperspy-doc/current/auto_examples/region_of_interest/index.html>`__.
For a line profile, see :ref:`sphx_glr_auto_examples_plotting_extraction_of_linescan.py`.
"""

# %%
import hyperspy.api as hs
import lumispy as lum

# Load a cathodoluminescence spectrum image of nanoparticles.
s = lum.data.nanoparticles()

# %%
# Select the 480-550 nm emission band for the navigator. Display the spectrum
# at a position with high intensity in this range instead of the default (0, 0).
selected = s.isig[480.0:550.0]
selected.axes_manager.indices = (16, 10)

# %%
# Define two circular ROIs at pixel positions (15, 14) and (7, 7), each with
# a radius of five pixels. ROIs use calibrated coordinates, so convert the
# pixel indices using the navigation axes.
ax_x, ax_y = s.axes_manager.navigation_axes
radius = 5 * min(abs(ax_x.scale), abs(ax_y.scale))
centers = [(15, 14), (7, 7)]
rois = [
    hs.roi.CircleROI(cx=ax_x.index2value(px), cy=ax_y.index2value(py), r=radius)
    for px, py in centers
]

# Plot the selected spectral range and display both ROIs on the navigator.
selected.plot()
rois[0].add_widget(selected, color="tab:blue")
rois[1].add_widget(selected, color="tab:orange")

# %%
# Apply the ROIs to the original signal to extract the full spectra.
# Pixels outside the circles are set to NaN; nanmean() ignores these values.
mean_1 = rois[0](s).nanmean()
mean_2 = rois[1](s).nanmean()

# Plot the two mean spectra for comparison.
hs.plot.plot_spectra([mean_1, mean_2], legend=["ROI 1", "ROI 2"])

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 2
# sphinx_gallery_end_ignore
