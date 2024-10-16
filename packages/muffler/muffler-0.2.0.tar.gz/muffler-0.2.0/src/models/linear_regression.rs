//! A Denoising model based on Linear Regression.

use serde::{Deserialize, Serialize};
use smartcore::{
    linalg::basic::matrix::DenseMatrix,
    linear::linear_regression::{LinearRegression, LinearRegressionParameters},
};

/// A Linear Regression model.
#[allow(clippy::upper_case_acronyms)]
type LR = LinearRegression<f32, f32, DenseMatrix<f32>, ndarray::Array1<f32>>;

/// A model for denoising time-series data based on linear regression.
#[derive(Serialize, Deserialize)]
pub struct LRModel {
    /// The linear regression model.
    models: Vec<LR>,
    /// The number of elements in each window.
    window_size: usize,
}

impl super::Classical<LR, LinearRegressionParameters> for LRModel {
    fn new(models: Vec<LR>, window_size: usize) -> Self {
        Self {
            models,
            window_size,
        }
    }

    fn name(&self) -> String {
        format!("muffler-linear_regression-{}", self.window_size)
    }

    fn models(&self) -> &[LR] {
        &self.models
    }

    fn window_size(&self) -> usize {
        self.window_size
    }
}
