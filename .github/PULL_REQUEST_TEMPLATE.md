### Requirements
* Read the [contributing guidelines](https://github.com/lumispy/lumispy/blob/main/.github/CONTRIBUTING.md).
* Fill out the template; it helps the review process and it is useful to summarise the PR.
* This template can be updated during the progression of the PR to summarise its status. 

*You can delete this section after you read it.*

### Description of the change
A few sentences and/or a bulleted list to describe and motivate the change:
- Change A.
- Change B.
- etc.

### Progress of the PR
- [ ] Change implemented (can be split into several points),
- [ ] docstring updated (if appropriate),
- [ ] update user guide (if appropriate),
- [ ] added tests,
- [ ] add a changelog entry in the `upcoming_changes` folder (see [`upcoming_changes/README.rst`](https://github.com/lumispy/lumispy/blob/main/upcoming_changes/README.rst)),
- [ ] Check formatting of the changelog entry (and eventual user guide changes) in the `docs/readthedocs.org:lumispy` build of this PR (link in github checks),
- [ ] ready for review.

### Minimal example of the bug fix or the new feature
```python
import lumispy as lum
import numpy as np
s = lum.signals.LumiSpectrum(np.arange(10))
# Your new feature...
```


