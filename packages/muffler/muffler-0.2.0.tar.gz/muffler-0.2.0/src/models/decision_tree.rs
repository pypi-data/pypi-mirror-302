//! A Denoising model based on Linear Regression.

use serde::{Deserialize, Serialize};
use smartcore::{
    linalg::basic::matrix::DenseMatrix,
    tree::decision_tree_regressor::{
        DecisionTreeRegressor, DecisionTreeRegressorParameters,
    },
};

/// A Decision Tree model.
#[allow(clippy::upper_case_acronyms)]
type DTR = DecisionTreeRegressor<f32, f32, DenseMatrix<f32>, ndarray::Array1<f32>>;

/// A model for denoising time-series data based on linear regression.
#[derive(Serialize, Deserialize)]
pub struct DTModel {
    /// The linear regression model.
    models: Vec<DTR>,
    /// The number of elements in each window.
    window_size: usize,
}

impl super::Classical<DTR, DecisionTreeRegressorParameters> for DTModel {
    fn new(models: Vec<DTR>, window_size: usize) -> Self {
        Self {
            models,
            window_size,
        }
    }

    fn name(&self) -> String {
        format!("muffler-decision_tree-{}", self.window_size)
    }

    fn models(&self) -> &[DTR] {
        &self.models
    }

    fn window_size(&self) -> usize {
        self.window_size
    }
}
