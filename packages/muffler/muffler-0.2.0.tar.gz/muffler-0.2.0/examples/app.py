"""Muffler: Denoising Algorithms for Time Series Data."""

import time

import data  # type: ignore[import]
import muffler
import numpy
import plots  # type: ignore[import]
import streamlit as st

st.title("Muffler")

sample_num = 100
sample_len = 1024 * 4

freq_choices = [
    0.25,
    0.5,
    1.0,
    *list(map(float, range(2, 10, 2))),
    *list(map(float, range(10, 41, 5))),
]
amp_range = (1.0, 10.0)
offset_range = (-0.25 * numpy.pi, 0.25 * numpy.pi)

x = numpy.linspace(0, 2 * numpy.pi, sample_len)
clean, noisy = data.random_signals(
    x=x,
    num_samples=sample_num,
    freq_choices=freq_choices,
    amp_range=amp_range,
    off_range=offset_range,
    noise_std=0.25,
    add_linear_trend=True,
)

# Run the denoising algorithms
window_size = 100
stride = 20

st.write(f"Running the denoising algorithm with {window_size = } and {stride = } ...")
start = time.perf_counter()
denoised = muffler.denoise_linear_regression(noisy, window_size, stride)
time_taken = time.perf_counter() - start
st.write(
    f"Denoising took {time_taken:.3f} seconds for {sample_num} samples of "
    f"length {sample_len}.",
)

# plot the sine wave
st.write("Plotting the signals ...")
figs, clean_v_noisy, clean_v_denoised = plots.plot_signals(1, noisy, denoised, clean)
for fig in figs:
    st.plotly_chart(fig)

# plot the frequency distribution of errors
st.write(f"Mean error: noisy vs clean: {numpy.mean(clean_v_noisy):.2e}")
st.write(f"Mean error: denoised vs clean: {numpy.mean(clean_v_denoised):.2e}")
fig = plots.plot_errors(clean_v_noisy, clean_v_denoised)
st.plotly_chart(fig)
