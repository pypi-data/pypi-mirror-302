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

from oslo_log import log as logging

from varroa.common import exceptions
from varroa.extensions import db
from varroa import models
from varroa.worker import api as worker_api

LOG = logging.getLogger(__name__)


class Manager:
    def __init__(self):
        self.worker_api = worker_api.WorkerAPI()

    def create_security_risk(self, context, security_risk):
        db.session.add(security_risk)
        db.session.commit()
        self.worker_api.process_security_risk(context, security_risk.id)
        return security_risk

    def delete_security_risk(self, context, security_risk):
        db.session.delete(security_risk)
        db.session.commit()

    def delete_security_risk_type(self, context, security_risk_type):
        vulnerabilities = (
            db.session.query(models.SecurityRisk)
            .filter_by(type_id=security_risk_type.id)
            .all()
        )
        if vulnerabilities:
            raise exceptions.SecurityRiskTypeInUse(
                f'SecurityRiskType {security_risk_type.id} is in use'
            )
        db.session.delete(security_risk_type)
        db.session.commit()
