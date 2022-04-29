Welcome to LumiSpy's documentation!
***********************************

|Build_status|_ |Tests|_ |Codecov_status|_ |DOI|_

|Python_version|_ |PyPI_version|_ |Anaconda_version|_ |License|_ |Documentation_status|_

.. |Build_status| image:: https://dev.azure.com/Lumispy/lumispy/_apis/build/status/LumiSpy.lumispy?branchName=main
.. _Build_status: https://dev.azure.com/Lumispy/lumispy/_build/latest?definitionId=3&branchName=main
.. |Tests| image:: https://github.com/lumispy/lumispy/workflows/Tests/badge.svg
.. _Tests: https://github.com/lumispy/lumispy/actions
.. |Codecov_status| image:: https://codecov.io/gh/lumispy/lumispy/branch/main/graph/badge.svg?token=8ZFX8X4Z1I
.. _Codecov_status: https://codecov.io/gh/lumispy/lumispy
.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.4640445.svg
.. _DOI: https://doi.org/10.5281/zenodo.4640445

.. |Python_version| image:: https://img.shields.io/pypi/pyversions/lumispy.svg?style=flat
.. _Python_version: https://pypi.python.org/pypi/lumispy
.. |PyPI_version| image:: http://img.shields.io/pypi/v/lumispy.svg?style=flat
.. _PyPI_version: https://pypi.python.org/pypi/lumispy
.. |Anaconda_version| image:: https://anaconda.org/conda-forge/lumispy/badges/version.svg
.. _Anaconda_version: https://anaconda.org/conda-forge/lumispy
.. |License| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
.. _License: https://www.gnu.org/licenses/gpl-3.0
.. |Documentation_status| image:: https://readthedocs.org/projects/lumispy/badge/?version=latest
.. _Documentation_status: https://lumispy.readthedocs.io/en/latest/?badge=latest

**LumiSpy** is a Python package extending the functionality for multi-dimensional
data analysis provided by the `HyperSpy <https://hyperspy.org/>`_ library. It is
aimed at helping with the analysis of luminescence spectroscopy data
(cathodoluminescence, photoluminescence, electroluminescence, Raman, SNOM).

Check out the :ref:`installation-label` section for further information, including
how to start using this project.

Complementing this documentation, the `LumiSpy Demos <https://github.com/LumiSpy/lumispy-demos>`_
repository contains curated Jupyter notebooks to provide tutorials and exemplary
workflows.

.. note::

   This project is under active development. Everyone is welcome to contribute.
   Please read our (see :ref:`contributing_label`) guidelines and get started!

Contents
========

.. toctree::
   :maxdepth: 1
   :caption: User Guide

   user_guide/installation.rst
   user_guide/introduction.rst
   user_guide/signal_axis.rst
   user_guide/fitting_luminescence.rst
   user_guide/utilities.txt
   user_guide/metadata_structure.rst

.. toctree::
   :maxdepth: 2
   :caption: API References

   api/modules.rst

.. toctree::
   :maxdepth: 1
   :caption: Tutorials

   Demo notebooks <https://github.com/LumiSpy/lumispy-demos>

.. toctree::
   :maxdepth: 1
   :caption: Release Notes

   changelog.rst

.. toctree::
   :maxdepth: 1
   :caption: Credits and citation

   citing.rst
   contributing.rst
   license.rst
   On GitHub <https://github.com/LumiSpy/lumispy>
