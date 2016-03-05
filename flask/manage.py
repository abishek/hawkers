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
	db.session.add(admin_user)
	db.session.commit()
	
@manager.command
def populatecuisines() :
    from hawkers.models import db, MenuType
    print MenuType.query.delete(), " rows deleted from MenuType"
    
	# add cuisines
    thai = MenuType()
    thai.type = 'Thai'
    indmus = MenuType()
    indmus.type = 'Indian Muslim'
    chinese = MenuType()
    chinese.type = 'Chinese'
    veg = MenuType()
    veg.type = 'Vegetarian'
    noodles = MenuType()
    noodles.type = 'Noodles'
    soups = MenuType()
    soups.type = 'Soup'
    western = MenuType()
    western.type = 'Western'
    
    db.session.add_all([thai, indmus, chinese, veg, noodles, soups, western])
    db.session.commit()
 	
@manager.command
def populatedata() :
    from hawkers.models import db, Hawker, Menu, MenuType, Food
    # Empty the tables first
    print Hawker.query.delete(), " rows deleted from Hawker"
    print Menu.query.delete(), " rows deleted from Menu"
    print Food.query.delete(), " rows deleted from Food"
    
	# add hawker
    h = Hawker()
    h.name = 'Indian Stall'
    h.address = 'Golden Palace Eating House, 5 Kallang Sector, Singapore'
    h.pincode = 349279
    h.contact_number = 99991111
    db.session.add(h)
    
    # add menu for this hawker
    m = Menu()
    m.hawker = h
    mt = MenuType.query.filter_by(type = 'Indian Muslim').first()
    m.menu_type = mt
    db.session.add(m)
    
    # add foods for this menu
    f1 = Food()
    f1.name = 'Mix Veg Curry'
    f1.description = 'North Indian Side dish for Rice and Roti'
    f1.price = 1.00
    f1.is_available = True
    f1.image = '/hawkers/images/1.jpg'
    f1.menu = m

    f2 = Food()
    f2.name = 'South Indian Lunch'
    f2.description = 'Complete Platter with variety rice and side dish'
    f2.price = 3.20
    f2.is_available = False
    f2.image = '/hawkers/images/2.jpg'
    f2.menu = m

    f3 = Food()
    f3.name = 'Brussels Sprouts'
    f3.description = 'Indian Style garnished with mustard'
    f3.is_available = True
    f3.price = 1.00
    f3.image = '/hawkers/images/3.jpg'
    f3.menu = m

    db.session.add_all([f1, f2, f3])
    db.session.commit()
    	
manager.run()
