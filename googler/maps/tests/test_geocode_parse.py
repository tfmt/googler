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

from googler.maps import geocoding

import json
import unittest


class TestEncryption(unittest.TestCase):
    """
    Test case to test Geocode response parsing.
    """
    def setUp(self):
        self.response = json.loads('''{
   "results" : [
      {
         "address_components" : [
            {
               "long_name" : "1600",
               "short_name" : "1600",
               "types" : [ "street_number" ]
            },
            {
               "long_name" : "Amphitheatre Pkwy",
               "short_name" : "Amphitheatre Pkwy",
               "types" : [ "route" ]
            },
            {
               "long_name" : "Mountain View",
               "short_name" : "Mountain View",
               "types" : [ "locality", "political" ]
            },
            {
               "long_name" : "Santa Clara",
               "short_name" : "Santa Clara",
               "types" : [ "administrative_area_level_2", "political" ]
            },
            {
               "long_name" : "California",
               "short_name" : "CA",
               "types" : [ "administrative_area_level_1", "political" ]
            },
            {
               "long_name" : "United States",
               "short_name" : "US",
               "types" : [ "country", "political" ]
            },
            {
               "long_name" : "94043",
               "short_name" : "94043",
               "types" : [ "postal_code" ]
            }
         ],
         "formatted_address" : "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA",
         "geometry" : {
            "location" : {
               "lat" : 37.42291810,
               "lng" : -122.08542120
            },
            "location_type" : "ROOFTOP",
            "viewport" : {
               "northeast" : {
                  "lat" : 37.42426708029149,
                  "lng" : -122.0840722197085
               },
               "southwest" : {
                  "lat" : 37.42156911970850,
                  "lng" : -122.0867701802915
               }
            }
         },
         "types" : [ "street_address" ]
      }
   ],
   "status" : "OK"
}''')

    def test_response_parsing(self):
        result = geocoding.GeocodeResult(self.response)

        for geocode in result.results:
            print(geocode)

        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()