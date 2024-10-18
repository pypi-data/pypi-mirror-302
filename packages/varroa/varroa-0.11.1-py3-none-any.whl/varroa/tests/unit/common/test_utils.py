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

from varroa.common import utils
from varroa.tests.unit import base


class TestUtils(base.TestCase):
    def test_is_private_ip(self):
        private_ips = [
            '10.0.0.1',
            '172.16.0.1',
            '192.168.0.1',
            '10.255.255.255',
            '172.31.255.255',
            '192.168.255.255',
        ]
        public_ips = [
            '8.8.8.8',
            '203.0.113.1',
            '172.32.0.1',
            '192.169.0.1',
            '11.0.0.1',
        ]

        for ip in private_ips:
            self.assertTrue(utils.is_private_ip(ip), f"{ip} should be private")

        for ip in public_ips:
            self.assertFalse(utils.is_private_ip(ip), f"{ip} should be public")
