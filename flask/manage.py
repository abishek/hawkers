#!/usr/bin/env python

from hawkers import app
from flask.ext.script import Manager, Shell, Server

manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command("shell", Shell())

@manager.command
def createdb():
    from hawkers.models import db
    db.create_all()

@manager.command
def populatedb() :
	from hawkers.models import db
	
manager.run()
