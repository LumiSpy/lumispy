"""
Advanced Model Fitting
======================
In this example, we will demonstrate further model fitting techniques.
"""

# %%
# First we load the data and convert it to eV. Aswell as create the model.
import hyperspy.api as hs
import lumispy as lum
import numpy as np

s = lum.data.nanoparticles()
s.data = s.data.astype(np.float64)
s.to_eV()

m = s.create_model()

# %%
# Now we initialize the models components.
bkg = hs.model.components1D.Offset()
g = hs.model.components1D.GaussianHF()
m.extend([g, bkg])
m.components

# %%
# Next we will set some starting points for our components.
# You could also use the estimate parameters function of the ``GaussianHF`` component.
# However, this approach does not work as well as using manual starting points.
s.axes_manager.indices = (7, 7)  # position where we know that there should be a signal.
g.centre.value = 2.4  # Gaussian centre
g.fwhm.value = 0.1  # Gaussian width
g.height.value = 5  # Gaussian height
bkg.offset.value = 0.1  # background offset

# %%
# We can also set boundaries (``bmin`` and ``bmax``) for some of the parameters.
g.centre.bmax = g.centre.value + 0.2
g.centre.bmin = g.centre.value - 0.2
g.fwhm.bmin = 0.01

# %%
# We can now fit the model at the current position.
# Fitting for a single pixel allows to optimize the starting parameters and boundaries
# before we run the more time consuming fit on all parameters.
# To apply the boundaries we set ``bounded=True``.
m.fit(bounded=True)
m.assign_current_values_to_all()
m.plot()

# %%
# The Model has now the result from our choosen pixel everywhere. Since we now have optimized our starting point, we can now fit all pixels.
m.multifit(bounded=True)  # you can show a progrssbar with ``show_progressbar=True``
m.plot(plot_components=True)  # Plot the individual components

# %%
# We now can plot maps of the Gaussian parameters.
m_centre = g.centre.as_signal()
m_centre.plot(
    cmap="bwr_r", centre_colormap=False  # Otherwise, it would be centred around `0`
)
m_intensity = g.height.as_signal()
m_intensity.plot(cmap="viridis")

# %%
# sphinx_gallery_thumbnail_number = 2
