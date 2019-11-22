from celery import Celery

from service.database import db, Reaction, Counters

BACKEND = BROKER = 'redis://127.0.0.1:6379'
celery = Celery(__name__, backend=BACKEND, broker=BROKER)

_APP = None


@celery.task
def count_reactions_async(story_id):
    # story existed (previously queried Story Service)
    global _APP
    if _APP is None:
        from service.app import create_app
        app = create_app()
    else:
        app = _APP
    with app.app_context():

        num_likes = db.session.query(Reaction.story_id).filter_by(
            story_id=story_id, type=1).count()
        num_dislikes = db.session.query(Reaction.story_id).filter_by(
            story_id=story_id, type=2).count()

        q = Counters.query.filter_by(story_id=story_id).first()
        if q is not None:
            q.likes = num_likes
            q.dislikes = num_dislikes
            db.session.commit()
        else:
            q = Counters()
            q.story_id = story_id
            q.likes = num_likes
            q.dislikes = num_dislikes
            db.session.add(q)
            db.session.commit()
        return True
