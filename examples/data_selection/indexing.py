"""
Indexing navigation and signal axes
===================================

HyperSpy provides :py:attr:`~hyperspy.api.signals.BaseSignal.inav` and
:py:attr:`~hyperspy.api.signals.BaseSignal.isig` to index navigation and
signal axes independently. The syntax is similar to NumPy array indexing.
See the `HyperSpy indexing guide
<https://hyperspy.org/hyperspy-doc/current/user_guide/signal/indexing.html>`__
for further details.
"""

# %%
import hyperspy.api as hs
import matplotlib.pyplot as plt
import numpy as np

# Create a signal with two navigation axes and one signal axis.
s = hs.signals.Signal1D(np.linspace(1, 24, 24).reshape(2, 3, 4))
# The navigation shape is (3, 2), and the signal shape is (4,).
s.data

# %%
# Indexing navigation axes
# ------------------------
#
# Select the first element along the first navigation axis. The signal axis
# remains unchanged.
s.inav[0].data

# %%
# Select the first element of the second navigation axis instead.
s.inav[:, 0].data

# %%
# Select a single navigation position.
s.inav[0, 0].data

# %%
# Select a range along the first navigation axis at a fixed position on the
# second axis.
s.inav[1:3, 0].data

# %%
# Indexing with calibrated axis values
# ------------------------------------
#
# Create a calibrated sine wave.
x = np.linspace(0, 2 * np.pi, 1000)
s_sin = hs.signals.Signal1D(
    np.sin(x),
    axes=[
        {
            "scale": x[1] - x[0],
            "offset": x[0],
            "size": x.size,
            "name": "Angle",
            "units": "rad",
        }
    ],
)

# Integer slice bounds are indices.
by_index = s_sin.isig[0:500]

# Floating-point slice bounds are calibrated axis values, here radians.
by_units = s_sin.isig[0.0 : np.pi]

# An illustrative highlight: the Matplotlib shading is added separately
# for this figure; it is not part of the isig operation itself.
fig, ax = plt.subplots()
ax.plot(x, np.sin(x))
ax.axvspan(0, np.pi, alpha=0.25, label="Selected range: 0 to pi rad")
ax.set(xlabel="Angle (rad)", ylabel="sin(angle)")
ax.legend()

# Both slices select approximately the first half of the signal.
by_index.plot()
by_units.plot()

# %%
# Combining navigation and signal slicing
# ---------------------------------------
#
# Navigation and signal axes can be indexed consecutively.
s.inav[2, 1].isig[0].data

# Sliced signals may share their underlying NumPy data with the original.
# In-place changes to one array can therefore affect the other.
np.shares_memory(s.data, s.inav[0, 0].data)

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 1
# sphinx_gallery_end_ignore
