from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from celery import Celery

app = Flask(__name__)
app.config.from_object('cwr.config')

db = SQLAlchemy(app)

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

import cwr.views
import cwr.tasks

if __name__ == '__main__':
    app.run()
