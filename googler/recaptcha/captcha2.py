##
# Copyright (C) 2015 Christian Jurk <commx@commx.ws>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##

from googler.utils.compat import urlencode

import requests

"""
This module implements methods to generate HTML code for use with reCAPTCHA 2.0
as well as methods for verification of user response.
"""


def head_html(**kwargs):
    """
    Return the HTML code to be placed into the <head> section of a HTML document.

    :param hl: User language (optional); If not specified, the language is auto-detected
    :return: HTML code
    """

    s = '<script src="https://www.google.com/recaptcha/api.js{}" async defer></script>'

    if kwargs:
        for key, value in kwargs:
            if key not in ('onload', 'render', 'hl'):
                raise AttributeError('Invalid keyword argument: {!r}'.format(key))
            if key == 'render' and value not in ('explicit', 'onload'):
                raise ValueError('Keyword argument {!r} must have one of '
                                 'the following values: explicit, onload'.format(key))

        s = s.format('?' + urlencode(kwargs))

    return s


def widget_html(site_key, theme=None, type_=None):
    """
    Return the HTML code for the reCAPTCHA widget.

    :param site_key: Site key
    :param theme: Theme, may be "dark" or "light" (optional)
    :param type_: Data type, may be "image" or "audio" (optional)
    :return: HTML code
    """

    attrs = {'data-sitekey': site_key}
    s = '<div class="g-recaptcha" {attrs}></div>'

    if theme:
        if theme not in ('light', 'dark'):
            raise ValueError('theme must be "light" or "dark"')
        attrs['data-theme'] = theme

    if type_:
        if type_ not in ('image', 'audio'):
            raise ValueError('type_ must be "image" or "audio"')
        attrs['data-type'] = type_

    return s.format(attrs=' '.join(['{}="{}"'.format(k, v) for k, v in attrs.items()]))


def verify(secret_key, response, remote_ip=None):
    """
    Verify user response.

    This method returns silently when the response is correct.

    :param secret_key: Shared secret key
    :param response: User response token
    :param remote_ip: User IP address (optional)
    :raises: RecaptchaError in case the response is invalid or cannot be verified
    :return: RecaptchaResponse object
    """

    verification_url = 'https://www.google.com/recaptcha/api/siteverify'
    data = {'secret': secret_key, 'response': response}

    if remote_ip:
        data['remoteip'] = remote_ip

    try:
        r = requests.post(verification_url, data=data)
    except requests.RequestException:
        raise RecaptchaError('request-error')
    else:
        resp = r.json()

        if not resp['success']:
            raise RecaptchaError(resp.get('error-codes'))


class RecaptchaError(ValueError):
    """
    API Response wrapper.
    """

    def __init__(self, error_codes=None):
        self.error_codes = error_codes or []

    def __str__(self):
        if len(self.error_codes) > 1:
            return ', '.join([self.translate_error_code(x) for x in self.error_codes])
        elif len(self.error_codes) == 1:
            return self.translate_error_code(self.error_codes[0])
        else:
            return 'No error codes'

    @staticmethod
    def translate_error_code(s):
        """
        Translate error code in friendly version.

        :param s: Error code
        :return: Friendly version of the error code
        """
        if s == 'request-error':
            return 'The request has failed'
        elif s == 'missing-input-secret':
            return 'The secret parameter is missing'
        elif s == 'invalid-input-secret':
            return 'The secret parameter is invalid or malformed'
        elif s == 'missing-input-response':
            return 'The response parameter is missing'
        elif s == 'invalid-input-response':
            return 'The response parameter is invalid or malformed'
        else:
            raise AttributeError('{!r} is not a valid error code'.format(s))