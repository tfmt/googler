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

from googler.recaptcha import mailhide

import unittest


class TestEncryption(unittest.TestCase):
    """
    Test case to test whether Encryption and Decryption for the mailhide
    API works correctly.
    """
    def setUp(self):
        self.private_key = 'deadbeefdeadbeefdeadbeefdeadbeef'
        self.email_address_list = (
            'x@example.com',
            'johndoe@example.com',
            'foobar.quite.long+custom@example.com',
        )

    def test_mailhide_encryption(self):
        for email in self.email_address_list:
            enc = mailhide._encrypt_email_address(email, self.private_key)
            dec = mailhide._decrypt_email_address(enc, self.private_key)
            self.assertEqual(email, dec)


if __name__ == '__main__':
    unittest.main()