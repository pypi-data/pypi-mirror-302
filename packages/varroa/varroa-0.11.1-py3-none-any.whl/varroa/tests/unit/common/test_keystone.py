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

from unittest import mock

from keystoneauth1 import loading as ks_loading
from oslo_config import cfg

from varroa.common import keystone
from varroa.tests.unit import base


class TestKeystoneSession(base.TestCase):
    def setUp(self):
        super().setUp()
        self.keystone_session = keystone.KeystoneSession()

    @mock.patch.object(ks_loading, 'load_session_from_conf_options')
    @mock.patch.object(ks_loading, 'load_auth_from_conf_options')
    def test_get_session(self, mock_load_auth, mock_load_session):
        mock_auth = mock.Mock()
        mock_session = mock.Mock()
        mock_load_auth.return_value = mock_auth
        mock_load_session.return_value = mock_session

        session = self.keystone_session.get_session()

        self.assertEqual(session, mock_session)
        mock_load_auth.assert_called_once_with(cfg.CONF, 'service_auth')
        mock_load_session.assert_called_once_with(
            cfg.CONF, 'service_auth', auth=mock_auth
        )

    @mock.patch.object(ks_loading, 'load_auth_from_conf_options')
    def test_get_auth(self, mock_load_auth):
        mock_auth = mock.Mock()
        mock_load_auth.return_value = mock_auth

        auth = self.keystone_session.get_auth()

        self.assertEqual(auth, mock_auth)
        mock_load_auth.assert_called_once_with(cfg.CONF, 'service_auth')

    @mock.patch.object(keystone.KeystoneSession, 'get_auth')
    @mock.patch.object(keystone.KeystoneSession, 'get_session')
    def test_get_service_user_id(self, mock_get_session, mock_get_auth):
        mock_auth = mock.Mock()
        mock_session = mock.Mock()
        mock_get_auth.return_value = mock_auth
        mock_get_session.return_value = mock_session

        user_id = self.keystone_session.get_service_user_id()

        mock_auth.get_user_id.assert_called_once_with(mock_session)
        self.assertEqual(user_id, mock_auth.get_user_id.return_value)


class TestSkippingAuthProtocol(base.TestCase):
    def setUp(self):
        super().setUp()
        self.app = mock.Mock()
        self.skipping_auth = keystone.SkippingAuthProtocol(self.app, {})

    def test_process_request_noauth_path(self):
        request = mock.Mock()
        request.path = '/'

        result = self.skipping_auth.process_request(request)

        self.assertIsNone(result)

    @mock.patch('keystonemiddleware.auth_token.AuthProtocol.process_request')
    def test_process_request_auth_path(self, mock_process_request):
        request = mock.Mock()
        request.path = '/api/v1/resources'

        self.skipping_auth.process_request(request)

        mock_process_request.assert_called_once_with(request)
