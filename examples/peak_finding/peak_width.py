"""
Peak width (FWHM) after background subtraction
==============================================

This example uses :external:meth:`~hyperspy.api.signals.Signal1D.estimate_peak_width`
to estimate the full width at half maximum (FWHM) of a luminescence peak
after subtracting a constant background.
"""

# %%
import lumispy as lum

# Load and plot an example spectrum image.
s = lum.data.asymmetric_peak_map()
s.plot()

# %%
# Estimate a constant background in the 540-590 nm range and subtract it
# without interactive parameter selection.
corrected = s.remove_background(signal_range=(540.0, 590.0), background_type="Offset")

# Limit the analysis to the main emission band between 600 and 750 nm.
peak = corrected.isig[600.0:750.0]
width, left, right = peak.estimate_peak_width(return_interval=True)
width.metadata.Signal.quantity = "Peak width (nm)"

# %%
# Plot the estimated peak width.
width.plot(cmap="viridis")

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 3
# sphinx_gallery_end_ignore
