
from flask import jsonify
from service.background import count_reactions_async
from flask import Blueprint
from service.database import db, Reaction, Counters

import json
import requests

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
def _reactions(storyid):

    # return number of like and dislike for a story (async updated)
    try:
        counter = count_reaction(storyid)
        return counter.to_json() # storyid, likes, dislikes
    except StoryNonExistsError as err_msg:
        return count_error_json()


def exist_story(story_id):
    # call Story service API
    # resp = requests.get('/stories/'+story_id)
    # story = story_to_json(resp)
    return True


def add_reaction(reacter_id, story_id, reaction_type):
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

    def __str__(self):
        return repr(self.value)


def reacted(user_id, story_id):
    q = db.session.query(Reaction).filter_by(
        story_id=story_id, user_id=user_id).all()

    if len(q) > 0:
        return q[0].type
    return 0


def count_reaction(storyid):
    exist_story(storyid)
    if not exist_story(storyid):
        raise StoryNonExistsError('Story not exists!')
    return Counters.query.filter_by(story_id=storyid).first()


def count_error_json():
    m = {'story_id': -1,
         'likes': -1,
         'dislikes': -1}
    return json.dumps(m)
