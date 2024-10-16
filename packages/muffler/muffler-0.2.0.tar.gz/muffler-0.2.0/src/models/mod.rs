//! ML Models that can be trained for denoising time series data.

mod classical;
mod decision_tree;
mod linear_regression;

pub use classical::Classical;
pub use decision_tree::DTModel;
pub use linear_regression::LRModel;
