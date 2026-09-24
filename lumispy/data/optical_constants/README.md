# Optical constants data format

LumiSpy stores the bundled optical constants as HyperSpy `.hspy` files. Each file contains a one-dimensional `ComplexSignal1D` without navigation axes.

## HyperSpy files

The signal axis must contain positive, unique spectral coordinates in strictly increasing order. Its name and unit must agree with the corresponding metadata.

The complex signal data represent either:

* the complex refractive index \(n + ik\), or
* the relative permittivity \(\varepsilon_1 + i\varepsilon_2\).

The following metadata are required:

```text
OpticalConstants.spectral_variable
OpticalConstants.spectral_unit
OpticalConstants.data_kind
```

Supported spectral coordinates are:

```text
spectral_variable: "wavelength"
spectral_unit:     "µm"
```

or:

```text
spectral_variable: "Photon energy"
spectral_unit:     "eV"
```

The complex signal data can represent either:
```text
data_kind:      "complex_refractive_index"
data:  "n + ik"
```

or

```
data_kind: "relative_permittivity"
data: "epsilon_real + i * epsilon_imag"
```

The following descriptive metadata should also be provided:

```text
OpticalConstants.material
OpticalConstants.reference
Signal.quantity
General.title
```

Bundled datasets can be listed and loaded with:

```python
from lumispy.data import (
    load_optical_constants,
    supported_optical_constants,
)

print(supported_optical_constants())
optical_data = load_optical_constants("Au_johnson")
```

## CSV and text files

User-provided optical constants do not need to be converted to `.hspy` first. The recommended text format uses one spectral-coordinate column followed by the two optical components.

For \(n\) and \(k\):

```csv
wavelength,n,k
0.400,1.50,0.10
0.500,1.60,0.12
0.600,1.70,0.15
```

For relative permittivity:

```csv
wavelength,epsilon_real,epsilon_imag
1.5,-20.0,1.2
2.0,-15.0,1.5
2.5,-10.0,2.0
```

The files can be converted to the required `ComplexSignal1D` with:

```python
from lumispy.utils import optical_constants_to_signal

dataset = {
    "layout": "combined_n_k",
    "representation": "n_k",
    "file": "optical.csv",
    "loadfile_kwargs": {
        "delimiter": ",",
        "skiprows": 1,
    },
    "coordinate": "wavelength",
    "coordinate_units": "µm",
    "coordinate_column": 0,
    "n_column": 1,
    "k_column": 2,
    "material": "Example material",
    "reference": "Example reference",
}

optical_data = optical_constants_to_signal(dataset)
```

The following keys are required for all layouts:

- `layout`
- `representations`
- `loadfile_kwargs`
- `coordinate`
- `coordinate_units`
- `coordinate_column`
- `material`
- 'reference'

The required file and column keys depend on the selected layout:

- `combined_n_k`: `file`, `n_column`, `k_column`, and optionally
  `k_coordinate_column`
- `separate_n_k`: `n_file`, `k_file`, `n_column`, and `k_column`
- `combined_epsilon`: `file`, `real_column`, and `imaginary_column`

Column indices are zero_based. `loadfile_kwargs` is passed directly to `numpy.loadtxt`, for example
to specify a delimiter or skip a header row. Relative file paths are resolved from the current working directory

The input rows may be unordered; they are sorted by the spectral coordinate during conversion. Coordinates must be positive, finite, and unique, and both optical components must contain only finite values.
