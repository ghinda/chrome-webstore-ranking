import logging

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from cwr.app import app, db

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
logger = logging.getLogger(__file__)

if __name__ == "__main__":
    manager.run()
