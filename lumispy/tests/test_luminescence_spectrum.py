from unittest import TestCase

from lumispy.signals.luminescence_spectrum import LumiSpectrum
import numpy as np
from lumispy.signals.luminescence_spectrum import LumiSpectrum

backgrounds = [
    ([np.ones(50)], [np.zeros(50, dtype='float64')]),
    ([np.linspace(0, 49, num=50, dtype='float64'), np.ones(50)], [np.zeros(50, dtype='float64')]),
    ([np.linspace(0, 50, num=30, dtype='float64'), np.ones(30)], [np.zeros(50, dtype='float64')]),
    (LumiSpectrum([np.ones(50)]), [np.zeros(50, dtype='float64')]),
]

error_backgrounds = [
    ([np.linspace(0, 49, num=10, dtype='float64'), np.ones(50)]),
    ([[1, 1], [1, 1], [1, 1]]),
]


class TestLumiSpectrum(TestCase):

    def test_remove_background(self):
        s = LumiSpectrum(np.ones(50))
        for bkg, output in backgrounds:
            s2 = s.remove_background(bkg, inplace=False)
            s.remove_background(bkg, inplace=True)
            assert np.allclose(s.data, output)
            assert np.allclose(s2.data, output)
            assert s.metadata.Signal.background_subtracted is True
            assert hasattr(s.metadata.Signal, 'background')

    def test_errors_raise(self):
        s = LumiSpectrum(np.ones(50))
        for bkg in error_backgrounds:
            self.assertRaises(Exception, s.remove_background(), bkg)
        pass
