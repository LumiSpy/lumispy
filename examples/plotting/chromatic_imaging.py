"""
Chromatic Imaging
==================

This example shows how to do a color-filtered (chromatic) imaging.
"""

# %%
# Load the data from a file
import lumispy as lum

cl1 = lum.data.nanoparticles()

cl1.mean().plot()

# %%
# First, lets plot the panchromatic image:
# (the object is transposed, so that we plot the intensity over navigation instead of signal dimensions)

cl1.T.mean().plot(cmap="viridis")

# %%
# Now, we can plot the intensity in a selected spectral window (color-filtered image) using indexing:

cl1.isig[480.0:550.0].T.mean().plot(cmap="viridis")

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 3
# sphinx_gallery_end_ignore
