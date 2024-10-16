//! Creating training data from time-series data.

use ndarray::prelude::*;

/// Converts a 2d array of time-series samples into a collection of windows.
///
/// We assume that the time-series `samples` are stored in the rows of the 2d array.
/// The `window_size` is an even number and evenly divides the length of the
/// time-series.
///
/// # Parameters
///
/// * `samples`: The time-series samples to convert.
/// * `window_size`: The number of elements in each window.
///
/// # Returns
///
/// * The collection of windows.
/// * The column index where each window starts
pub fn create_windows(
    samples: &Array2<f32>,
    window_size: usize,
    stride: usize,
) -> (Vec<ArrayView2<f32>>, Vec<usize>) {
    let sample_len = samples.ncols();
    let window_starts = if (sample_len - window_size) % stride == 0 {
        (0..=(sample_len - window_size))
            .step_by(stride)
            .collect::<Vec<_>>()
    } else {
        (0..(sample_len - window_size))
            .step_by(stride)
            .chain(core::iter::once(sample_len - window_size))
            .collect()
    };
    let windows = window_starts
        .iter()
        .map(|&i| (i, i + window_size))
        .map(|(start, end)| samples.slice(s![.., start..end]))
        .collect::<Vec<_>>();
    (windows, window_starts)
}

/// Converts a collection of windows into training data.
///
/// We assume that the `index` is less than the window size.
/// The column at the `index` will be removed from the windows and used as the target.
///
/// # Parameters
///
/// * `windows`: The collection of windows.
/// * `index`: The index of the column to use as the target.
///
/// # Returns
///
/// * The training data.
/// * The target data.
pub fn windows_to_train(
    windows: &[ArrayView2<f32>],
    index: usize,
) -> (Array2<f32>, Array1<f32>) {
    let window_size = windows[0].len_of(Axis(1));
    let train = windows
        .iter()
        .map(|w| {
            if index == 0 {
                w.slice(s![.., 1..]).to_owned()
            } else if index == window_size - 1 {
                w.slice(s![.., ..index]).to_owned()
            } else {
                let pre_index = w.slice(s![.., ..index]);
                let post_index = w.slice(s![.., index + 1..]);
                ndarray::concatenate(Axis(1), &[pre_index, post_index]).unwrap_or_else(
                    |_| {
                        unreachable!(
                            "We made the slices, so they should have the correct shape."
                        )
                    },
                )
            }
        })
        .collect::<Vec<_>>();

    let target = windows
        .iter()
        .map(|w| w.index_axis(Axis(1), index).to_owned())
        .collect::<Vec<_>>();

    let train = train.iter().map(ArrayBase::view).collect::<Vec<_>>();
    let target = target.iter().map(ArrayBase::view).collect::<Vec<_>>();

    let train = ndarray::concatenate(Axis(0), &train).unwrap_or_else(|_| {
        unreachable!("We made the arrays, so they should have the correct shape.")
    });
    let target = ndarray::concatenate(Axis(0), &target).unwrap_or_else(|_| {
        unreachable!("We made the arrays, so they should have the correct shape.")
    });
    (train, target)
}

/// Converts a the predictions from models into the time-series.
///
/// # Parameters
///
/// * `targets`: The predictions.
/// * `out_shape`: The shape of the time-series.
/// * `window_size`: The number of elements in each window.
/// * `num_windows`: The number of windows.
/// * `stride`: The stride used to create the windows.
///
/// # Returns
///
/// The time-series.
///
/// # Errors
///
/// * If `targets` is empty.
/// * If any element in `targets` is not the correct size.
#[allow(clippy::needless_pass_by_value)]
pub fn reassemble(
    targets: Array2<f32>,
    out_shape: (usize, usize),
    window_starts: &[usize],
) -> Array2<f32> {
    let (num_samples, sample_len) = out_shape;
    let window_size = targets.ncols();

    let mut reassembled = Array2::zeros(out_shape);
    let mut counts = Array1::<u32>::zeros(sample_len);
    let increment = Array1::ones(window_size);

    for (i, &window_start) in window_starts.iter().enumerate() {
        let sample_start = i * num_samples;
        let sample_end = sample_start + num_samples;
        assert!(sample_start < targets.nrows());
        assert!(sample_end <= targets.nrows());
        let window = targets.slice(s![sample_start..sample_end, ..]);

        let window_end = window_start + window_size;
        let mut reassembled_slice =
            reassembled.slice_mut(s![.., window_start..window_end]);
        reassembled_slice += &window;

        let mut count_slice = counts.slice_mut(s![window_start..window_end]);
        count_slice += &increment;
    }

    // divide the columns by the corresponding counts
    #[allow(clippy::cast_precision_loss)]
    for (mut col, count) in reassembled
        .axis_iter_mut(Axis(1))
        .zip(counts.iter().map(|&c| c as f32))
    {
        col /= count;
    }

    reassembled
}

#[cfg(test)]
mod tests {
    use rand::prelude::*;

    use super::*;

    #[test]
    fn test_create_windows() {
        let samples = array![[1., 2., 3., 4., 5.], [6., 7., 8., 9., 10.]];
        let window_size = 3;
        let stride = 1;

        let (windows, starts) = create_windows(&samples, window_size, stride);
        assert_eq!(windows.len(), starts.len());
        let expected = vec![
            array![[1., 2., 3.], [6., 7., 8.]],
            array![[2., 3., 4.], [7., 8., 9.]],
            array![[3., 4., 5.], [8., 9., 10.]],
        ];
        assert_eq!(windows, expected);

        let stride = 2;
        let (windows, starts) = create_windows(&samples, window_size, stride);
        assert_eq!(windows.len(), starts.len());
        let expected = vec![
            array![[1., 2., 3.], [6., 7., 8.]],
            array![[3., 4., 5.], [8., 9., 10.]],
        ];
        assert_eq!(windows, expected);
    }

