from datetime import timedelta

DEBUG = True
PROFILE = False
BASE_URL = "http://localhost:5000"

SQLALCHEMY_DATABASE_URI = 'postgres://cwr:cwr@localhost/cwr'
SQLALCHEMY_DATABASE_URI_TEST = 'postgres://cwr:cwr@localhost/cwrtest'
SQLALCHEMY_ECHO = False

CELERY_BROKER_URL = 'redis://localhost:6380'
CELERY_RESULT_BACKEND = 'redis://localhost:6380'
# CELERY_ACCEPT_CONTENT = ['json']
CELERYBEAT_SCHEDULE = {
    'search-task1': {
        'task': 'cwr.tasks.search',
        'schedule': timedelta(seconds=10)
    },
    'search-task2': {
        'task': 'cwr.tasks.search',
        'schedule': timedelta(seconds=10)
    }
}

CELERY_TIMEZONE = 'UTC'

SECRET_KEY = "dsads399393 d ad ad dks999d **  ^67 33993 djdjjdh"
