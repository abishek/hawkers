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
    db.drop_all()
    db.create_all()

@manager.command
def populateadmin() :
	from hawkers.models import db, User
	print User.query.delete(), " rows deleted from User"
	
	# add admin user
	admin_user = User()
	admin_user.first_name = 'Admin'
	admin_user.last_name = 'istrator'
	admin_user.login = 'admin'
	admin_user.email = 'webmaster@rohabini.com'
	admin_user.password = generate_password_hash(app.config['ADMIN_PASSWORD'])
	admin_user.hawker = None
	admin_user.is_admin = True
	db.session.add(admin_user)
	db.session.commit()
	
@manager.command
def populatevendor() :
    populateadmin()
    from hawkers.models import db, User
    
    # add a vendor user
    vendor_user = User()
    vendor_user.first_name = 'Test'
    vendor_user.last_name = 'Vendor'
    vendor_user.login = 'vndr'
    vendor_user.email = 'webmaster@rohabini.com'
    vendor_user.password = generate_password_hash('vndrP')
    vendor_user.hawker = None
    vendor_user.is_admin = False
    db.session.add(vendor_user)
    db.session.commit()
    
@manager.command
def populatedata() :
    from hawkers.models import db, Hawker, Food, User
    populatevendor()
    # Empty the tables first
    print(Hawker.query.delete(), " rows deleted from Hawker")
    print(Food.query.delete(), " rows deleted from Food")
    
	# add hawker
    h = Hawker()
    h.name = 'Indian Stall'
    h.address = 'Golden Palace Eating House, 5 Kallang Sector, Singapore'
    h.pincode = 349279
    h.contact_number = 99991111
    h.email = 'goda.abishek@gmail.com'
    h.owner = User.query.filter_by(login='vndr').first().id
    db.session.add(h)
    db.session.commit()
    
    # add foods for this menu
    f1 = Food()
    f1.name = 'Dosa'
    f1.description = 'Indian style lentil pancakes'
    f1.price = 1.00
    f1.is_available = True
    f1.image = 'dosa.jpg'
    f1.hawker_id = h.id

    f2 = Food()
    f2.name = 'South Indian Lunch'
    f2.description = 'Complete Platter with variety rice and side dish'
    f2.price = 3.20
    f2.is_available = False
    f2.image = '2.jpg'
    f2.hawker_id = h.id

    f3 = Food()
    f3.name = 'Idli'
    f3.description = 'Indian Style steamed rice cakes'
    f3.is_available = True
    f3.price = 1.00
    f3.image = 'idli.jpg'
    f3.hawker_id = h.id

    db.session.add_all([f1, f2, f3])
    db.session.commit()
    	
manager.run()
