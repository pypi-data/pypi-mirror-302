#![deny(clippy::correctness)]
#![warn(
    missing_docs,
    clippy::all,
    clippy::suspicious,
    clippy::style,
    clippy::complexity,
    clippy::perf,
    clippy::pedantic,
    clippy::nursery,
    clippy::missing_docs_in_private_items,
    clippy::unwrap_used,
    clippy::expect_used,
    clippy::panic,
    clippy::cast_lossless
)]
#![doc = include_str!("../README.md")]

pub(crate) mod data;
pub(crate) mod models;

use models::{Classical, DTModel, LRModel};

use ndarray::prelude::*;
use numpy::{prelude::*, PyArray2, PyReadonlyArray2};
use pyo3::{exceptions::PyValueError, prelude::*};
use smartcore::{
    api::SupervisedEstimator, linalg::basic::matrix::DenseMatrix,
    linear::linear_regression::LinearRegressionParameters,
    tree::decision_tree_regressor::DecisionTreeRegressorParameters,
};

/// Denoise a set of time-series samples.
///
/// # Parameters
///
/// * `samples`: The time-series samples to denoise.
/// * `window_size`: The number of elements in each window.
///
/// # Errors
///
/// * `window_size` is not an even number.
/// * `window_size` does not evenly divide the length of the time-series.
pub fn denoise<M, Mp, P>(
    samples: &Array2<f32>,
    window_size: usize,
    stride: usize,
    parameters: P,
) -> Result<Array2<f32>, String>
where
    M: Classical<Mp, P>,
    Mp: SupervisedEstimator<DenseMatrix<f32>, ndarray::Array1<f32>, P> + Send + Sync,
    P: Clone + Send + Sync,
{
    let model = M::train(samples, window_size, stride, parameters)?;
    model.denoise(samples, stride)
}

/// Denoise a set of time-series samples using linear regression.
///
/// # Parameters
///
/// * `samples`: The time-series samples to denoise.
/// * `window_size`: The number of elements in each window.
///
/// # Errors
///
/// * Shape mismatch. Should not happen.
///
/// # Returns
///
/// The denoised samples.
#[allow(clippy::needless_pass_by_value)]
#[pyfunction]
pub fn denoise_linear_regression<'py>(
    py: Python<'py>,
    samples: PyReadonlyArray2<'py, f32>,
    window_size: usize,
    stride: usize,
) -> PyResult<Bound<'py, PyArray2<f32>>> {
    let samples = samples.as_array().to_owned();
    denoise::<LRModel, _, _>(
        &samples,
        window_size,
        stride,
        LinearRegressionParameters::default(),
    )
    .map(|x| x.into_pyarray_bound(py))
    .map_err(PyValueError::new_err)
}

/// Denoise a set of time-series samples using decision trees.
///
/// # Parameters
///
/// * `samples`: The time-series samples to denoise.
/// * `window_size`: The number of elements in each window.
///
/// # Errors
///
/// * Shape mismatch. Should not happen.
///
/// # Returns
///
/// The denoised samples.
#[allow(clippy::needless_pass_by_value)]
#[pyfunction]
pub fn denoise_decision_tree<'py>(
    py: Python<'py>,
    samples: PyReadonlyArray2<'py, f32>,
    window_size: usize,
    stride: usize,
) -> PyResult<Bound<'py, PyArray2<f32>>> {
    let samples = samples.as_array().to_owned();
    let params = DecisionTreeRegressorParameters {
        max_depth: Some(8),
        min_samples_leaf: 1,
        min_samples_split: 2,
        seed: None,
    };
    denoise::<DTModel, _, _>(&samples, window_size, stride, params)
        .map(|x| x.into_pyarray_bound(py))
        .map_err(PyValueError::new_err)
}

/// A Python module implemented in Rust.
///
/// # Errors
///
/// * If the module cannot be created.
/// * If the function cannot be added to the module.
#[pymodule]
pub fn muffler<'py>(_py: Python<'py>, m: &Bound<'py, PyModule>) -> PyResult<()> {
    pyo3_log::init();

    m.add_function(wrap_pyfunction!(denoise_linear_regression, m)?)?;
    m.add_function(wrap_pyfunction!(denoise_decision_tree, m)?)?;

    Ok(())
}
