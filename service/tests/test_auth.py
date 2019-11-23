import json
import unittest

import mock

from service.app import create_app
from service.auth import encode_auth_token
from service.database import empty_db


class TestAuth(unittest.TestCase):

    def test0(self):
        user_id = 1
        # create token
        new_token = encode_auth_token(user_id)

        _app = create_app(debug=True)
        empty_db(_app)
        with _app.test_client() as client:
            with mock.patch('service.views.reactions.exist_story') as exist_story_mock:
                exist_story_mock.return_value = True
                reply = client.post('/reactions/1/1/1', headers={'Authorization': 'Bearer ' + new_token})
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(int(body['reaction']), 1)
                self.assertEqual(body['reply'], 'Reaction created!')
                self.assertEqual(int(body['story_id']), 1)

                # wrong token
                reply = client.post('/reactions/1/1/1', headers={'Authorization': 'Bearer ' + 'a'})
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(int(body['reaction']), 1)
                self.assertEqual(body['reply'], 'Provide a valid auth token!')
                self.assertEqual(int(body['story_id']), 1)

                # wrong token: 'Bearer token malformed!'
                reply = client.post('/reactions/1/1/1', headers={'Authorization': 'a'})
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(int(body['reaction']), 1)
                self.assertEqual(body['reply'], 'Bearer token malformed!')
                self.assertEqual(int(body['story_id']), 1)
