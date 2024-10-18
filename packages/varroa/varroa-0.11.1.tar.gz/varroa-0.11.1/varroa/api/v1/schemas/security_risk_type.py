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

from varroa.extensions import ma
from varroa import models


class SecurityRiskTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.SecurityRiskType
        load_instance = True


class SecurityRiskTypeCreateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.SecurityRiskType
        load_instance = True
        exclude = ('id',)


security_risk_type = SecurityRiskTypeSchema()
security_risk_types = SecurityRiskTypeSchema(many=True)
security_risk_typecreate = SecurityRiskTypeCreateSchema()
security_risk_typeupdate = SecurityRiskTypeCreateSchema(partial=True)
