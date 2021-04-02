## Releasing a new LumiSpy version

To publish a new LumiSpy release do the following steps:

- Create a new branch for the release process
- Make sure to have the code ready, including changelog
- Change version number in `lumispy/release_info.py` (increase the third digit
  for a patch release, the second digit for a regular minor release, the first
  digit for a major release)
- Create a tag e.g. `git tag -a v0.1.1 -m "LumiSpy version 0.1.1"`
- Push tag to user repository for a test run `git push origin v0.1.1`
- Push tag to lumispy repository to trigger release `git push upstream v0.1.1`
  (this triggers the GitHub action to create the sdist and wheel and upload to
  PyPi automatically).
