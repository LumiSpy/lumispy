import numpy as np
import pytest
from numpy.testing import assert_allclose
from lumispy.utils.signals import com


def test_com():
    wavelengths = [200, 300, 400, 500, 600, 700]
    intensities = [1, 2, 3, 2, 1, 0]

    centroid = com(intensities, wavelengths)
    assert_allclose(centroid, 400.0, atol=0.1)


def test_com_inputs():
    with pytest.raises(ValueError):
        com(np.ones(2), np.ones(3))
    with pytest.raises(ValueError):
        com(np.ones(3), np.ones(2))
