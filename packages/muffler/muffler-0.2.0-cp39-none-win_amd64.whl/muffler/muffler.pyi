"""Type stubs for the package."""

import numpy
import numpy.typing as npt


def denoise_linear_regression(
    samples: npt.NDArray[numpy.float32],
    window_size: int,
    stride: int,
) -> npt.NDArray[numpy.float32]:
    """Denoise a set of time-series samples using linear regression.

    Args:
        samples: The time-series samples to denoise.
        window_size: The size of the window to use for linear regression.
        stride: The distance between adjacent window start points.
    """


def denoise_decision_tree(
    samples: npt.NDArray[numpy.float32],
    window_size: int,
    stride: int,
) -> npt.NDArray[numpy.float32]:
    """Denoise a set of time-series samples using decision trees.

    Args:
        samples: The time-series samples to denoise.
        window_size: The size of the window to use for linear regression.
        stride: The distance between adjacent window start points.
    """
