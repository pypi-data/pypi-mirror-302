"""Time Series De-noising."""

from . import muffler  # type: ignore[import]

denoise_linear_regression = muffler.denoise_linear_regression
denoise_decision_tree = muffler.denoise_decision_tree


__all__ = [
    "denoise_linear_regression",
    "denoise_decision_tree",
]
