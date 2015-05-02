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

from googler.recaptcha import captcha2

import sys
import unittest


class TestCaptcha2(unittest.TestCase):
    """
    Test case to test whether some validation works or not.
    """
    def setUp(self):
        self.site_key = 'SOME-LEGACY-KEY'
        self.secret_key = 'SUPER-SECRET'

    def test_verification(self):
        self.assertRaises(captcha2.RecaptchaError, captcha2.verify, self.secret_key, 'someresponse')

        try:
            captcha2.verify(self.secret_key, 'someresponse')
        except captcha2.RecaptchaError:
            exc = sys.exc_info()[1]
            self.assertTrue('invalid-input-response' in exc.error_codes)
            self.assertTrue('invalid-input-secret' in exc.error_codes)


if __name__ == '__main__':
    unittest.main()