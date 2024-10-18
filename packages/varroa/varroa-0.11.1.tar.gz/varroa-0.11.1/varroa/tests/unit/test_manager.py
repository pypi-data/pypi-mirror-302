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

import datetime
from unittest import mock

from varroa.common import exceptions
from varroa import manager
from varroa import models
from varroa.tests.unit import base


class TestManager(base.TestCase):
    def setUp(self):
        super().setUp()
        self.manager = manager.Manager()

    @mock.patch('varroa.worker.api.WorkerAPI.process_security_risk')
    def test_create_security_risk(self, mock_process):
        security_risk = models.SecurityRisk(
            ipaddress='192.168.1.1',
            type_id=self.create_security_risk_type().id,
            time=datetime.datetime(2020, 2, 2),
            expires=datetime.datetime(2020, 2, 3),
        )

        result = self.manager.create_security_risk(self.context, security_risk)

        self.assertIsNotNone(result.id)
        mock_process.assert_called_once_with(self.context, result.id)

    def test_delete_security_risk(self):
        security_risk = self.create_security_risk()

        self.manager.delete_security_risk(self.context, security_risk)

        self.assertIsNone(models.SecurityRisk.query.get(security_risk.id))

    def test_delete_security_risk_type_success(self):
        security_risk_type = self.create_security_risk_type()

        self.manager.delete_security_risk_type(
            self.context, security_risk_type
        )

        self.assertIsNone(
            models.SecurityRiskType.query.get(security_risk_type.id)
        )

    def test_delete_security_risk_type_in_use(self):
        security_risk = self.create_security_risk()

        with self.assertRaises(exceptions.SecurityRiskTypeInUse):
            self.manager.delete_security_risk_type(
                self.context, security_risk.type
            )
