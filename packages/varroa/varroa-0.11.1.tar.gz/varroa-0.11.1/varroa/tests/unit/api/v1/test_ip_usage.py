#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from varroa.tests.unit import base


class TestIPUsageAPI(base.ApiTestCase):
    def test_ip_usage_list(self):
        self.create_ip_usage()
        response = self.client.get("/v1/ip-usage/")

        self.assert200(response)
        results = response.get_json().get("results")
        self.assertEqual(1, len(results))
