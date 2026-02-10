"""
Basic Model Fitting
====================
In this Example we will give a brief introduction to model fitting in Lumispy/Hyperspy.
"""

# %%
# Load examplary data
import hyperspy.api as hs
import lumispy as lum

s = lum.data.asymmetric_peak_map()

# %%
# First we need to initialize the model:
m = s.create_model()

# %%
# A Hyperspy model can be composed of multiple components (functions).
# To take a look at the components of the model we can use ``m.components``.
m.components

# %%
# Since we dont hav any yet, we need to create some components and add them to the model.
# Since we have an asymmetric peak, we will use a single SkewNormal component.
# For successful Fit we need to pass the center wavelength ``x0=650nm`` [#f1]_.
g = hs.model.components1D.SkewNormal(x0=650)
# Alternative way to set the start value of x0:
# g.x0.value = 650
m.append(g)
m.components

# %%
# To see the parameters of our components and their values, we can print all parameter values:
m.print_current_values()

# %%
# To apply the fit, we can use the ``fit()`` function. In this case it will only be using the current index for fitting.
# The fit for the other spectra will be the same. If you want to apply the fit to all spectra of the map, you can use ``multifit()`` instead.
m.fit()

# %%
# We can now plot the model together with the data:
m.plot()

# %%
# After we applied the fit, we can again print the fitted parameter at the current index:
m.print_current_values()

# %%
# If we used ``multifit()``, we could aswell return the fitted parameter as Signal objects.
m.multifit()
g.A.as_signal().plot(cmap="viridis")

# %%
# sphinx_gallery_thumbnail_number = 2
#
# .. [#f1] Note that Hyperspy has a range of built-in functions covering most needs that can be addedd as components to a model. However, it aslo has an intuitive mechanism to define custom functions.
