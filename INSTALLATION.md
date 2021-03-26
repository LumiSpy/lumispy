## Installation

### 1) Creating a conda environment

LumiSpy requires Python 3 and conda -- we suggest using the Python 3 version 
of [Miniconda](https://conda.io/miniconda.html).

We recommend creating a new environment for the lumispy package (or installing 
it in the hyperspy environment, if you have one already). To create a new 
environment:

1. Load the anaconda prompt.
2. Run the following command:

```
    $ conda create -n lumispy
```

### 2) Installing the package in the new environment

Now activate the lumispy environment and install the package using pip:
```
    $ conda activate lumispy
    $ pip install lumispy
```

Installation is completed! To start using it, check the next section.

#### OPTIONAL: Working with eV instead of wavelength units

In order to convert your signal luminescence axes (normally in wavelength in nanometers) to energy units, you will need to reinstall the `hyperspy` package to its developing branch `non-uniform-axes`. **If you skip this, all lumispy function will work, except the energy conversion functions.**

To do that, follow these steps:

1. Load the anaconda prompt.
2. Activate the lumispy environment using `conda activate lumispy`).
5. Install `git` and reinstall the hyperspy package running:

```
    $ conda activate lumispy
    $ conda install git -y
    $ pip uninstall hyperspy -y
    $ pip install git+git://github.com/hyperspy/hyperspy@non_uniform_axes
```

Now you are ready to use all the functionalites of lumispy.

### 3) Getting Started

To get started using LumiSpy, especially if you are unfamiliar with Python, we 
recommend using [Jupyter notebooks](https://jupyter.org/). Having installed 
lumispy as above, a Jupyter notebook can be opened using the following commands 
entered into an anaconda prompt (from scratch):

```
    $ conda activate lumispy
    $ jupyter lab
```
