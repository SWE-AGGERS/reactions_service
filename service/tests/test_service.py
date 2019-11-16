from time import sleep
from service.app import create_app
from service.database import empty_db

import unittest
import json


class TestReactionDB(unittest.TestCase):
    def test1(self):
        _app = create_app(debug=True)
        empty_db(_app)

        with _app.test_client() as client:

            # create like to story 1 from user 1
            reply = client.post('/reactions/1/1/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['reaction'], '1')
            self.assertEqual(body['reply'], 'Reaction created!')
            self.assertEqual(body['story_id'], '1')

            # remove like
            reply = client.post('/reactions/1/1/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['reaction'], '1')
            self.assertEqual(body['reply'], 'Reaction removed!')
            self.assertEqual(body['story_id'], '1')

            # create dislike
            reply = client.post('/reactions/1/2/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['reaction'], '2')
            self.assertEqual(body['reply'], 'Reaction created!')
            self.assertEqual(body['story_id'], '1')

            # change reaction dislike -> like
            reply = client.post('/reactions/1/1/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['reaction'], '1')
            self.assertEqual(body['reply'], 'Reaction changed!')
            self.assertEqual(body['story_id'], '1')

            # create dislike
            reply = client.post('/reactions/2/2/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['reaction'], '2')
            self.assertEqual(body['reply'], 'Reaction created!')
            self.assertEqual(body['story_id'], '2')

            # TODO create reaction of non existing story

    def test2(self):
        _app = create_app(debug=True)
        empty_db(_app)

        with _app.test_client() as client:
            for ii in range(1, 101):
                # create like to story 1 from user 1
                reply = client.post('/reactions/1/1/' + str(ii))
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(body['reaction'], '1')
                self.assertEqual(body['reply'], 'Reaction created!')
                self.assertEqual(body['story_id'], '1')

            for ii in range(101, 151):
                # create like to story 1 from user 1
                reply = client.post('/reactions/1/2/' + str(ii))
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(body['reaction'], '2')
                self.assertEqual(body['reply'], 'Reaction created!')
                self.assertEqual(body['story_id'], '1')

            # wait for background tasks
            sleep(5.0)
            # get number of likes and dislikes of a story
            reply = client.get('/reactions/1')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(body['story_id'], '1')
            self.assertEqual(body['likes'], 100)
            self.assertEqual(body['dislikes'], 50)

            # TODO get number of reactions of non existing story