.. _installation:

Installation
************

To install LumiSpy, you have the following options (independent of the operating system you use):

1. LumiSpy is included in the `HyperSpy Bundle <https://hyperspy.org/hyperspy-bundle/>`_,
   a standalone program that includes a python distribution and all relevant libraries 
   (recommended if you do not use *python* for anything else).
2. :ref:`conda` (recommended if you are also working with other *python* packages).
3. :ref:`pip`.
4. Installing the development version from `GitHub <https://github.com/LumiSpy/lumispy/>`_.
   Refer to the appropriate section in the :external+hyperspy:ref:`HyperSpy user guide
   <install-dev>` (replacing ``hyperspy`` by ``lumispy``).


.. _conda:

Installation using conda
========================

Follow these 3 steps to install LumiSpy using **conda** and start using it.

1. Creating a conda environment
-------------------------------

LumiSpy requires Python 3 and ``conda`` -- we suggest using the Python 3 version
of `Miniconda <https://conda.io/miniconda.html>`_.

We recommend creating a new environment for the LumiSpy package (or installing
it in the :external+hyperspy:ref:`HyperSpy <anaconda-install>` 
environment, if you have one already). To create a new environment:

1. Load the anaconda prompt.
2. Run the following command:

.. code-block:: bash

    (base) conda create -n lumispy -y


2. Installing the package in the new environment
------------------------------------------------

Now activate the LumiSpy environment and install the package from ``conda-forge``:

.. code-block:: bash

    (base) conda activate lumispy
    (lumispy) conda install -c conda-forge lumispy -y

Required dependencies will be installed automatically.

Installation is completed! To start using it, check the next section.

.. Note::

   If you run into trouble, check the more detailed documentation in the
   :external+hyperspy:ref:`HyperSpy user guide <anaconda-install>`.


3. Getting Started
------------------

To get started using LumiSpy, especially if you are unfamiliar with Python, we
recommend using `Jupyter notebooks <https://jupyter.org/>`_. Having installed
LumiSpy as above, a Jupyter notebook can be installed and opened using the following commands
entered into an anaconda prompt (from scratch):

.. code-block:: bash

    (base) conda activate lumispy
    (lumispy) conda install -c conda-forge jupyterlab -y
    (lumispy) jupyter lab

`Tutorials and exemplary workflows <https://github.com/lumispy/lumispy-demos>`_
have been curated as a series of Jupyter notebooks that you can work through 
and modify to perform many common analyses.


.. _pip:

Installation using pip
========================

Alternatively, you can also find LumiSpy in the `Python Package Index (PyPI)
<https://pypi.org/search/?q=lumispy>`_ and install it using (requires ``pip``):

.. code-block:: bash

    pip install lumispy

Required dependencies will be installed automatically.


Updating the package
====================

Using **conda**:

.. code-block:: bash

    conda update lumispy -c conda-forge

Using **pip**:

.. code-block:: bash

    pip install lumispy --upgrade

.. Note::

    If you want to be notified about new releases, please *Watch (Releases only)* the `Lumispy repository 
    on GitHub <https://github.com/LumiSpy/lumispy/>`_ (requires a GitHub account).
