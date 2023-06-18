import numpy as np
import pytest
from numpy.testing import assert_allclose
from lumispy.utils.signals import com
from hyperspy.axes import FunctionalDataAxis, DataAxis, UniformDataAxis


@pytest.mark.parametrize(
    "axis, output",
    [
        (
            FunctionalDataAxis(
                **{
                    "expression": "a * x + b",
                    "a": 1,
                    "b": 0,
                },
                size=2
            ),
            0.5,
        ),
        (DataAxis(axis=[0.0, 1.0]), 0.5),
        (UniformDataAxis(size=2), 0.5),
    ],
)
def test_com_axes(axis, output):
    intensities = np.array([1, 1])

    centroid = com(intensities, axis)
    assert_allclose(centroid, output, atol=0.1)


def test_com_list():
    # Float without decimals as index for centroid
    wavelengths = [200, 300, 400, 500, 600, 700]
    intensities = np.array([1, 2, 3, 2, 1, 0])
    centroid = com(intensities, wavelengths)
    assert_allclose(centroid, 400.0, atol=0.1)

    # Float with decimals as index for centroid
    wavelengths = [
        200,
        300,
    ]
    intensities = np.array(
        [
            1,
            1,
        ]
    )
    centroid = com(intensities, wavelengths)
    assert_allclose(centroid, 250.0, atol=0.1)


def test_com_inputs():
    with pytest.raises(ValueError, match="The length of the spectrum array"):
        com(np.ones(2), np.ones(3))
    with pytest.raises(ValueError):
        com(np.ones(3), np.ones(2))
    with pytest.raises(
        ValueError, match="The parmeter `signal_axis` must be a HyperSpy Axis object."
    ):
        com(np.ones(3), "string")
