"""Generate some plots for the streamlit demo."""

import numpy
import plotly.express as px
import plotly.graph_objects as go


def plot_signals(
    num: int,
    noisy: numpy.ndarray,
    denoised: numpy.ndarray,
    clean: numpy.ndarray,
) -> tuple[list[go.Figure], numpy.ndarray, numpy.ndarray]:
    """Plot the signals.

    Args:
        num: The number of signals to plot from each set.
        noisy: The noisy signals, a 2d array.
        denoised: The denoised signals, a 2d array.
        clean: The clean signals, a 2d array.

    Returns:
        The list of figures to display in the streamlit demo.
    """
    # Calculate the errors
    clean_v_noisy = numpy.sqrt(numpy.mean((clean - noisy) ** 2, axis=1))
    clean_v_denoised = numpy.sqrt(numpy.mean((denoised - clean) ** 2, axis=1))

    figs = []

    for i in range(num):
        if i >= noisy.shape[0]:
            break
        # On a single plot, show the noisy (red), denoised (blue), and clean (green)
        # signals as lines. Make the noisy signal thin.
        fig = px.line()
        fig.add_scatter(y=noisy[i], line={"color": "red", "width": 1}, name="noisy")
        fig.add_scatter(y=denoised[i], line={"color": "blue"}, name="denoised")
        fig.add_scatter(y=clean[i], line={"color": "green"}, name="clean")

        # Add a title with both error values
        cne = clean_v_noisy[i]
        cde = clean_v_denoised[i]
        fig.update_layout(
            title=f"Signal {i + 1}: RMSE {cne:.2e} -> {cde:.2e}",
        )
        figs.append(fig)

    return figs, clean_v_noisy, clean_v_denoised


def plot_errors(
    clean_v_noisy: numpy.ndarray,
    clean_v_denoised: numpy.ndarray,
) -> go.Figure:
    """Plot the distribution of errors as histograms on the same figure."""
    # Use red for the `clean_v_noisy` and blue for the `clean_v_denoised` histograms.
    # Use 50 bins for each histogram.
    fig = go.Figure()
    fig.add_histogram(x=clean_v_noisy, name="noisy", marker_color="red", nbinsx=100)
    fig.add_histogram(
        x=clean_v_denoised, name="denoised", marker_color="blue", nbinsx=100,
    )
    fig.update_layout(
        title="Distribution of RMSE vs Clean signal",
        xaxis_title="RMSE",
        yaxis_title="Probability Density",
    )
    return fig
