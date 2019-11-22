from time import sleep

from service.app import create_app
from service.database import empty_db
from service.views.reactions import add_reaction, \
    StoryNonExistsError, count_reaction, CounterNonExistsError
from service.background import count_reactions_async

import unittest
import mock


class TestReactionDB(unittest.TestCase):

    def test1(self):
        _app = create_app(debug=True)

        # empty DB each time for independent testing
        empty_db(_app)
        with mock.patch('service.views.reactions.exist_story') as exist_story_mock:
            exist_story_mock.return_value = True
            with _app.app_context():

                # Create like to story 1 from user 1
                res = add_reaction(1, 1, 1)
                self.assertEqual('Reaction created!', res)

                # remove like
                res = add_reaction(1, 1, 1)
                self.assertEqual('Reaction removed!', res)

                # create dislike
                res = add_reaction(1, 2, 1)
                self.assertEqual('Reaction created!', res)

                # Change reaction
                res = add_reaction(1, 2, 2)
                self.assertEqual('Reaction changed!', res)

        with mock.patch('service.views.reactions.exist_story') as exist_story_mock:
            exist_story_mock.return_value = False
            # Reaction to non existing story
            self.assertRaises(StoryNonExistsError, lambda: add_reaction(1, 1, 1))

    def test2(self):
        _app = create_app(debug=True)
        # empty DB each time for independent testing
        empty_db(_app)
        with mock.patch('service.views.reactions.exist_story') as exist_story_mock:
            exist_story_mock.return_value = True
            with _app.app_context():
                # Create like to story 1 from user 1
                for ii in range(1, 11):
                    res = add_reaction(ii, 1, 1)
                    self.assertEqual('Reaction created!', res)

                # force async counting function
                self.assertRaises(CounterNonExistsError, lambda: count_reaction(1))
                sleep(5.0)
                print(res)