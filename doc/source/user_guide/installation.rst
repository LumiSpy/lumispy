.. _installation-label:

Installation
************

Follow these 3 steps to install LumiSpy.

Creating a conda environment
============================

LumiSpy requires Python 3 and conda -- we suggest using the Python 3 version
of `Miniconda <https://conda.io/miniconda.html/>`_.

We recommend creating a new environment for the LumiSpy package (or installing
it in the HyperSpy environment, if you have one already). To create a new
environment:

1. Load the anaconda prompt.
2. Run the following command:

.. code-block:: bash

    (base) conda create -n lumispy


Installing the package in the new environment
=============================================

Now activate the LumiSpy environment and install the package using pip:

.. code-block:: bash

    (base) conda activate lumispy
    (lumispy) pip install lumispy

Installation is completed! To start using it, check the next section.

.. Note::

    If the installation fails using ``pip``, try installing using ``conda install lumispy -c conda-forge``.

Getting Started
===============

To get started using LumiSpy, especially if you are unfamiliar with Python, we
recommend using `Jupyter notebooks <https://jupyter.org/>`_. Having installed
LumiSpy as above, a Jupyter notebook can be opened using the following commands
entered into an anaconda prompt (from scratch):

.. code-block:: bash

    (base) conda activate lumispy
    (lumispy) pip install jupyterlab
    (lumispy) jupyter lab
