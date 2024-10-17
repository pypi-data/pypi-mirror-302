# AWKDE

AWKDE is a Python library designed for calculating bandwidth variables and optimizing the Sigma parameter using the ML_k method. This library allows you to determine suitable Sigma values based on your data.

## Features

- Computes distance matrix
- Optimizes Sigma using input weights
- Supports iterations for improved results

## Installation

To install AWKDE, you can use `pip`:

```bash
pip install awkde-package
```

## Usage

The `AWKDE` library includes the `AWKDE` function for calculating Sigma and the `W_matrix` function for computing the distance matrix.

### Example

```python
import numpy as np
from awkde import AWKDE

# Input data
x_data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])

# Number of iterations
iterations = 10

# Calculate Sigma
sigma_values = AWKDE(x_data, iterations)

print("Sigma values:", sigma_values)
```

## Functions

### AWKDE(x, iterations, weights=None)

Calculates Sigma using the ML_k method.

**Parameters:**
- `x`: An array of input data
- `iterations`: Number of iterations for optimization
- `weights`: Optional weights (default is 1)

**Returns:**
- An array of optimized Sigma values

## Notes

- Ensure that the `numpy` library is installed.
- You can use different weights for each data point to obtain better results.

## Contributing

If you have suggestions or want to make changes to the library, we would love to hear from you. Please submit a Pull Request or report an issue in the [Issues](https://github.com/yourusername/awkde-package/issues) section.

## License

This project is licensed under the MIT License.
