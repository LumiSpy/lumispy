"""
Remove a measured dark background
=================================

This example shows how to remove a measured dark spectrum using the
``Scalable fixed pattern`` background model added in HyperSpy 2.5.0.
"""

# %%
# Load the experimental AlN spectrum and the measured dark background.
import lumispy as lum

s = lum.data.AlN_Cornell()
bkg = lum.data.AlN_bkg()

s.plot()

# %%
# Subtract the measured background without scaling it. ``signal_range='full'``
# enables non-interactive background removal over the complete spectrum.
# A different integration time or acquisition setting might require scaling.
corrected = s.remove_background(
    signal_range="full",
    background_type="Scalable fixed pattern",
    background_signal=bkg,
    yscale=False,
)

corrected.plot()
