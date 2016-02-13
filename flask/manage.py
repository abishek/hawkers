#!/usr/bin/env python

from hawkers import app
from flask.ext.script import Manager, Shell, Server
from werkzeug.security import generate_password_hash

manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command("shell", Shell())

@manager.command
def createdb():
    from hawkers.models import db
    db.create_all()

@manager.command
def populatedb() :
	from hawkers.models import db, User
	admin_user = User()
	admin_user.first_name = 'Admin'
	admin_user.last_name = 'istrator'
	admin_user.login = 'admin'
	admin_user.email = 'webmaster@rohabini.com'
	admin_user.password = generate_password_hash(app.config['ADMIN_PASSWORD'])
	db.session.add(admin_user)
	db.session.commit()
	
manager.run()
