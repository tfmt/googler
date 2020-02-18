# Overview

**googler** - A Python Library for Google APIs.

**The development of this library has ceased. Please switch to [googleapis/google-api-python-client](https://github.com/googleapis/google-api-python-client).**

The original purpose of this library was to provide library support for a subset of of the Google APIs to be used with Python 3.x at a time when Google had no plans to provide Python 3 support to its google-api-python-client. Things have changed since then: The google-api-python-client library now supports current Python versions (3.x). Please use it instead as it offer more functionality and is actively maintained. This repository will be kept archived.

## Requirements

* Python 2.6, 2.7, 3.3, 3.4 or higher
* [PyCrypto](https://www.dlitz.net/software/pycrypto/)
* [requests](http://www.python-requests.org/)

## Components

* `reCAPTCHA`
  * `captcha` reCAPTCHA 1.0
  * `captcha2` reCAPTCHA 2.0
  * `mailhide` Mailhide

* `maps`
  * `geocoding` Google Maps Geocoding functionality


## License

Googler is released under the terms of the Apache License 2.0.
