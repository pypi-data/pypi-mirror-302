# Muffler

Denoising Time-Series Data

## Installation

```bash
pip install muffler
```

## Usage

```python
import muffler
import numpy as np

# Generate some noisy data
t = np.linspace(0, 1, 100)
clean_signal = np.sin(2 * np.pi * t)

# Add some noise
std = 1.0
conditional_noise = np.sqrt(np.abs(clean))
random_noise = np.random.normal(0, std, t.shape)
noisy_signal = clean + random_noise * conditional_noise

# Denoise the data
window_size = 100
stride = 25
denoised_signal = muffler.denoise_linear_regression(noisy_signal, window_size, stride)

# Compute the error
error = np.mean(np.sqrt(np.mean((clean_signal - denoised_signal) ** 2, axis=1)))
print(f"Error: {error:.2e}")
```

## Streamlit App (An example)

You can also use the streamlit app to see how the denoising works.
To run the app, you need to install [Rust](https://www.rust-lang.org/tools/install) and [Maturin](https://www.maturin.rs/installation) for compiling the code.
Then, you need to create a Python (3.9 or greater) virtual environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
maturin develop --release --extras=dev
```

Finally, you can run the app:

```bash
streamlit run examples/app.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

TODO: Add citation
