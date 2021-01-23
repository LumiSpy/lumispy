from unittest import TestCase
from lumispy.signals.cl_spectrum import CLSpectrum
import numpy as np

param_list_signal_mask = [
    ([900, 500], [False, False, False,  True,  True,  True,  True,  True,  True, False]),
    ([[500, 100],[700,1]],[False,  True,  True, False,  True, False, False, False, False, False]),
    ([[200, 100], [600, 300]], [ True,  True,  True,  True,  True, False, False, False, False, False]),
]


class TestCLSpectrum(TestCase):

    def test__make_signal_mask(self):
        s = CLSpectrum(np.ones(10))
        s.axes_manager.signal_axes[0].scale = 100.5
        s.axes_manager.signal_axes[0].offset = 300
        for peak_list, mask_test in param_list_signal_mask:
            mask = s._make_signal_mask(peak_list)
            assert np.allclose(mask, mask_test)

    def test_remove_spikes(self):
        pass
