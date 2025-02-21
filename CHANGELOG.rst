Changelog
*********

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

Changelog entries for the development version are available at
https://lumispy.readthedocs.io/en/latest/changelog.html


.. towncrier-draft-entries:: |release| [UNRELEASED]

.. towncrier release notes start

.. _changes_0.3.0:

0.3.0 (2025-02-23)
==================

New features
------------

- Implement correct casting of :class:`~.signals.luminescence_transientspec.LumiTransientSpectrum` to either :class:`~.signals.luminescence_spectrum.LumiSpectrum` or :class:`~.signals.luminescence_transient.LumiTransient` when the signal dimension is reduced - previously, a :class:`~hyperspy.api.signals.Signal1D` object was returned. (`#205 <https://github.com/lumispy/lumispy/issues/205>`_)
- Add functions :meth:`~.signals.luminescence_transientspec.LumiTransientSpectrum.spec2nav` and :meth:`~.signals.luminescence_transientspec.LumiTransientSpectrum.time2nav` to convert either `signal` dimension to a `navigation` dimension for efficient iteration over the respective axes. (`#223 <https://github.com/lumispy/lumispy/issues/223>`_)

Enhancements
------------

- Fix axis conversion for two signal dimensions (e.g. streak camera maps) (`#205 <https://github.com/lumispy/lumispy/issues/205>`_)

Improved Documentation
----------------------

- Various updates and improvements of the documentation (`#188 <https://github.com/lumispy/lumispy/issues/188>`_, `#193 <https://github.com/lumispy/lumispy/issues/193>`_, `#196 <https://github.com/lumispy/lumispy/issues/196>`_, `#206 <https://github.com/lumispy/lumispy/issues/206>`_, `#213 <https://github.com/lumispy/lumispy/issues/213>`_ , `#218 <https://github.com/lumispy/lumispy/issues/218>`_, `#224 <https://github.com/lumispy/lumispy/issues/224>`_)
- Use ``towncrier`` to manage changelog (`#211 <https://github.com/lumispy/lumispy/issues/211>`_)

Maintenance
-----------

- Align supported python versions (3.8-3.12) to HyperSpy 2.0 (`#202 <https://github.com/lumispy/lumispy/issues/202>`_)
- Fix intersphinx links to documentation of HyperSpy 2.0 and add linkchecker workflow (`#203 <https://github.com/lumispy/lumispy/issues/203>`_)
- CI, lint, test fixes ( `#187 <https://github.com/lumispy/lumispy/issues/187>`_, `#209 <https://github.com/lumispy/lumispy/issues/209>`_, `#216 <https://github.com/lumispy/lumispy/issues/216>`_)
- Streamline project files and release workflow to match HyperSpy ecosystem:

  - Migrate to ``pyproject.toml`` from ``setup.py``
  - Use ``setuptools-scm`` to set version at build time
  - Adapt release workflow, e.g. mine doi only after successful upload (`#211 <https://github.com/lumispy/lumispy/issues/211>`_)

- Add support for python 3.13 and drop support for python 3.8, update tests workflows (`#225 <https://github.com/lumispy/lumispy/issues/225>`_)


.. _changes_0.2.2:

2023-03-15 - version 0.2.2
==========================
Changed
-------
- Use `GitHub code scanning (CodeQL)
  <https://docs.github.com/en/code-security/code-scanning/automatically-scanning-your-code-for-vulnerabilities-and-errors/about-code-scanning-with-codeql>`_
  for integrity check as `it replaces LGTM
  <https://github.blog/2022-08-15-the-next-step-for-lgtm-com-github-code-scanning/>`_
- Added a centroid/center of mass functionality to analyse peak position of a spectrum (both in `utils`` and in `LumiSpectrum``)
- Add documentation of signal tools

Maintenance
-----------
- Replace ``sphinx.ext.imgmath`` by ``sphinx.ext.mathjax`` to fix the math rendering in the *ReadTheDocs* build
- fix external references in the documentation


.. _changes_0.2.1:

2022-11-02 - version 0.2.1
==========================
Added
-----
- Improved documentation
- Use lgtm.com to check code integrity

Changed
-------
- Fix conversion to Raman shift (relative wavenumber) and make ``jacobian=False`` default; ``fix inplace=False`` for axis conversions
- Fix ``to_eV`` and ``to_invcm``, as slicing with `.isig[]` was failing on converted signals
- ``s.remove_negative`` now defaults to ``inplace=False`` (previously ``True``)

Maintenance
-----------
- Use ``softprops/action-gh-release`` action instead of deprecated ``create-release``, pin action to a commit SHA


.. _changes_0.2.0:

2022-04-29 - version 0.2.0
==========================
Added
-----
- Set up read the docs documentation
- Added metadata convention
- Add proper handling of variance on Jacobian transformation during axis conversion (eV, invcm)

Changed
-------
- Account for the general availability of non-uniform axes with the HyperSpy v1.7 release
- Make ``LumiTransient`` 1D and add 2D ``LumiTransientSpectrum`` class
- Add python 3.10 build, remove python 3.6
- Fix error in background dimensions that allows compatibility for updated ``map`` in HyperSpy (failing integration tests)
- Fix for links in PyPi
- Deprecate ``exposure`` argument of ``s.scale_by_exposure`` in favor of ``integration_time`` in line with metadata convention
- Add deprecation warning to ``remove_background_from_file``


.. _changes_0.1.3:

2021-11-23 - version 0.1.3
==========================
Changed
-------
- Mentions of the now deleted ``non_uniform_axes`` branch in HyperSpy updated to `RELEASE_next_minor`
- Change 'master' to 'main' branch
- Updated/corrected badges and other things in README.md and other documentation files


.. _changes_0.1.2:

2021-08-22 - version 0.1.2
==========================
Added
-----
- This project now keeps a Changelog
- Added signal-hierarchy for time-resolved luminescence
- Added GitHub action for release
- Created logo

Changed
-------
- Consistent black-formatting
- fixed join_spectra
- fixed tests


.. _changes_0.1.0:

2021-03-26 - version 0.1.0
==========================
Added
-----
- The first release, basic functionality implemented