    #[test]
    fn test_windows_to_train() {
        let windows = vec![
            array![[1., 2., 3.], [6., 7., 8.]],
            array![[2., 3., 4.], [7., 8., 9.]],
            array![[3., 4., 5.], [8., 9., 10.]],
        ];
        let windows = windows.iter().map(ArrayBase::view).collect::<Vec<_>>();

        let (train, target) = windows_to_train(&windows, 0);
        let expected_train =
            array![[2., 3.], [7., 8.], [3., 4.], [8., 9.], [4., 5.], [9., 10.]];
        let expected_target = array![1., 6., 2., 7., 3., 8.];
        assert_eq!(train, expected_train);
        assert_eq!(target, expected_target);

        let (train, target) = windows_to_train(&windows, 1);
        let expected_train =
            array![[1., 3.], [6., 8.], [2., 4.], [7., 9.], [3., 5.], [8., 10.]];
        let expected_target = array![2., 7., 3., 8., 4., 9.];
        assert_eq!(train, expected_train);
        assert_eq!(target, expected_target);

        let (train, target) = windows_to_train(&windows, 2);
        let expected_train =
            array![[1., 2.], [6., 7.], [2., 3.], [7., 8.], [3., 4.], [8., 9.]];
        let expected_target = array![3., 8., 4., 9., 5., 10.];
        assert_eq!(train, expected_train);
        assert_eq!(target, expected_target);

        let windows = vec![
            array![[1., 2., 3.], [6., 7., 8.]],
            array![[3., 4., 5.], [8., 9., 10.]],
        ];
        let windows = windows.iter().map(ArrayBase::view).collect::<Vec<_>>();

        let (train, target) = windows_to_train(&windows, 0);
        let expected_train = array![[2., 3.], [7., 8.], [4., 5.], [9., 10.]];
        let expected_target = array![1., 6., 3., 8.];
        assert_eq!(train, expected_train);
        assert_eq!(target, expected_target);

        let (train, target) = windows_to_train(&windows, 1);
        let expected_train = array![[1., 3.], [6., 8.], [3., 5.], [8., 10.]];
        let expected_target = array![2., 7., 4., 9.];
        assert_eq!(train, expected_train);
        assert_eq!(target, expected_target);

        let (train, target) = windows_to_train(&windows, 2);
        let expected_train = array![[1., 2.], [6., 7.], [3., 4.], [8., 9.]];
        let expected_target = array![3., 8., 5., 10.];
        assert_eq!(train, expected_train);
        assert_eq!(target, expected_target);
    }

    #[test]
    fn test_reassemble_small() -> Result<(), String> {
        let samples = array![
            [1., 2., 3., 4., 5., 6., 7., 8., 9., 10.],
            [11., 12., 13., 14., 15., 16., 17., 18., 19., 20.]
        ];
        let out_shape = (2, 10);

        for window_size in [2, 3, 4, 5, 6, 7, 8, 9, 10] {
            for stride in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] {
                if stride > window_size {
                    continue;
                }
                let (windows, starts) = create_windows(&samples, window_size, stride);
                let targets = (0..window_size)
                    .map(|i| windows_to_train(&windows, i).1)
                    .collect::<Vec<_>>();
                let targets = targets.iter().map(ArrayBase::view).collect::<Vec<_>>();
                let targets =
                    ndarray::stack(Axis(1), &targets).map_err(|e| e.to_string())?;
                let reassembled = reassemble(targets, out_shape, &starts);
                assert_eq!(reassembled, samples);
            }
        }

        Ok(())
    }

    #[test]
    fn test_reassemble_large() -> Result<(), String> {
        let out_shape = (20, 256);
        let (num_samples, sample_len) = out_shape;
        let mut rng = rand::thread_rng();
        let samples = (0..(num_samples * sample_len))
            .map(|_| rng.gen_range(0.0..1.0))
            .collect::<Vec<f32>>();
        let samples =
            Array2::from_shape_vec(out_shape, samples).map_err(|e| e.to_string())?;

        for window_size in [32, 50, 100, 256] {
            for stride in [9, 16, 40, 50, 128] {
                if stride > window_size {
                    continue;
                }
                assert!(stride <= window_size);

                let (windows, starts) = create_windows(&samples, window_size, stride);
                assert_eq!(windows.len(), starts.len());

                let targets = (0..window_size)
                    .map(|i| windows_to_train(&windows, i).1)
                    .collect::<Vec<_>>();
                let targets = targets.iter().map(ArrayBase::view).collect::<Vec<_>>();
                let targets =
                    ndarray::stack(Axis(1), &targets).map_err(|e| e.to_string())?;
                let reassembled = reassemble(targets, out_shape, &starts);
                reassembled.into_iter().zip(samples.iter()).enumerate().all(
                    |(i, (r, &s))| {
                        let diff = (r - s).abs();
                        assert!(diff <= 1e-5, "Different at index {i}: {r} vs {s}");
                        diff <= 1e-5
                    },
                );
            }
        }

        Ok(())
    }
}
