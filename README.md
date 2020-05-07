# LumiSpy

[![Build Status](https://dev.azure.com/Lumispy/lumispy/_apis/build/status/LumiSpy.lumispy?branchName=master)](https://dev.azure.com/Lumispy/lumispy/_build/latest?definitionId=3&branchName=master)
[![Build Status](https://travis-ci.org/LumiSpy/lumispy.svg?branch=master)](https://travis-ci.org/LumiSpy/lumispy)
[![Coverage Status](https://coveralls.io/repos/github/LumiSpy/lumispy/badge.svg?branch=master)](https://coveralls.io/github/LumiSpy/lumispy?branch=master)

### Introduction

LumiSpy is an extension Python package for multi-dimensional data analysis 
provided by the [HyperSpy](http://hyperspy.org) library. It is aimed at helping 
with the analysis of luminescence spectroscopy data (cathodoluminescence, 
photoluminescence, electroluminescence, Raman, SNOM).

LumiSpy is released under the GPL v3 license. 

If analysis using LumiSpy forms a part of published work please consider 
recognising the code development by citing the
[github repository](www.github.com/lumispy/lumispy).

### Installation

##### Creating a conda environment

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

##### Installing the package in the new environment

Now that you have created a new environment, install the package:

1. Download the [source code](https://github.com/lumispy/lumispy) and put it 
in a directory on your computer (by default, GitHub saves it in 
`Username\Documents\GitHub\lumispy`).
2. Load the anaconda prompt.
3. Change current working directory to the folder where you downloaded the 
source code.
4. Activate the lumispy environment.
5. Install the package running:

```
    $ cd PATH_TO_SOURCE_CODE
    $ conda activate lumispy
    $ pip install .
```

Installation is completed! To start using it, check the next section.

### Getting Started

To get started using LumiSpy, especially if you are unfamiliar with Python, we 
recommend using [Jupyter notebooks](https://jupyter.org/). Having installed 
lumispy as above, a Jupyter notebook can be opened using the following commands 
entered into an anaconda prompt (from scratch):

```
    $ conda activate lumispy
    $ jupyter lab
```

[Tutorials and example workflows](https://github.com/lumispy/lumispy-demos)
have been curated as a series of Jupyter notebooks that you can work through 
and modify to perform many common analyses. Simply:

1. Download the `lumispy_demos` repository in your desired folder
2. Load lumispy (as shown above)
3. In Jupyter lab, navigate to the folder and start using the notebook
