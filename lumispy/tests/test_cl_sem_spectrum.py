from unittest import TestCase

import pytest
import numpy as np

from lumispy.signals.cl_sem_spectrum import CLSEMSpectrum

param_list = [(1e-10, 1e-10, 1e-10, 10, 10),
              (1e-10, 1e-10, 1e-10, 20, 10),
              (1e-10, 1e-10, 1e-10, 10, 20),]

class TestCLSEMSpectrum(TestCase):

    def test_correct_grating_shift(self):
        for calx, corg, fov, nx, ny in param_list:
            with self.subTest():
                s = CLSEMSpectrum(np.ones((nx, ny, 100)) * np.random.random())
                garray = np.arange((-corg / 2) * calx / (fov * nx) * 1000 * nx,
                                   (corg / 2) * calx / (fov * nx) * 1000 * nx,
                                   corg * calx / (fov * nx) * 1000)
                barray = np.full((ny, nx), garray)
                s2 = s.deepcopy()
                s.correct_grating_shift(calx, corg, fov)
                s2.shift1D(barray)
                assert np.allclose(s2.data, s.data)

    def test_double_correct_grating_shift(self):
        s = CLSEMSpectrum(np.ones((10, 10, 10)))
        s.correct_grating_shift(1e-10, 1e-10, 1e-10)
        self.assertRaises(Exception, s.correct_grating_shift, 1, 1, 1)

