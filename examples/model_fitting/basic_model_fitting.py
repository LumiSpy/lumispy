"""
Basic model fitting
===================

This example fits an asymmetric luminescence peak using a HyperSpy model
with a SkewNormal component and a constant background.
"""

# %%
import hyperspy.api as hs
import lumispy as lum

# Load an example spectrum image and create a model.
s = lum.data.asymmetric_peak_map()
m = s.create_model()

# %%
# Use SkewNormal for the asymmetric peak and Offset for the background.
# Fix the offset at 5 so that it remains constant during fitting.
peak = hs.model.components1D.SkewNormal(x0=650)
background = hs.model.components1D.Offset(offset=5.0)
m.append(peak)
m.append(background)
background.offset.free = False
m.components
m.print_current_values()

# %%
# Fit the spectrum at the current navigation position.
m.fit()
m.plot()
m.print_current_values()

# %%
# Fit all spectra in the map and plot the fitted peak amplitude.
m.multifit()
peak.A.as_signal().plot(cmap="viridis")


# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 2
# sphinx_gallery_end_ignore
