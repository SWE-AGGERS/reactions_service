# encoding: utf8
import datetime as dt
import json
from time import sleep

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Reaction(db.Model):
    __tablename__ = 'reaction'

    user_id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)

    # def to_json(self):
    #     react_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
    #     return json.dumps(react_dict)


class Counters(db.Model):
    __tablename__ = 'counters'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    story_id = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    time_updated = db.Column(db.DateTime)

    # time_updated = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __init__(self, *args, **kw):
        super(Counters, self).__init__(*args, **kw)
        self.time_updated = dt.datetime.now()

    def to_json(self):
        # counters_d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        counters_d = {'story_id': self.story_id,
                      'likes': self.likes,
                      'dislikes': self.dislikes,
                      'time_updated': self.time_updated.strftime("%d/%m/%Y")}
        return json.dumps(counters_d)

    @staticmethod
    def zeros_to_json(story_id):
        return json.dumps({'story_id': story_id,
                           'likes': 0,
                           'dislikes': 0,
                           'time_updated': dt.datetime.now().strftime("%d/%m/%Y")})

    @staticmethod
    def error_to_json():
        return json.dumps({'story_id': -1,
                           'likes': -1,
                           'dislikes': -1})


def empty_db(app):
    sleep(2)
    with app.app_context():
        db.drop_all()
        db.create_all()
