//! A model that relies on classical ML techniques to denoise time-series data.

use std::path::{Path, PathBuf};

use ndarray::prelude::*;
use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use smartcore::{
    api::SupervisedEstimator,
    linalg::basic::{arrays::Array2, matrix::DenseMatrix},
};

/// A model that can be trained, evaluated, and used for prediction.
///
/// # Type Parameters
///
/// * `M`: The type of the model.
/// * `P`: The type of the model parameters.
pub trait Classical<M, P>:
    Sized + Send + Sync + Serialize + for<'de> Deserialize<'de>
where
    M: SupervisedEstimator<DenseMatrix<f32>, Array1<f32>, P> + Send + Sync,
    P: Clone + Send + Sync,
{
    /// Creates a new model.
    fn new(models: Vec<M>, window_size: usize) -> Self;

    /// Returns a name for the model, which can be used for saving and loading.
    fn name(&self) -> String;

    /// Returns the inner models.
    fn models(&self) -> &[M];

    /// Returns the window size.
    fn window_size(&self) -> usize;

    /// Trains the model.
    ///
    /// # Parameters
    ///
    /// * `samples`: The time-series samples to create the data from.
    /// * `window_size`: The number of elements in each window.
    ///
    /// # Errors
    ///
    /// * Depends on the implementation.
    ///
    /// # Returns
    ///
    /// The trained model.
    fn train(
        samples: &ndarray::Array2<f32>,
        window_size: usize,
        stride: usize,
        parameters: P,
    ) -> Result<Self, String> {
        let (windows, _) = crate::data::create_windows(samples, window_size, stride);
        let inner_models = (0..window_size)
            .into_par_iter()
            .map(|i| {
                let (train_x, train_y) = crate::data::windows_to_train(&windows, i);
                let train_x = DenseMatrix::from_slice(&train_x);
                M::fit(&train_x, &train_y, parameters.clone())
                    .map_err(|e| e.to_string())
            })
            .collect::<Result<Vec<_>, _>>()?;
        Ok(Self::new(inner_models, window_size))
    }

    /// Predicts the denoised time-series using the model.
    ///
    /// # Parameters
    ///
    /// * `x`: The input data to predict the target data.
    ///
    /// # Errors
    ///
    /// * Depends on the implementation.
    ///
    /// # Returns
    ///
    /// The denoised time-series.
    fn denoise(
        &self,
        samples: &ndarray::Array2<f32>,
        stride: usize,
    ) -> Result<ndarray::Array2<f32>, String> {
        let (windows, starts) =
            crate::data::create_windows(samples, self.window_size(), stride);
        let predicted = (0..self.window_size())
            .into_par_iter()
            .map(|i| {
                let (test_x, _) = crate::data::windows_to_train(&windows, i);
                let test_x = DenseMatrix::from_slice(&test_x);
                let model = &self.models()[i];
                M::predict(model, &test_x).map_err(|e| e.to_string())
            })
            .collect::<Result<Vec<_>, _>>()?;
        let predicted = predicted.iter().map(ArrayBase::view).collect::<Vec<_>>();
        let predicted =
            ndarray::stack(Axis(1), &predicted).map_err(|e| e.to_string())?;

        let out_shape = (samples.len_of(Axis(0)), samples.len_of(Axis(1)));
        Ok(crate::data::reassemble(predicted, out_shape, &starts))
    }

    /// Saves the model to a file.
    ///
    /// # Parameters
    ///
    /// * `path_to_dir`: The path to the directory to save the model to.
    ///
    /// # Errors
    ///
    /// * If the model cannot be saved.
    /// * If the directory does not exist or is not writable.
    ///
    /// # Returns
    ///
    /// The path to the saved model.
    fn save(&self, path_to_dir: &Path) -> Result<PathBuf, String> {
        if !path_to_dir.exists() {
            return Err(format!(
                "The directory '{}' does not exist.",
                path_to_dir.display()
            ));
        }
        if !path_to_dir.is_dir() {
            return Err(format!(
                "The path '{}' is not a directory.",
                path_to_dir.display()
            ));
        }
        if !path_to_dir
            .metadata()
            .map(|m| m.permissions().readonly())
            .unwrap_or(false)
        {
            return Err(format!(
                "The directory '{}' is not writable.",
                path_to_dir.display()
            ));
        }

        let path = path_to_dir.join(self.name());
        let mut file = std::fs::File::create(&path).map_err(|e| e.to_string())?;
        bincode::serialize_into(&mut file, self).map_err(|e| e.to_string())?;
        Ok(path)
    }

    /// Loads a model from a file.
    ///
    /// # Parameters
    ///
    /// * `path`: The path to the file to load the model from, as produced by `save`.
    ///
    /// # Errors
    ///
    /// * If the model cannot be loaded.
    /// * If the file does not exist or is not readable.
    ///
    /// # Returns
    ///
    /// The loaded model.
    fn load(path: &Path) -> Result<Self, String> {
        if !path.exists() {
            return Err(format!("The file '{}' does not exist.", path.display()));
        }
        if !path.is_file() {
            return Err(format!("The path '{}' is not a file.", path.display()));
        }
        if !path
            .metadata()
            .map(|m| m.permissions().readonly())
            .unwrap_or(false)
        {
            return Err(format!("The file '{}' is not readable.", path.display()));
        }
        let file = std::fs::File::open(path).map_err(|e| e.to_string())?;
        bincode::deserialize_from(file).map_err(|e| e.to_string())
    }
}
