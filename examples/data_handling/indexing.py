"""
Indexing
========
Indexing is achieved using `inav <HS_inav_>`__ or `isig <HS_isig_>`__, which allows the navigation- and signalaxes to be accessed independently.
The index operation returns a view of the original signal.

.. _HS_inav: https://hyperspy.org/hyperspy-doc/current/reference/api.signals/BaseSignal.html#hyperspy.api.signals.BaseSignal.inav
.. _HS_isig: https://hyperspy.org/hyperspy-doc/current/reference/api.signals/BaseSignal.html#hyperspy.api.signals.BaseSignal.isig
.. _HS_uniform_axis: https://hyperspy.org/hyperspy-doc/current/reference/base_classes/axes.html#hyperspy.axes.UniformDataAxis
"""

import hyperspy.api as hs
import numpy as np

# %%
# Creating a small example signal
# --------------------------------
#
# We create a simple ``Signal1D`` with a total shape of ``(2, 3, 4)``:
#
# - navigation shape: ``(2, 3)``
# - signal shape: ``(4,)``
s = hs.signals.Signal1D(np.linspace(1, 24, 24).reshape(2, 3, 4))
s.data

# %%
# Indexing navigation axes using `inav <HS_inav_>`__
# ---------------------------------------
#
# The signal contains two navigation axes, both of which can be accessed independently or together.

# Indexing the first navigation axis:
s.inav[0].data

# %%
# Indexing the second navigation axis:
#
# When accessing the second navigation axis, the first must still be addressed explicitly.
s.inav[:, 0].data

# %%
# Accessing both navigation axes:
s.inav[0, 0].data

# %%
# Indexing signal axes using `isig <HS_isig_>`__
# -----------------------------------
# The signal axis can be indexed independently of the navigation axes.
s.isig[0].data

# %%
# Combining navigation and signal indexing
# ----------------------------------------
#
# Navigation and signal indexing can be combined by chaining `inav <HS_inav_>`__ and `isig <HS_isig_>`__ operations.
s.inav[2, 1].isig[0].data

# %%
# Indexing using Physical units
# -----------------------------
#
# Hyperspy supports indexing with physical units (floating-point) values when the corresponding axis is calibrated. This is achieved using the `scale <HS_uniform_axis_>`__ and `offset <HS_uniform_axis_>`__ attributes of the axis.
s.axes_manager[-1].scale = 0.5

# the scale gives us the new indices for indexing
s.axes_manager[-1].axis

# %%
# Indexing the signal axis using physical units:
s.isig[0.5:1.5].data

# %%
# Importantly the original signal and its "indexed self" share their data and, therefore, modifying the value of the data in one modifies the same value in the other:
s.isig[0].data[0, 0] = 42
s.data

# %%
# More on indexing with inav and isig can be found in the `Hyperspy documentation <https://hyperspy.org/hyperspy-doc/current/user_guide/signal/indexing.html>`__.
