# Overview

**googler** - A Python Library for Google APIs.

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

## Status

This is under active development. If you'd like to join hacking on this, please fork and do pull requests to it.

## Why another Google API Library?

The default Google Python API Client Library only works with Python 2.x. There are currently no plans to provide Python 3 support. Also, the library design is horrible IMO. Googler tries to provide a simple Library that provides basic API methods.

## License

Googler is released under the terms of the Apache License 2.0.