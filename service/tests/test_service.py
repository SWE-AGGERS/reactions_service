from time import sleep
from unittest import mock

from service.app import create_app
from service.database import empty_db

import unittest
import json


class TestReactionDB(unittest.TestCase):
    def test1(self):
        _app = create_app(debug=True)
        empty_db(_app)

        with _app.test_client() as client:
            with mock.patch('service.views.reactions.exist_story') as exist_story_mock:
                exist_story_mock.return_value = True
                # create like to story 1 from user 1
                reply = client.post('/reactions/1/1/1')
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(int(body['reaction']), 1)
                self.assertEqual(body['reply'], 'Reaction created!')
                self.assertEqual(int(body['story_id']), 1)

                # remove like
                reply = client.post('/reactions/1/1/1')
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(int(body['reaction']), 1)
                self.assertEqual(body['reply'], 'Reaction removed!')
                self.assertEqual(int(body['story_id']), 1)

                # create dislike
                reply = client.post('/reactions/1/2/1')
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(int(body['reaction']), 2)
                self.assertEqual(body['reply'], 'Reaction created!')
                self.assertEqual(int(body['story_id']), 1)

                # change reaction dislike -> like
                reply = client.post('/reactions/1/1/1')
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(int(body['reaction']), 1)
                self.assertEqual(body['reply'], 'Reaction changed!')
                self.assertEqual(int(body['story_id']), 1)

                # create dislike
                reply = client.post('/reactions/2/2/1')
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(int(body['reaction']), 2)
                self.assertEqual(body['reply'], 'Reaction created!')
                self.assertEqual(int(body['story_id']), 2)

                # create like of non existing story
            with mock.patch('service.views.reactions.exist_story') as exist_story_mock:
                exist_story_mock.return_value = False
                # create like to story 1 from user 1
                reply = client.post('/reactions/2/1/2')
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(int(body['reaction']), 1)
                self.assertEqual(body['reply'], 'Story not exists!')
                self.assertEqual(int(body['story_id']), 2)

    def test2(self):
        _app = create_app(debug=True)
        empty_db(_app)

        with _app.test_client() as client:
            with mock.patch('service.views.reactions.exist_story') as exist_story_mock:
                exist_story_mock.return_value = True
                for ii in range(1, 11):
                    # create like to story 1 from user 1
                    reply = client.post('/reactions/1/1/' + str(ii))
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(int(body['reaction']), 1)
                    self.assertEqual(body['reply'], 'Reaction created!')
                    self.assertEqual(int(body['story_id']), 1)

                for ii in range(11, 16):
                    # create like to story 1 from user 1
                    reply = client.post('/reactions/1/2/' + str(ii))
                    body = json.loads(str(reply.data, 'utf8'))
                    self.assertEqual(int(body['reaction']), 2)
                    self.assertEqual(body['reply'], 'Reaction created!')
                    self.assertEqual(int(body['story_id']), 1)

                # wait for background tasks
                sleep(5.0)
                # get number of likes and dislikes of a story
                reply = client.get('/reactions/1')
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(int(body['story_id']), 1)
                self.assertEqual(int(body['likes']), 10)
                self.assertEqual(int(body['dislikes']), 5)

                # get non existing yet counter
                reply = client.get('/reactions/10')
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(int(body['story_id']), 10)
                self.assertEqual(int(body['likes']), 0)
                self.assertEqual(int(body['dislikes']), 0)


            # get number of likes and dislikes of a not-exist story
            with mock.patch('service.views.reactions.exist_story') as exist_story_mock:
                exist_story_mock.return_value = False
                reply = client.get('/reactions/10')
                body = json.loads(str(reply.data, 'utf8'))
                self.assertEqual(int(body['story_id']), -1)
                self.assertEqual(int(body['likes']), -1)
                self.assertEqual(int(body['dislikes']), -1)
