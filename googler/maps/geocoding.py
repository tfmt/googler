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

from googler.utils.http import get_headers

import requests

# Base URL for the Geocoding API
API_URL = 'maps.googleapis.com/maps/api/geocode'


class Geocode(object):
    def __init__(self, result):
        self.address_components = result.get('address_components')
        self.formatted_address = result.get('formatted_address')
        self.latitude = result['geometry']['location']['lat']
        self.longitude = result['geometry']['location']['lng']

    def __repr__(self):
        return '<Geocode: %f %f>' % (self.latitude, self.longitude)


class GeocodeResult(object):
    def __init__(self, data):
        self.status = data['status']
        self.error_message = None
        self.results = []

        if self.status != 'OK':
            self.error_message = data['error_message']

        for result in data['results']:
            self.results.append(Geocode(result))

    def __iter__(self):
        return self.results.__iter__()

    def __len__(self):
        if self.status != 'OK':
            return 0
        return len(self.results)


def get_geocode(address, api_key, format='json', use_tls=True):
    """
    Perform a Geocoding lookup (Latitude/Longitude).

    :param address: Address to geocode
    :param api_key: API key
    :param format: Output format. Can be "json" or "xml"
    :param use_tls: Specifies whether the request is made with https
    :return:
    """
    if format not in ('json', 'xml'):
        raise AttributeError('format argument must be "json" or "xml"')

    url = 'https' if use_tls else 'http'
    url += '://%s/%s' % (API_URL, format)
    headers = get_headers()
    params = {'address': address}

    try:
        r = requests.get(url, params=params, headers=headers)
    except requests.RequestException as e:
        return None
    else:
        if format == 'json':
            return GeocodeResult(r.json())
        else:
            raise NotImplementedError('xml support is currently not available')