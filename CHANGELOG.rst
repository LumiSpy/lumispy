Changelog
*********

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

UNRELEASED
==========
Added
-----
- Improved documentation
- Use `lgtm.com <https://lgtm.com/projects/g/LumiSpy/lumispy/>`_ to check code integrity
- Added ``lumispy.utils.analysis.plot_span_map`` for interactively viewing how different peaks vary spatially in a hyperspectra.

Changed
-------
- Fix conversion to Raman shift (relative wavenumber) and make ``jacobian=False`` default; ``fix inplace=False`` for axis conversions
- ``s.remove_negative`` now defaults to ``inplace=False`` (previously ``True``)

Maintenance
-----------
- Use ``softprops/action-gh-release`` action instead of deprecated ``create-release`` . Pin action to a commit SHA.

2022-04-29 - version 0.2
========================
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

2021-11-23 - version 0.1.3
==========================
Changed
-------
- Mentions of the now deleted ``non_uniform_axes`` branch in HyperSpy updated to `RELEASE_next_minor`
- Change 'master' to 'main' branch
- Updated/corrected badges and other things in README.md and other documentation files

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

2021-03-26 - version 0.1
========================
Added
-----
- The first release, basic functionality implemented

