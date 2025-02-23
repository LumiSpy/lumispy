# Releasing a new LumiSpy version

To publish a new LumiSpy release do the following steps:

## Preparation

- Create a new PR to the 'main' branch for the release process, e.g. `release_v0.1.1`
- In a pull request, prepare the release by running the `prepare_release.py` python script
  (e.g. `python prepare_release.py 0.1.1`), which will do the following:
  - update the release notes in `CHANGES.rst` by running `towncrier`,
  - update the `setuptools_scm` fallback version in `pyproject.toml` (for a patch release, this will stay the same).
- Check release notes
- Let that PR collect comments for a day to ensure that other maintainers are comfortable 
  with releasing
- Verify that correct date and version number ist set in `CHANGELOG.rst`
  
## Tag and Release

- Create a tag e.g. `git tag -a v0.1.1 -m "LumiSpy version 0.1.1"`. The lumispy version will
  be set at build time from the tag by `setuptools_scm`.
- Push tag to user fork for a test run `git push origin v0.1.1`. Will run the release
  workflow without uploading to PyPi
- Push tag to LumiSpy repository to trigger release `git push upstream v0.1.1`
  (this triggers the GitHub action to create the sdist and wheel and upload to
  PyPi automatically). :warning: this is a point of no return :warning:
  
## Post-release action
 
- Prepare `CHANGELOG.rst` for development by adding `UNRELEASED` headline
- Merge the PR

## Follow-up

- Tidy up and close corresponding milestone or project
- A PR to the conda-forge feedstock will be created by the conda-forge bot
