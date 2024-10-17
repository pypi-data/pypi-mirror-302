# Pretty headers for http.client

Pretty headers for http.client is a library extends standard library http.client with a print function which prints HTTP request headers on new lines and consistently prefixes response HTTP headers. Example of usage and its output:

```python
>>> from http_client_pretty_headers import activate_httpclient_pretty
>>> activate_httpclient_pretty()
>>> from http.client import HTTPSConnection
>>> conn = HTTPSConnection("httpbin.org")
>>> conn.set_debuglevel(1)
>>> conn.request("HEAD", "/")
send: HEAD / HTTP/1.1
send: Host: httpbin.org
send: Accept-Encoding: identity
>>> resp = conn.getresponse()
reply: HTTP/1.1 200 OK
reply: Date: Tue, 08 Oct 2024 10:00:00 GMT
reply: Content-Type: text/html; charset=utf-8
reply: Content-Length: 9593
reply: Connection: keep-alive
reply: Server: gunicorn/19.9.0
reply: Access-Control-Allow-Origin: *
reply: Access-Control-Allow-Credentials: true
>>>
```

<details>
    <summary>Original output from http.client</summary>

```python
>>> from http.client import HTTPSConnection
>>> conn = HTTPSConnection("httpbin.org")
>>> conn.set_debuglevel(1)
>>> conn.request("HEAD", "/")
send: b'HEAD / HTTP/1.1\r\nHost: httpbin.org\r\nAccept-Encoding: identity\r\n\r\n'
>>> resp = conn.getresponse()
reply: 'HTTP/1.1 200 OK\r\n'
header: Date: Tue, 08 Oct 2024 10:00:00 GMT
header: Content-Type: text/html; charset=utf-8
header: Content-Length: 9593
header: Connection: keep-alive
header: Server: gunicorn/19.9.0
header: Access-Control-Allow-Origin: *
header: Access-Control-Allow-Credentials: true
>>>
```
</details>

This library could be also used with [urllib3](https://urllib3.readthedocs.io/en/latest/) because it uses http.client as its backend. While [http.client](https://docs.python.org/3/library/http.client.html) prints headers with `print` function, urllib3 uses [logging](https://docs.python.org/3/library/logging.html) module. See this example how to use logging library with Pretty headers for http.client:

```python
>>> import logging
>>> logging.basicConfig()
>>>
>>> import http.client
>>> http.client.HTTPConnection.debuglevel = 1
>>>
>>> import urllib3
>>> logging.getLogger("urllib3").setLevel(logging.DEBUG)
>>>
>>> from http_client_pretty_headers import activate_httpclient_pretty, LoggingOutput
>>> logger = logging.getLogger()
>>> logger.setLevel(logging.DEBUG)
>>> output = LoggingOutput(logger_obj=logger)
>>> activate_httpclient_pretty(output)
>>>
>>> resp = urllib3.request("HEAD", "https://httpbin.org/")
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): httpbin.org:443
DEBUG:root:send: HEAD / HTTP/1.1
DEBUG:root:send: Host: httpbin.org
DEBUG:root:send: Accept-Encoding: identity
DEBUG:root:send: User-Agent: python-urllib3/2.2.3
DEBUG:root:reply: HTTP/1.1 200 OK
DEBUG:root:reply: Date: Wed, 09 Oct 2024 10:03:00 GMT
DEBUG:root:reply: Content-Type: text/html; charset=utf-8
DEBUG:root:reply: Content-Length: 9593
DEBUG:root:reply: Connection: keep-alive
DEBUG:root:reply: Server: gunicorn/19.9.0
DEBUG:root:reply: Access-Control-Allow-Origin: *
DEBUG:root:reply: Access-Control-Allow-Credentials: true
DEBUG:urllib3.connectionpool:https://httpbin.org:443 "HEAD / HTTP/11" 200 0
>>>
```

And, finally, the library could be also used with [Requests](https://requests.readthedocs.io/en/latest/) because it uses `urllib3`, which in turn uses `http.client`. Requests, on its own, does not emit any logs nor use print. It is up to you which of the approaches above you use.

If you decide to use logging with `requests`, you should use `getLogger("urllib3")` (as above) instead of `getLogger("requests.packages.urllib3")` which is still commonly found on the internet. The use of later has been discouraged since around 2015, and no longer works since [requests 2.16.0 released on 2017-05-26](https://github.com/psf/requests/blob/main/HISTORY.md#2160-2017-05-26) when `urlib3` has been devendored from the library.

## Why

There are couple of implementations that alters Requests headers output. I haven't found a solution that would make this possible for http.client as well. On the top of that majority of that code is available without proper license. Finally I haven't found any package published on PyPI that could be used directly as a dependency. List of these implementations in no particular order:

* [Debugging HTTPS clients written with Python requests](https://romainjacquet.github.io/debugging-https-clients-written-with-python-requests.html) by Romain JACQUET on his blog.
* [StackOverflow response to question How to make httplib debugger infomation into logger debug level](https://stackoverflow.com/a/34285632) by Mallikarjunarao Kosuri

## User guide

See [User guide](docs/user_guide.rst) for more details.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for more details.

## License

Code of Pretty headers for http.client is distributed under the terms of the [MIT license](LICENSE.txt). Documentation is distributed under the terms of the [Creative Commons Attribution 4.0 International License](docs/LICENSE.txt).
