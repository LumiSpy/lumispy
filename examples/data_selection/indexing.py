"""
Indexing
========
Indexing is achieved using :py:attr:`~hyperspy.api.signals.BaseSignal.inav` or :py:attr:`~hyperspy.api.signals.BaseSignal.isig`, which allows the
navigation and signal axes to be accessed independently. The index operation returns a
copy of the original signal.

.. _HS_inav: https://hyperspy.org/hyperspy-doc/current/reference/api.signals/BaseSignal.html#hyperspy.api.signals.BaseSignal.inav
.. _HS_isig: https://hyperspy.org/hyperspy-doc/current/reference/api.signals/BaseSignal.html#hyperspy.api.signals.BaseSignal.isig
.. _HS_uniform_axis: https://hyperspy.org/hyperspy-doc/current/reference/base_classes/axes.html#hyperspy.axes.UniformDataAxis
"""

import hyperspy.api as hs
import numpy as np

# %%
# Creating a small example signal
# -------------------------------
#
# We create a simple :py:class:`~hyperspy.api.signals.Signal1D` with axes shape of ``(2, 3, 4)``:
#
# - navigation shape: ``(3, 2)``
# - signal shape: ``(4,)``
s = hs.signals.Signal1D(np.linspace(1, 24, 24).reshape(2, 3, 4))
s.data

# %%
# Indexing navigation axes using :py:attr:`~hyperspy.api.signals.BaseSignal.inav` 
# -------------------------------------------------------------------------------
#
# The signal contains two navigation axes, both of which can be accessed independently or together.

# Indexing the first navigation axis:
s.inav[0].data

# %%
# Indexing the second navigation axis
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# When accessing the second navigation axis, the first must still be addressed explicitly.
s.inav[:, 0].data

# %%
# Accessing both navigation axes:
s.inav[0, 0].data

# %%
# Indexing signal axes using :py:attr:`~hyperspy.api.signals.BaseSignal.isig`
# ---------------------------------------------------------------------------
# The signal axis can be indexed independently of the navigation axes.
# To show a little bit better how this works exactly, we will use a signal where we can
# see a bit better what we are doing.
x = np.linspace(0, 2 * np.pi, 1000)
y = np.sin(x)
s_sin = hs.signals.Signal1D(
    y, axes=[{"scale": x[1] - x[0], "offset": x[0], "size": x.size, "name": "x"}]
)
s_sin.plot()
# sphinx_gallery_start_ignore
# This is purely for visualization purpose only and doesnt effect the outcome
import matplotlib.pyplot as plt

ax = plt.gca()
ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
ax.set_xticklabels(
    [r"$0$", r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$", r"$2\pi$"]
)
ax.axvspan(0, np.pi, alpha=0.3, label="selected region")
ax.legend()
plt.draw()
# sphinx_gallery_end_ignore
# Indexing the signal axis:
s_sin.isig[0 : np.pi].plot()  # this is the same as s_sin.isig[0:500]
# sphinx_gallery_start_ignore
# This is purely for visualization purpose only and doesnt effect the outcome
ax = plt.gca()
ax.set_xticks([0, np.pi / 2, np.pi])
ax.set_xticklabels([r"$0$", r"$\frac{\pi}{2}$", r"$\pi$"])
# sphinx_gallery_end_ignore

# %%
# Combining navigation and signal indexing
# ----------------------------------------
#
# Navigation and signal indexing can be combined by chaining
# :py:attr:`~hyperspy.api.signals.BaseSignal.inav` and :py:attr:`~hyperspy.api.signals.BaseSignal.isig` operations.
s.inav[2, 1].isig[0].data

# %%
# Indexing using physical units
# -----------------------------
#
# Hyperspy supports indexing with physical units (floating-point) values when the
# corresponding axis is calibrated. This is achieved using the
# :py:attr:`~hyperspy.axes.UniformDataAxis.scale` attribute of the
# axis, for :py:class:`~hyperspy.axes.UniformDataAxis`. For non-uniform axes you would just use the values of the axis.
s.axes_manager[-1].scale = 0.5

# the scale gives us the new indices for indexing
s.axes_manager[-1].axis

# %%
# Indexing the signal axis using physical units:
s.isig[0.5:1.5].data

# %%
# Importantly the original signal and its "indexed self" share their data and,
# therefore, modifying the value of the data in one modifies the same value in the
# other:
s.inav[0, 0].isig[0] = 42
s.data

# %%
# More on indexing with :py:attr:`~hyperspy.api.signals.BaseSignal.inav`
# and :py:attr:`~hyperspy.api.signals.BaseSignal.isig` can be found in the HyperSpy
# `documentation <https://hyperspy.org/hyperspy-doc/current/user_guide/signal/indexing.html>`__.

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail = 2
# sphinx_gallery_end_ignore
