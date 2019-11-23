import json
import unittest

from service.app import create_app
from service.database import empty_db


class TestAuth(unittest.TestCase):
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