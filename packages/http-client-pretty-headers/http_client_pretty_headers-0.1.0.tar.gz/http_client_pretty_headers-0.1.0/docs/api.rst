.. _api:

API Reference
=============

.. module:: http_client_pretty_headers

Main Interface
--------------

There are three ways to use this library.

1. Use :py:func:`activate_httpclient_pretty` to activate pretty headers for the whole codebase.
2. Use :py:class:`HttpClientPrettyHeaders` as a context manager (see :py:meth:`HttpClientPrettyHeaders.__enter__`) to activate pretty headers for the designated part of the codebase.
3. Use :py:func:`httpclient_print_func_closure` to replace the print function manually.

.. autoclass:: http_client_pretty_headers.HttpClientPrettyHeaders
   :members:
   :undoc-members:
   :special-members:
   :exclude-members: __dict__,__weakref__, __module__, __annotations__, __abstractmethods__

.. autofunction:: http_client_pretty_headers.activate_httpclient_pretty
.. autofunction:: http_client_pretty_headers.deactivate_httpclient_pretty

Alternative Output
------------------

.. autoclass:: http_client_pretty_headers.LoggingOutput
   :members:
   :undoc-members:

Lower level Output
------------------

.. autoclass:: http_client_pretty_headers.AbstractOutput
   :members:
   :undoc-members:

.. autoclass:: http_client_pretty_headers.PrintOutput
   :members:
   :undoc-members:
