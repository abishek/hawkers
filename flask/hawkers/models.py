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
    menus = db.relationship('Menu', backref='hawker', lazy='dynamic')
    pccache = db.relationship('PincodeCache', backref='hawker')
        
    def get_map(self) :
        food_list = []
        menu = self.menus.first()
        foods = menu.foods.all()
        for food in foods :
            food_list.append(food.get_map())
            
        return {
                'name' : self.name,
                'address' : self.address,
                'pincode' : self.pincode,
                'contact' : self.contact_number,
                'menu' : food_list
                }
    
    def __repr__(self) :
        return '%s, %s - %d'%(self.name, self.address, self.pincode)
        
class MenuType(db.Model) :
	"Type of cuisine. Mapping table."
	
	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String(50))
	menus = db.relationship('Menu', backref='menu_type', lazy='dynamic')
	
	def __repr__(self) :
		return self.type
	 
class Menu(db.Model) :
	'''Menu published by a hawker. Aggregate of food items.'''
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	menu_type_id = db.Column(db.Integer, db.ForeignKey('menu_type.id'))
	hawker_id = db.Column(db.Integer, db.ForeignKey('hawker.id'))
	foods = db.relationship('Food', backref='menu', lazy='dynamic')
	
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
	food = db.relationship('OrderItem', backref='food', lazy='dynamic')
	
	def get_map(self) :
	    return {
	        'name' : self.name,
	        'description' : self.description,
	        'price' : 'S$%.02f'%self.price,
	        'is_available': self.is_available,
	        'image': self.image
	    }
	def __repr__(self) :
		return '%s :: %s'%(self.name, self.description)
		
class PincodeCache(db.Model) :
	'''Cacheing by pincode to see which hawker accepts which codes. To reduce
		troubling google maps for previosuly seen codes'''
		
	id = db.Column(db.Integer, primary_key=True)
	pincode = db.Column(db.Integer)
	hawker_id = db.Column(db.Integer, db.ForeignKey('hawker.id'))
	
	def __repr__(self) :
		return 'Singapore, %d '%(self.pincode)

class Order(db.Model) :
	'''Orders placed by a customer.'''
	
	# Order Specific Fields
	id = db.Column(db.Integer, primary_key=True)
	date_time = db.Column(db.DateTime)
	# Customer Details
	customer_name = db.Column(db.String(100))
	customer_email = db.Column(db.String(100))
	customer_phone = db.Column(db.Integer)
	order = db.relationship('OrderItem', backref='order')
	
	def __repr__(self) :
		return '%s | %s | %d | %s'%(self.customer_name, self.customer_email, 
						self.customer_phone, self.date_time)
						
class OrderItem(db.Model):
	'''Food items in the order'''
	
	id = db.Column(db.Integer, primary_key=True)
	order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
	food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
	
	def __repr__(self) :
	    return '%d '%self.id
	
# Admin Login Requires a user model. Maybe can be extended to all users later on
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(64))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username	
