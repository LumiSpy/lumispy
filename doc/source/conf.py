# Configuration file for the Sphinx documentation builder.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
import sys

sys.path.append("../../")


# -- Project information
exec(open("../../lumispy/release_info.py").read())  # grab version info

project = "LumiSpy"
copyright = copyright
author = author

release = version
version = version

# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.imgmath",
    "sphinx.ext.graphviz",
    "sphinx.ext.autosummary",
    "sphinx_toggleprompt",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    "hyperspyweb": ("https://hyperspy.org/", None),
    "matplotlib": ("https://matplotlib.org", None),
    "numpy": ("https://docs.scipy.org/doc/numpy", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
    "hyperspy": ("https://hyperspy.org/hyperspy-doc/current/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "logo_only": True,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["../_static"]
html_css_files = ["css/custom.css"]

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "../_static/logo_rec_april21.svg"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "../_static/lumispy.ico"

# -- Options for EPUB output
epub_show_urls = "footnote"


def run_apidoc(_):
    # https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html
    # https://www.sphinx-doc.org/es/1.2/ext/autodoc.html
    import os

    os.environ[
        "SPHINX_APIDOC_OPTIONS"
    ] = "members,private-members,no-undoc-members,show-inheritance,ignore-module-all"

    from sphinx.ext.apidoc import main

    cur_dir = os.path.normpath(os.path.dirname(__file__))
    output_path = os.path.join(cur_dir, "api")
    modules = os.path.normpath(os.path.join(cur_dir, "../../lumispy"))
    exclude_pattern = [
        "../../lumispy/tests",
        "../../lumispy/components",
        "../../lumispy/release_info.py",
    ]
    main(["-e", "-f", "-P", "-o", output_path, modules, *exclude_pattern])


def setup(app):
    app.connect("builder-inited", run_apidoc)
    app.add_css_file("css/dark.css")
    app.add_css_file("css/light.css")
