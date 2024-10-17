#  SPDX-FileCopyrightText: 2024 Red Hat, Inc.
#
#  SPDX-License-Identifier: MIT
import ast
import http.client
import logging
import sys
from types import TracebackType
import typing
from abc import ABC, abstractmethod


class AbstractOutput(ABC):
    """Common interface for output classes.

    Primarily for typing and to show what methods are required.
    """

    @abstractmethod
    def log(self, message: str) -> None:
        """Log a message.

        :param message: The message to log.
        """
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        """Log an error message.

        :param message: The error message to log.
        """
        pass


class PrintOutput(AbstractOutput):
    """Standard output of headers using print function."""

    def __init__(self):
        self.log_handler = sys.stdout
        self.error_handler = sys.stderr

    def log(self, message: str) -> None:
        print(message, file=self.log_handler)

    def error(self, message: str) -> None:
        print(message, file=self.error_handler)


class LoggingOutput(AbstractOutput):
    """Alterantive output to use with standard logging module.


    Usage::

        >>> # Usual initialization of logger
        >>> logger = logging.getLogger(__name__)
        >>> logger.setLevel(logging.DEBUG)

        >>> # Create an output object and pass it to the logger
        >>> output = LoggingOutput(logger)
        >>> htcph = HttpClientPrettyHeaders(output)

        >>> # a) use the pretty headers within a context manager:
        >>> with htcph:
        >>>     # Your code that uses http.client
        >>>     pass

        >>> # b) activate the code for the whole codebase:
        >>> activate_httpclient_pretty(output)
        >>> # Your code that uses http.client

    :param logger_obj: The logger object to use for logging.
    :type logger_obj: logging.Logger
    """

    def __init__(self, logger_obj: logging.Logger):
        self.logger_obj = logger_obj
        self.log_level: int = logging.DEBUG
        self.error_level: int = logging.ERROR

    def log(self, message: str) -> None:
        self.logger_obj.log(self.log_level, message)

    def error(self, message: str) -> None:
        self.logger_obj.log(self.error_level, message)


