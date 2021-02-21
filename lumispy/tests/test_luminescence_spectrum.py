from unittest import TestCase
import numpy as np
from lumispy.signals.luminescence_spectrum import LumiSpectrum
import warnings

backgrounds = [
    ([np.ones(50)], [np.zeros(50, dtype='float64')]),
    ([np.linspace(0, 49, num=50, dtype='float64'), np.ones(50)], [np.zeros(50, dtype='float64')]),
    ([np.linspace(0, 50, num=30, dtype='float64'), np.ones(30)], [np.zeros(50, dtype='float64')]),
    (LumiSpectrum(np.ones(50)), [np.zeros(50, dtype='float64')]),
]

error_backgrounds = [
    ([np.linspace(0, 49, num=10, dtype='float64'), np.ones(50)], AttributeError),
    ([[1, 1], [1, 1], [1, 1]], AttributeError),
]


class TestLumiSpectrum(TestCase):

    def test_remove_background_from_file(self):
        for bkg, output in backgrounds:
            s = LumiSpectrum(np.ones(50))
            s2 = s.remove_background_from_file(bkg, inplace=False)
            s.remove_background_from_file(bkg, inplace=True)
            assert np.allclose(s.data, output)
            assert np.allclose(s2.data, output)
            assert s.metadata.Signal.background_subtracted is True
            assert hasattr(s.metadata.Signal, 'background')

    def test_errors_raise(self):
        s = LumiSpectrum(np.ones(50))
        for bkg, error in error_backgrounds:
            self.assertRaises(error, s.remove_background_from_file, bkg)
        # Test that a GUI is opened if s.remove_background_from_file is passed without a background
        # s.remove_background_from_file()
        # Test double background removal
        s.remove_background_from_file(backgrounds[0][0], inplace=True)
        self.assertRaises(RecursionError, s.remove_background_from_file, backgrounds[0][0])

