import json
import unittest

import mock

from service.app import create_app
from service.database import empty_db
from service.auth import encode_auth_token

class TestAuth(unittest.TestCase):

    def test0(self):
        user_id = 1
        # create token
        new_token = encode_auth_token(user_id).decode()

        _app = create_app(debug=True)
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

    def test1(self):
        _app = create_app(debug=True)
        with _app.test_client() as client:
            reply = client.get('/createauth/1')
            body = json.loads(str(reply.data, 'utf8'))
            print()
            print(body['auth_token'])
            newtoken = body['auth_token']

            # correct token
            reply = client.get('/testauth', headers={'Authorization': 'Bearer ' + newtoken})
            body = json.loads(str(reply.data, 'utf8'))
            print(body)

            # wrong token
            reply = client.get('/testauth', headers={'Authorization': 'Bearer ' + newtoken + 'a'})
            body = json.loads(str(reply.data, 'utf8'))
            print(body)