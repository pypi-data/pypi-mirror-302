"""Test the package."""

import muffler
import numpy


def test_linear_regression():
    sample_num = 100
    sample_len = 1024
    rng = numpy.random.default_rng(42)

    freq = sample_len / 64
    x = numpy.linspace(0, 2 * numpy.pi * freq, sample_len)
    sin_wave = numpy.sin(x)

    noise = rng.normal(0, 0.2, (sample_num, sample_len))
    samples = (sin_wave + noise).astype(numpy.float32)

    window_size = 100
    stride = 20
    denoised = muffler.denoise_linear_regression(samples, window_size, stride)

    assert denoised.shape == samples.shape

    rmse = numpy.mean(numpy.sqrt(numpy.mean((denoised - sin_wave) ** 2, axis=1)))
    assert rmse < 0.2, f"Test error: {rmse:2e}"


def test_decision_tree():
    sample_num = 100
    sample_len = 1024
    rng = numpy.random.default_rng(42)

    freq = sample_len / 64
    x = numpy.linspace(0, 2 * numpy.pi * freq, sample_len)
    sin_wave = numpy.sin(x)

    noise = rng.normal(0, 0.2, (sample_num, sample_len))
    samples = (sin_wave + noise).astype(numpy.float32)

    window_size = 100
    stride = 20
    denoised = muffler.denoise_decision_tree(samples, window_size, stride)

    assert denoised.shape == samples.shape

    rmse = numpy.mean(numpy.sqrt(numpy.mean((denoised - sin_wave) ** 2, axis=1)))
    assert rmse < 0.2, f"Test error: {rmse:2e}"
