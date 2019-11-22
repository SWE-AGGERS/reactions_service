import json

import requests
from flask import jsonify
from requests import Timeout

from service.background import count_reactions_async
from flask import Blueprint
from service.database import db, Reaction, Counters
from service.constants import STORIES_SERVICE_IP, STORIES_SERVICE_PORT

reacts = Blueprint('reacts', __name__)


@reacts.route('/reactions/<storyid>/<reactiontype>/<reacterid>', methods=['POST'])
def _reaction(storyid, reactiontype, reacterid):
    try:
        resp_message = add_reaction(reacterid, storyid, reactiontype)
        return jsonify({'reply': resp_message,
                        'reaction': reactiontype,
                        'story_id': storyid})

    except StoryNonExistsError as err_msg:
        return jsonify({'reply': str(err_msg),
                        'reaction': reactiontype,
                        'story_id': storyid})


@reacts.route('/reactions/<storyid>', methods=['GET'])
def _counts(storyid):
    # return number of like and dislike for a story (async updated)
    try:
        counter = count_reaction(storyid)

        return counter.to_json()  # storyid, likes, dislikes

    except StoryNonExistsError:
        return Counters.error_to_json()

    except CounterNonExistsError:
        return Counters.zeros_to_json(storyid)

    except StoryServiceConnectionFailed:
        return Counters.error_to_json()


def add_reaction(reacter_id, story_id, reaction_type):
    """
    Add the reaction of type reaction_type to the story of id
    story_id from the user reacter_id.
    The reaction is immediately added to the DB, but the counters
    will be updated asynchronously
    @param reacter_id: id of user who react
    @param story_id: id of the story
    @param reaction_type: type of reaction [1=like, 2=dislike]
    @rtype: string
    @return: return message
    @raise StoryNonExistsError: if requested story not exists
    """
    if not exist_story(story_id):
        raise StoryNonExistsError('Story not exists!')

    old_reaction = Reaction.query.filter_by(
        user_id=reacter_id, story_id=story_id).first()

    if old_reaction is None:
        new_reaction = Reaction()
        new_reaction.user_id = reacter_id
        new_reaction.story_id = story_id
        new_reaction.type = reaction_type
        db.session.add(new_reaction)
        db.session.commit()
        message = 'Reaction created!'
    else:
        if int(reaction_type) == int(old_reaction.type):
            message = 'Reaction removed!'
            db.session.delete(old_reaction)
            db.session.commit()
        else:
            old_reaction.type = reaction_type
            db.session.commit()
            message = 'Reaction changed!'
        # # Update DB counters
    res = count_reactions_async.delay(story_id=story_id)
    return message


class StoryNonExistsError(Exception):
    def __init__(self, value):
        self.value = value


class CounterNonExistsError(Exception):
    def __init__(self, value):
        self.value = value


def count_reaction(storyid):
    """
    Return the number of reactions of a story identified by storyd
    @param storyid: id of the story
    @rtype: Counter
    @return: Counter object if exist a counter with requested story
    @raise StoryNonExistsError: if requested story not exists
    @raise CounterNonExistsError: if counter of the story not exists
    """
    if not exist_story(storyid):
        # if exists remove counter of non-exist story
        q = Counters.query.filter_by(story_id=storyid).first()

        if q is not None:
            db.session.delete(q)
            db.session.commit()

        raise StoryNonExistsError('Story not exists!')

    q = Counters.query.filter_by(story_id=storyid).first()

    if q is None:
        raise CounterNonExistsError('Counter not yet created!')
    return q


def exist_story(story_id):
    """
    Check if the story identified by story_id exists, by calling
    Story Service
    @param story_id: id of the story
    @return: True if story exists, False otherwise
    """
    # call Story service API
    try:
        url = 'http://' + STORIES_SERVICE_IP + ':' + STORIES_SERVICE_PORT + '/story_exist/' + story_id
        reply = requests.get(url, timeout=1)
        body = json.loads(str(reply.data, 'utf8'))
        return body['result'] == 1
    except Timeout:
        return False


class StoryServiceConnectionFailed(Exception):
    def __init__(self, value):
        self.value = value

