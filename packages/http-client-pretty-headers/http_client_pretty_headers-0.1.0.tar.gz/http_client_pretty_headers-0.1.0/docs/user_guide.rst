.. _user_guide:

User guide
==========

Installation
------------

Install the package from GitHub repository ``git+https://github.com/pbabinca/http_client_pretty_headers.git`` using your preferred Python package manager:

.. tabs::

   .. tab:: pip

      .. code-block:: bash

         python3 -m pip install git+https://github.com/pbabinca/http_client_pretty_headers.git

   .. tab:: uv pip

      .. code-block:: bash

         uv pip install git+https://github.com/pbabinca/http_client_pretty_headers.git

Quick start
-----------

1. Import the :external+python:py:mod:`http.client` and get a connection to the server:

.. code-block:: python

   import http.client
   conn = http.client.HTTPSConnection("httpbin.org")

2. Call :external+python:py:meth:`http.client.HTTPConnection.set_debuglevel` to get any output with HTTP headers:

.. code-block:: python

   conn.set_debuglevel(1)

3. Activate pretty headers with :func:`~http_client_pretty_headers.activate_httpclient_pretty`:

.. code-block:: python

   from http_client_pretty_headers import activate_httpclient_pretty
   activate_httpclient_pretty()

4. Use the connection as usual:

.. code-block:: python

   conn.request("HEAD", "/")
   resp = conn.getresponse()

5. Deactivate pretty headers if necessary:

.. code-block:: python

   from http_client_pretty_headers import deactivate_httpclient_pretty
   deactivate_httpclient_pretty()

This approach is easiest to use in large code base but it might be problematic if there are many places with HTTP calls that you are not interested in. Use Context manager to limit the scope of pretty headers.

Context manager interface of pretty headers
-------------------------------------------

For smaller section of code use context manager. Follow steps 1-2 from quick start:

.. code-block:: python

   import http.client
   conn = http.client.HTTPSConnection("httpbin.org")
   conn.set_debuglevel(1)

Import the pretty headers class and wrap any code with the context manager to get pretty headers:

.. code-block:: python

   from http_client_pretty_headers import HttpClientPrettyHeaders

   with HttpClientPrettyHeaders():
       conn.request("HEAD", "/")
       resp = conn.getresponse()

Note that only :external+python:py:meth:`http.client.HTTPConnection.request` and :external+python:py:meth:`http.client.HTTPConnection.getresponse` methods need to be wrapped in the context manager.

Advanced manual replacement of print function
---------------------------------------------

You could also explicitly replace `print` function of :external+python:py:mod:`http.client` module on your own. Follow steps 1-2 from quick start:

.. code-block:: python

   import http.client
   conn = http.client.HTTPSConnection("httpbin.org")
   conn.set_debuglevel(1)

Import the pretty headers class and replace the print function:

.. code-block:: python

   from http_client_pretty_headers import HttpClientPrettyHeaders
   http.client.print = HttpClientPrettyHeaders().httpclient_print_func_closure()

From now on use :mod:`http.client` as usual. For example:

.. code-block:: python

   conn.request("HEAD", "/")
   resp = conn.getresponse()

Output to logging objects
-------------------------

If your code base uses logging objects, you could also use logging interface of pretty headers.

1. Follow steps 1-2 from quick start:

.. code-block:: python

   import http.client
   conn = http.client.HTTPSConnection("httpbin.org")
   conn.set_debuglevel(1)

2. If you haven't created a logger create one. By default it needs to have `DEBUG` log level. For example:

.. code-block:: python

   import logging
   logger = logging.getLogger(__name__)
   logger.setLevel(logging.DEBUG)

3. Pass the logger to :class:`LoggingOutput` class.

.. code-block:: python

   from http_client_pretty_headers import LoggingOutput
   logger_output = LoggingOutput(logger)

4. Pass the logger_output to either :func:`~http_client_pretty_headers.activate_httpclient_pretty` or :class:`~http_client_pretty_headers.HttpClientPrettyHeaders` context manager.

   .. code-block:: python

      from http_client_pretty_headers import activate_httpclient_pretty
      activate_httpclient_pretty(logger_output)
      conn.request("HEAD", "/")
      resp = conn.getresponse()

   or

   .. code-block:: python

      from http_client_pretty_headers import HttpClientPrettyHeaders
      with HttpClientPrettyHeaders(logger_output):
          conn.request("HEAD", "/")
          resp = conn.getresponse()
