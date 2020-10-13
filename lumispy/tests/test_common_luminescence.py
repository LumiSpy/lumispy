from unittest import TestCase
import numpy as np
import pytest

from lumispy.signals.luminescence_spectrum import LumiSpectrum
from lumispy.signals.luminescence_transient import LumiTransient

class TestCommonLumi(TestCase):

    # @pytest.mark.parametrize(
    #     "nav_x, nav_y, output",
    #     [
    #         (10, 10, (6,6)),
    #         (10, 15, (6,11)),
    #         (2, 2, ValueError("The pixels to be cropped cannot be larger than half the width or the length!"))
    #     ]
    # )
    #def test_crop_edges(self, nav_x, nav_y, output):
    def test_crop_edges(self):
        s1 = LumiSpectrum(np.ones((10, 10, 10)))
        s2 = LumiTransient(np.ones((10, 10, 10, 10)))
        s3 = LumiSpectrum(np.ones((3,3,10)))
        s1 = s1.crop_edges(crop_px=2)
        s2 = s2.crop_edges(crop_px=2)
        assert s1.axes_manager.navigation_shape[0] == 6
        assert s1.axes_manager.navigation_shape[1] == 6
        assert s2.axes_manager.navigation_shape[0] == 6
        assert s2.axes_manager.navigation_shape[1] == 6
        #TestCase.assertRaises(ValueError, lambda:s3.crop_edges(2))