class HttpClientPrettyHeaders:
    """Primary interface to get pretty classes in http.client.

    Acts as a context manager (see :meth:`__enter__`) and provides low level closure print function (see :meth:`httpclient_print_func_closure`) to manually replace the print function of :external+python:py:mod:`http.client`.

    :param output: An instance of AbstractOutput to use for logging. If not provided, :attr:`default_output_class` will be used by default.
    :type output: AbstractOutput, optional
    """

    #: The singleton instance of the class.
    _instance: typing.Optional["HttpClientPrettyHeaders"] = None
    #: The default output class to use if no output is provided.
    default_output_class = PrintOutput

    def __init__(self, output: typing.Optional[AbstractOutput] = None):
        self._output = output

    @property
    def output(self) -> AbstractOutput:
        if self._output is None:
            self._output = self.default_output_class()
        return self._output

    @output.setter
    def output(self, value: AbstractOutput) -> None:
        if not isinstance(value, AbstractOutput):
            raise TypeError("Output must be an instance of AbstractOutput")
        self._output = value

    def httpclient_print_func_closure(self) -> typing.Callable[..., None]:
        """Closure function to replace the print function of http.client.

        Usage::

            >>> http.client.print = HttpClientPrettyHeaders().httpclient_print_func_closure()

        .. seealso::
            Alternative ways to set the print function:
            :py:func:`activate_httpclient_pretty` when you want to activate pretty headers for large codebase
            :py:meth:`HttpClientPrettyHeaders.__enter__` when only designated part of your code should have pretty headers

        """

        def _httpclient_logging_func(*args: str) -> None:
            """Smart print function that calls self.output.log or self.output.error based on the arguments.

            Acts as a print function that uses known prefixes used by http.client and
            number of arguments to determine how headers should be formatted.

            :param args: The arguments to print.
            :type args: list[str]
            """
            if len(args) == 3 and args[0] in ("header:"):
                self.output.log("reply: %s" % " ".join(args[1:]))
            elif len(args) == 2 and args[0] in ("send:", "reply:"):
                """
                Some HTTP client's methods use repr on its data.
                Docstring of :external+python:py:meth:`http.client.HTTPConnection.send`:

                ``data`` can be a string object, a bytes object, an array object,
                a file-like object that supports a .read() method, or an iterable
                object.

                It uses duck typing to pass this data and only if it fails it
                falls back to other solutions. Probably because of that it goes
                the simplest way to print data - uses repr(). This representation
                is not ideal because new lines are represented as \n.

                To improve readability, we attempt to reverse the repr(), decode
                bytes to string and print each line separately. We apply similar
                treatment to the status line from _read_status().
                """
                try:
                    args_evalled: typing.Final = ast.literal_eval(args[1])
                except ValueError as err:
                    self.output.error("Failed to eval args: %s" % err)
                    self.output.log(" ".join(args))

                lines: typing.Final = args_evalled.splitlines()
                for i, line in enumerate(lines, 1):
                    if isinstance(line, (bytes, bytearray)):
                        try:
                            line = line.decode()
                        except (ValueError, AttributeError) as err:
                            line = repr(line)
                            self.output.error("Failed to decode line: %s" % err)
                    if args[0] == "send:" and i == len(lines) and line == "":
                        # skip last empty line after header requests
                        break
                    self.output.log("%s %s" % (args[0], line))
            else:
                self.output.log(" ".join(args))

        return _httpclient_logging_func

    def __enter__(self) -> None:
        """Sets the print function of the :external+python:py:mod:`http.client` module.

        This isn't called directly but used automatically when using this class within a `with` statement.

        Usage:

            >>> with HttpClientPrettyHeaders():
            >>>     # Your code that uses http.client
            >>>     pass

        .. seealso::
            Alternative ways to set the print function:
            :func:`activate_httpclient_pretty` when you want to activate pretty headers for large codebase
            :meth:`HttpClientPrettyHeaders.httpclient_print_func_closure` when you want to replace the print function manually
        """
        http.client.print = self.httpclient_print_func_closure()

    def __exit__(
        self,
        _not_used_exc_type: typing.Optional[BaseException],
        _not_used_exc_value: typing.Optional[BaseException],
        _not_used_traceback: typing.Optional[TracebackType],
    ) -> None:
        """Removes the print function from :external+python:py:mod:`http.client`.

        This is complementary to :meth:`HttpClientPrettyHeaders.__enter__`. This shouldn't be called directly.
        """
        try:
            del http.client.print
        except AttributeError:
            pass


def activate_httpclient_pretty(output: typing.Optional[AbstractOutput] = None) -> None:
    """Simple way to activate or reactivate print function for :external+python:py:mod:`http.client`.

    :param output: An object that implements :class:`AbstractOutput` to use for logging. If not provided,
        :attr:`HttpClientPrettyHeaders.default_output_class` will be used by default.
    :type output: AbstractOutput, optional

    Usage:

        >>> activate_httpclient_pretty()
        >>> # Your code that uses http.client
        >>> deactivate_httpclient_pretty()

    .. seealso::
        :func:`deactivate_httpclient_pretty` to deactivate it.
        :meth:`HttpClientPrettyHeaders.__enter__` when only designated part of your code should have pretty headers
        :meth:`HttpClientPrettyHeaders.httpclient_print_func_closure` when you want to replace the print function manually
    """
    HttpClientPrettyHeaders._instance = HttpClientPrettyHeaders(output)
    HttpClientPrettyHeaders._instance.__enter__()


def deactivate_httpclient_pretty() -> None:
    """
    Deactivate the print function for :external+python:py:mod:`http.client`.

    This is complementary to :func:`activate_httpclient_pretty`.
    """
    if not HttpClientPrettyHeaders._instance:
        return
    HttpClientPrettyHeaders._instance.__exit__(None, None, None)
    HttpClientPrettyHeaders._instance = None
