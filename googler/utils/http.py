##
# Googler - Google API Library for Python
#
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

from .. import __version__ as lib_version

def get_user_agent():
    """
    Build a user agent string for HTTP requests.

    :return: User agent string
    """
    return 'Googler/%s' % lib_version

def get_headers():
    """
    Build a dict with default headers.

    :return: dict
    """
    d = {
        'User-agent': get_user_agent()
    }

    return d