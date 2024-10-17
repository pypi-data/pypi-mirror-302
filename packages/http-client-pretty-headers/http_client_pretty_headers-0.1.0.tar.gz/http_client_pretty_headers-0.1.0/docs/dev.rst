.. _dev:

Developer's Guide
=================

The core of the code is fairly simple - monkey patch a `print` function with a custom function that processess arguments and potentially modifies the output if it finds match with string prefix or number of arguments.

http.client's :external+python:py:meth:`~http.client.HTTPConnection.send` accepts multiple types of data - `string` object, a `bytes` object, an `array` object a `file`-like object that supports a `.read()` method, or an iterable object.

It uses duck typing to pass this data and only if it fails it falls back to other solutions. Probably because of that it goes the simplest way to print data - uses repr(). This representation is not ideal because new lines are represented as `\n`. To improve readability, the code attempts to:

1. reverse the :external+python:py:func:`repr()` using :external+python:py:func:`ast.literal_eval`,
2. decode `bytes` to `string`
3. print each line separately.

The same approach is done to the status line from `_read_status` of :external+python:py:class:`http.client.HTTPConnection`.
