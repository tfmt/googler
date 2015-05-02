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

from Crypto.Cipher import AES
from googler.utils import compat

import base64


def get_html(email, private_key, public_key, use_tls=True, label=None):
    """
    Get Mailhide HTML code for a specific E-mail address.

    :param email: E-mail address to use for mailhide
    :param private_key: Private key
    :param public_key: Public key
    :param use_tls: Specifies whether to use https for the URL
    :param label: Optional - if present, it will display that label instead of a truncated E-mail address
    :return: Mailhide HTML code
    """
    url = get_url(email, private_key, public_key, use_tls)

    html_anchor_begin = '''<a href="%(href)s" onclick="window.open('%(href)s', '', 'toolbar=0,scrollbars=0,''' \
            '''location=0,statusbar=0,menubar=0,resizable=0,width=500,height=300');return false;" ''' \
            '''title="Reveal this e-mail address">'''
    html_anchor_end = '</a>'

    context = {
        'a_begin': html_anchor_begin % {
            'href': url
        },
        'a_end': html_anchor_end
    }

    if not label:
        email_parts = email.split('@', 2)
        username = email_parts[0]
        host = email_parts[1]
        prefix = ''

        if len(username) in range(1, 4 + 1):
            prefix = username[:2]
        elif len(username) in range(5, 6 + 1):
            prefix = username[:3]
        elif len(username) >= 7:
            prefix = username[:4]

        context.update({
            'prefix': prefix,
            'host': host
        })

        return '%(prefix)s%(a_begin)s…%(a_end)s@%(host)s' % context
    else:
        context.update({
            'label': label
        })

        return '%(a_begin)s%(label)s%(a_end)s' % context


def get_url(email, private_key, public_key, use_tls=True):
    """
    Get Mailhide URL for a specific E-mail address.

    :param email: E-mail address to use for mailhide
    :param private_key: Private key
    :param public_key: Public key
    :param use_tls: Specifies whether to use https for the URL
    :return: Mailhide URL
    """
    enc = _encrypt_email_address(email, private_key)

    ctx = {
        'public_key': public_key,
        'encrypted_email': base64.urlsafe_b64encode(enc).decode('utf-8')
    }

    url = 'https' if use_tls else 'http'
    url += '://www.google.com/recaptcha/mailhide/d?k=%(public_key)s&c=%(encrypted_email)s' % ctx

    return url


def _decrypt_email_address(cipher_text, private_key):
    """
    Decrypt a encrypted E-mail address.
    :param cipher_text: Encrypted E-mail address
    :param private_key: Private key
    :return: E-mail address in plain text
    """
    if compat.PY2:
        iv = chr(0) * 16
    else:
        iv = bytes([0] * 16)
    key = base64.b16decode(private_key, casefold=True)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plain_text = _unpad(cipher.decrypt(cipher_text))

    return plain_text.decode('utf-8')


def _encrypt_email_address(email, private_key):
    """
    Encrypt the E-mail address with AES-128-CBC.

    :param email: E-mail address
    :return:
    """
    padded_email = _pad(email.encode('utf-8'))
    key = base64.b16decode(private_key, casefold=True)

    # Create an initialization vector (16 times 0x00)
    if compat.PY2:
        iv = chr(0) * 16
    else:
        iv = bytes([0] * 16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    return cipher.encrypt(padded_email)


def _pad(s):
    """
    A helper function for padding a message for use with AES.

    :param s: Source string
    :return: Padded string
    """
    x = AES.block_size - len(s) % AES.block_size

    if compat.PY2:
        pad = chr(x) * x
    else:
        pad = bytes([x]) * x
    return s + pad


def _unpad(s):
    """
    A helper function to remove padding from a previously padded message.
    :param s: Padded string
    :return: Unpadded string
    """
    if compat.PY2:
        return s[:-ord(s[-1])]
    else:
        return s[:-s[-1]]