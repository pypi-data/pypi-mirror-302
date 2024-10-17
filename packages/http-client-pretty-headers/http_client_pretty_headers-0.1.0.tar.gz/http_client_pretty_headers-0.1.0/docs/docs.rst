About documentation
====================

Top level of the repository contains documents written in markdown to be rendered by GitHub. It should not contain includes or other Sphinx specific features.

Documentation under `docs/` directory is written in reStructuredText to be rendered by Sphinx either locally or, during publish process, on ReadTheDocs. reStructuredText was chosen because it is still best supported and easiest to start with. Majority of contents of the top level documents is included in the documentation. `myst` parser is used to include contents from markdown files within the reStructuredText documentation.

Python API is documented inline (aka "docstrings") with `sphinx` style.

Local build
-----------

To build the documentation locally once run:

.. code-block:: bash

   uv run --with-requirements docs/requirements.txt --from sphinx sphinx-build docs docs/_build/html


When editing docs to contiuously build the documentation run:

.. code-block:: bash

   uv run --with-requirements docs/requirements.txt sphinx-autobuild docs docs/_build/html

open the link displayed in the console to view automatically refreshed documentation.


Publish
-------

Documentation is published on ReadTheDocs automatically when a push is made to the repository.

License
-------

Documentation is distributed under the terms of the :ref:`Creative Commons Attribution 4.0 International License <doc_license>`.
