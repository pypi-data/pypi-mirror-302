# -*- coding: utf-8 -*-
from datetime import datetime
import sys
from pathlib import Path

now_dt: datetime = datetime.now()

project = "Pretty headers for http.client"
copyright = (
    f"2024{'-' + now_dt.strftime('%Y') if now_dt.year > 2024 else ''}, Red Hat Inc."
)
author = "Pavol Babinčák"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx_tabs.tabs",
    "myst_parser",
]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".venv", "LICENSE.txt", "README.md"]

# autodoc config
sys.path.insert(0, str(Path("..", "src").resolve()))

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False


# intersphinx config
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "urllib3": ("https://urllib3.readthedocs.io/en/latest", None),
}

# sphinx_tabs config
sphinx_tabs_disable_tab_closing = True

# HTML output options
html_theme = "sphinx_book_theme"
