from unittest import TestCase

from lumispy.signals.luminescence_spectrum import LumiSpectrum
import numpy as np

backgrounds = [
    ([np.ones(50)], [np.zeros(50, dtype='float64')]),
    ([np.linspace(0, 49, num=50, dtype='float64'), np.ones(50)], [np.zeros(50, dtype='float64')]),
    ([np.linspace(0, 50, num=30, dtype='float64'), np.ones(30)], [np.zeros(50, dtype='float64')]),
]

error_backgrounds = [
    ([np.linspace(0, 49, num=10, dtype='float64'), np.ones(50)]),
    ([[1,1], [1,1], [1,1]]),
]

class TestLumiSpectrum(TestCase):

    def test_background_subtraction_from_file(self):
        s = LumiSpectrum(np.ones(50))
        for bkg, output in backgrounds:
            s2 = s.background_subtraction_from_file(bkg, inplace=False)
            s.background_subtraction_from_file(bkg, inplace=True)
            assert np.allclose(s.data, output)
            assert np.allclose(s2.data, output)

    def test_errors_raise(self):
        s = LumiSpectrum(np.ones(50))
        for bkg in error_backgrounds:
            self.assertRaises(Exception, s.background_subtraction_from_file, bkg)
        pass
