# encoding: utf8
import datetime as dt
import json

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Reaction(db.Model):
    __tablename__ = 'reaction'

    user_id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)

    def to_json(self):
        react_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return json.dumps(react_dict)


class Counters(db.Model):
    __tablename__ = 'counters'

    story_id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)

    def __init__(self, story_id, likes, dislikes):
        self.story_id = story_id
        self.likes = likes
        self.dislikes = dislikes

    def to_json(self):
        counters_d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return json.dumps(counters_d)

    @staticmethod
    def zeros_to_json(story_id):
        return json.dumps({'story_id': story_id,
                           'likes': 0,
                           'dislikes': 0})

    @staticmethod
    def error_to_json():
        return json.dumps({'story_id': -1,
                           'likes': -1,
                           'dislikes': -1})
