Contributing
************

LumiSpy is meant to be a community maintained project. We welcome contributions
in the form of bug reports, documentation, code, feature requests, and more.
In the following we refer to some resources to help you make useful contributions.

Issues
======

The [issue tracker](https://github.com/lumispy/lumispy/issues) can be used to
report bugs or propose new features. When reporting a bug, the following is
useful:

- give a minimal example demonstrating the bug,
- copy and paste the error traceback.

Pull Requests
=============

If you want to contribute to the LumiSpy source code, you can send us a
[pull request](https://github.com/lumispy/lumispy/pulls).

Please refer to the 
[HyperSpy developer guide](http://hyperspy.org/hyperspy-doc/current/dev_guide/intro.html)
in order to get started and for detailed contributing guidelines.

The [kikuchypy contributors guide](https://kikuchipy.org/en/stable/contributing.html),
another HyperSpy extension, also is a valuable resource that can get you
started and provides useful guidelines.

Code style
==========

LumiSpy follows `Style Guide for Python Code <https://www.python.org/dev/peps/pep-0008/>`_ 
with `The Black Code style
<https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html>`_.

For `docstrings <https://www.python.org/dev/peps/pep-0257/>`_, we follow the `numpydoc
<https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard>`_ standard.

Package imports should be structured into three blocks with blank lines between
them:

- standard libraries (like ``os`` and ``typing``),
- third party packages (like ``numpy`` and ``hyperspy``),
- and finally ``lumispy`` imports.



