#!/usr/bin/env python

from hawkers import app
from flaskext.script import Manager, Shell, Server

manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command("shell", Shell())

@manager.command
def createdb():
    from hawker.models import db
    db.create_all()


manager.run()

