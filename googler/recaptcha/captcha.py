# coding: utf-8

##
# Copyright (C) 2014 Christian Jurk <commx@commx.ws>
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

from googler.utils import compat
from googler.utils.http import get_user_agent

import requests

# Base URL for the reCAPTCHA API
API_URL = 'www.google.com/recaptcha/api'

# HTML code for displaying the reCAPTCHA
DISPLAY_HTML = '''
<script type="text/javascript" src="%(api_url)s/challenge?k=%(public_key)s%(error_param)s">
</script>

<noscript>
  <iframe src="%(api_url)s/noscript?k=%(public_key)s%(error_param)s" height="300" width="500" frameborder="0"></iframe>
  <br/>
  <textarea name="recaptcha_challenge_field" rows="3" cols="40" required="required"></textarea>
  <input type="hidden" name="recaptcha_response_field" value="manual_challenge"/>
</noscript>
'''

# Error codes and their more verbose descriptions
ERROR_CODES = {
    'invalid-site-private-key': 'Unable to verify the private key',
    'invalid-request-cookie': 'The challenge parameter of the verify script was incorrect',
    'incorrect-captcha-sol': 'The CAPTCHA solution was incorrect',
    'captcha-timeout': 'The solution was received after the CAPTCHA timed out',
    'recaptcha-not-reachable': 'reCAPTCHA server currently not available'
}


class RecaptchaError(ValueError):
    """
    A base exception for all reCAPTCHA related errors.
    """
    def __init__(self, error_code):
        self.error_code = error_code

    def __str__(self):
        return ERROR_CODES.get(self.error_code)


class IncorrectRecaptchaSolution(RecaptchaError):
    """
    Raised when an invalid reCAPTCHA solution was provided.
    """
    pass


class RecaptchaResponse(object):
    """
    A reCAPTCHA response object.

    You can perform boolean testing on these objects for check whether
    the response was valid or not.
    """
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code

    if compat.PY3:
        def __bool__(self):
            return bool(self.is_valid)
    else:
        def __len__(self):
            return 1 if self.is_valid else 0

    @property
    def error_message(self):
        return ERROR_CODES.get(self.error_code)


def get_html(public_key, use_tls=True, error=None):
    """
    Get HTML code to display a reCAPTCHA.

    :param public_key: Public API key
    :param use_tls: Specifies whether the request is made with https
    :param error: A optional error message to display
    :return: HTML code for reCAPTCHA
    """
    error_param = ''

    if error:
        error_param = '&error=%s' % error

    context = {
        'api_url': _build_api_url(use_tls),
        'public_key': public_key,
        'error_param': error_param
    }

    return DISPLAY_HTML % context


def verify(challenge, response, private_key, remote_ip, use_tls=True):
    """
    Verify the reCAPTCHA response.

    On success, this function returns True. Otherwise, InvalidRecaptchaSolution
    is raised.

    :param challenge: The value of recaptcha_challenge_field from the form
    :param response: The value of recaptcha_response_field from the form
    :param private_key: Private API key
    :param remote_ip: User's IP address
    :param use_tls: Specifies whether the request is made with https
    :return: True on success
    """
    url = '%s/verify' % _build_api_url(use_tls)
    payload = {
        'privatekey': private_key,
        'remoteip': remote_ip,
        'challenge': challenge,
        'response': response
    }

    headers = _build_headers()

    try:
        r = requests.post(url, data=payload, headers=headers)
    except requests.RequestException:
        raise RecaptchaError('recaptcha-not-reachable')
    else:
        response = r.text.split('\n')

        if response[0].strip() == 'true':
            return True
        else:
            error_code = response[1].strip()

            if error_code == 'incorrect-captcha-sol':
                raise IncorrectRecaptchaSolution(error_code)
            else:
                raise RecaptchaError(error_code)


def _build_api_url(use_tls=True):
    """
    Build the API URL.

    :param use_tls: Specifies whether https is used for the URL
    :return: Full API URL
    """
    scheme = 'https' if use_tls else 'http'
    return '%s://%s' % (scheme, API_URL)


def _build_headers():
    """
    Build a headers dictionary containing pre-defined headers for HTTP requests.

    :return: Headers dictionary
    """
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'User-agent': get_user_agent()
    }

    return headers