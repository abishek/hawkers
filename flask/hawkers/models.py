from hawkers import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Hawker(db.Model) :
	'''Basic table of hawkers. Each hawker has a menu of food items.'''
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30))
	address = db.Column(db.String(150))
	pincode = db.Column(db.Integer) 
	contact_number = db.Column(db.Integer, unique=True)
	menus = db.relationship('Menu')
	
	def __repr__(self) :
		return '%s, %s - %d'%(self.name, self.address, self.pincode)

class MenuType(db.Model) :
	"Type of cuisine. Mapping table."
	
	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String(50))
	
	def __repr__(self) :
		return self.type
	 
class Menu(db.Model) :
	'''Menu published by a hawker. Aggregate of food items.'''
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	menu_type_id = db.Column(db.Integer, db.ForeignKey('menu_type.id'))
	hawker_id = db.Column(db.Integer, db.ForeignKey('hawker.id'))
		
	def __repr__(self) :
		return self.name

class Food(db.Model) :
	'''Actual food listing. Each food belongs in a menu.'''
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	description = db.Column(db.String(200))
	price = db.Column(db.Float)
	is_available = db.Column(db.Boolean)
	image = db.Column(db.String(100))
	menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
	
	def __repr__(self) :
		return '%s :: %s'%(self.name, self.description)
		
	