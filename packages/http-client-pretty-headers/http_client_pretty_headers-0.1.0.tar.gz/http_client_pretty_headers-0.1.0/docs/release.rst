Release Process
===============

Pretty headers for http.client uses dynamic version based on the git tag using `hatch-vcs`. There are multiple ways to test the package release before the release.

Local build
-----------

To release locally:

1. run `uv build` to create a source and wheel distribution.

Local GitHub Actions
--------------------

* Install `act <https://nektosact.com/>`_.
* Install `Docker <https://www.docker.com/get-started/>`_ and start the service.

.. note::
   While `act` may work with podman, it did not work correctly for me.

1. Navigate to some directory, for example the root of the repository.
2. Create a directory to hold the artifacts:

   .. code-block:: sh

      mkdir -p .artifacts

3. Run the artifact server and keep it running in background:

   .. code-block:: sh

      docker run --rm --name artifact-server -p 8080:8080 --add-host host.docker.internal:host-gateway -e AUTH_KEY='' --detach ghcr.io/jefuller/artifact-server:latest

4. Navigate to the root of the repository if not already there.

5. To test the build process and test of the distribution run following command:

   .. code-block:: sh

      act --env ACTIONS_RUNTIME_URL=http://host.docker.internal:8080/ --env ACTIONS_RUNTIME_TOKEN='' --env ACTIONS_CACHE_URL=http://host.docker.internal:8080/ --env ACTIONS_RESULTS_URL=http://host.docker.internal:8080/ --artifact-server-path .artifacts -P ubuntu-latest=-self-hosted --job test-distribution

   It should not fail on any of the steps.

6. Stop the artifact server:

   .. code-block:: sh

      docker stop artifact-server

.. _testpypi-with-github-actions:

TestPyPI with GitHub Actions
----------------------------

To test the release on TestPyPI, first find out the current version to determine version to push to TestPyPI.

1. Locally run:

   .. code-block:: sh

      uv run hatch version

   to display the current version. It will likely contain a `+g`, git hash and date, which is `local version identifier <https://packaging.python.org/en/latest/specifications/version-specifiers/#local-version-identifiers>`_ which is not a valid version for PyPI.

2. In your mind, take version from the left up until `.dev` and drop `.dev` and everything to the right of it. Bump Major, or Minor or Patch version. Append `.dev1` to the end if this is the first test release to the TestPyPI. Increase `1` if there has been already a release on TestPyPI. Check `Release history of http-client-pretty-headers <https://test.pypi.org/project/http-client-pretty-headers/#history>`_ if unsure.

To publish the release to TestPyPI:

1. Open a web browser and navigate to GitHub repository, actions tab.

2. Click on the `Publish Python 🐍 distribution 📦 to TestPyPI` workflow.

3. Enter version created in the previous step.

4. Click on `Run workflow`.

It should suceed and provide you a link to newly released package on TestPyPI.

Failure like:

.. code-block:: sh

   ERROR    HTTPError: 400 Bad Request from https://test.pypi.org/legacy/
            Bad Request

might indicate wrong version number. Or anything else really.

TestPyPI with local twine
-------------------------

To debug issues with TestPyPI with GitHub Actions:

1. Create a new development version as described above in :ref:`testpypi-with-github-actions`. Set and possibly export it to environment variable `SETUPTOOLS_SCM_PRETEND_VERSION`.

2. Ensure you have a valid token with TestPyPI. Here I use a variable `TOKEN` for it. Or, use `~/.pypirc` to configure it.

3. Run:

   .. code-block:: sh

      uv publish --publish-url https://test.pypi.org/legacy/ --token "$TOKEN"

Public release
--------------

The main artifact of the public release is a python package published to PyPI. Publication is done with GitHub Action that is triggered by pushing a git tag with prefix `v` followed by a version number.

To release:

1. Edit `CHANGELOG.md` to add a new entry for the release and commit the changes.
2. Push changes to `devel` branch to GitHub.
3. Create a new git tag with prefix `v` followed by a version number.
4. Push the tag to GitHub.

GitHub Actions should take care of the rest.
