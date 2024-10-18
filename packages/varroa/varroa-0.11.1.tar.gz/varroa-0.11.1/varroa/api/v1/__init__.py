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

from varroa.api.v1.resources import ip_usage
from varroa.api.v1.resources import security_risk
from varroa.api.v1.resources import security_risk_type


def initialize_resources(api):
    api.add_resource(ip_usage.IPUsageList, "/v1/ip-usage/")
    api.add_resource(
        security_risk_type.SecurityRiskTypeList, '/v1/security-risk-types/'
    )
    api.add_resource(
        security_risk_type.SecurityRiskType, '/v1/security-risk-types/<id>/'
    )
    api.add_resource(security_risk.SecurityRiskList, '/v1/security-risks/')
    api.add_resource(security_risk.SecurityRisk, '/v1/security-risks/<id>/')
