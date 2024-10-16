"""Generate various kinds of time series data for the examples."""


import numpy


def sine_wave(
    x: numpy.ndarray,
    freq: float,
    offset: float,
    amplitude: float,
) -> numpy.ndarray:
    """Generate a sine wave."""
    return amplitude * numpy.sin(freq * x + offset)


def summed_waves(
    x: numpy.ndarray,
    freq_off_amp: list[tuple[float, float, float]],
) -> numpy.ndarray:
    """Generate a sum of sine waves."""
    y = numpy.zeros_like(x)
    for freq, off, amp in freq_off_amp:
        y += sine_wave(x, freq, off, amp)
    return y


def random_signals(  # noqa: PLR0913
    *,
    x: numpy.ndarray,
    num_samples: int,
    freq_choices: list[float],
    amp_range: tuple[float, float],
    off_range: tuple[float, float],
    noise_std: float,
    add_linear_trend: bool = True,
) -> tuple[numpy.ndarray, numpy.ndarray]:
    """Generate several random signals.

    Args:
        x: The x-axis values.
        num_samples: The number of samples to generate.
        freq_choices: The frequencies to choose from.
        amp_range: The range of amplitudes to choose from.
        off_range: The range of offsets to choose from.
        noise_std: The standard deviation of the noise to add, relative to the
        strength of the signal.
        add_linear_trend: Whether to add a linear trend to the signal.

    Returns:
        A tuple of two arrays: the clean signals and the noisy signals.
    """
    rng = numpy.random.default_rng(42)
    num_choices = 8
    clean_signals: list[numpy.ndarray] = []
    noisy_signals: list[numpy.ndarray] = []
    for _ in range(num_samples):
        # Choose random frequencies
        freqs = list(map(float, rng.choice(freq_choices, num_choices, replace=False)))
        # Choose random amplitudes
        amps = list(map(float, rng.uniform(*amp_range, num_choices)))
        # Choose random offsets
        offs = list(map(float, rng.uniform(*off_range, num_choices)))
        # Generate the signal
        signal = summed_waves(x, list(zip(freqs, offs, amps)))

        min_val, max_val = signal.min(), signal.max()
        sign = 1 if len(clean_signals) % 2 == 0 else -1
        if not add_linear_trend:
            # Construct a linear trend, and add it to the signal
            diff = max_val - min_val
            linear = (numpy.linspace(0, diff, x.size, dtype=numpy.float32) + diff)
            signal += (sign * linear)
        else:
            offset = max(abs(min_val), abs(max_val)) * sign
            signal += offset

        clean_signals.append(signal)

        # Add some noise and multiply element-wise by the signal
        conditional_noise = numpy.abs(signal)
        noise = rng.normal(0, noise_std, x.shape) * conditional_noise
        noisy_signals.append(signal + noise)

    # join the list of arrays into a single array
    clean = numpy.array(clean_signals).astype(numpy.float32)
    noisy = numpy.array(noisy_signals).astype(numpy.float32)
    return clean, noisy
