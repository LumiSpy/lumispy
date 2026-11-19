"""
Remove a measured dark background
=================================

This example demonstrates subtraction of a measured dark spectrum with the
:external:meth:`~hyperspy.api.signals.Signal1D.remove_background` method
and the ``Scalable fixed pattern`` background model (HyperSpy >= 2.5).
"""

# %%
# Load the experimental AlN spectrum image and the measured dark background
# (single spectrum).
import lumispy as lum

s = lum.data.AlN_Spectrum()
bkg = lum.data.AlN_bkg()

# %%
# Show an experimental spectrum at navigation position (9, 1), where the
# AlN emission is particularly intense.
s.inav[9, 1].plot()

# %%
# Subtract the measured background at every position without scaling it.
# ``signal_range='full'`` enables non-interactive subtraction across the
# complete spectrum. ``yscale=False`` is already the default; it is shown
# explicitly to emphasize that no additional scale factor is fitted.
# Different acquisition settings may require background scaling.
corrected = s.remove_background(
    signal_range="full",
    background_type="Scalable fixed pattern",
    background_signal=bkg,
    yscale=False,
)

# Compare with the corrected spectrum at the same navigation position.
corrected.inav[9, 1].plot()

# %%
# Show the measured dark background used for the subtraction.
bkg.plot()

# sphinx_gallery_start_ignore
# sphinx_gallery_thumbnail_number = 2
# sphinx_gallery_end_ignore
