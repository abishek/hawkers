from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.event import listens_for
from flask_login import UserMixin

db = SQLAlchemy()

class Hawker(db.Model) :
    '''Basic table of hawkers. Each hawker has a menu of food items.'''
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    pincode = db.Column(db.Integer, nullable=False) 
    contact_number = db.Column(db.Integer, unique=True)
    order = db.relationship('Order', backref='hawker', lazy='dynamic')
    pccache = db.relationship('PincodeCache', backref='hawker')
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def get_map(self) :
        food_list = []
        foods = []
        for food in foods :
            food_list.append(food.get_map())
            
        return {
                'vid' : self.id,
                'name' : self.name,
                'address' : self.address,
                'pincode' : self.pincode,
                'contact' : self.contact_number,
                'menu' : food_list
                }
    
    def __repr__(self) :
        return '%s, %s - %d'%(self.name, self.address, self.pincode)
        
class CutOffTime(db.Model) :
    '''Cut Off Time until when the hawker accepts orders.'''
    
    hawker_id = db.Column(db.Integer, db.ForeignKey('hawker.id'), primary_key=True)
    cut_off_time = db.Column(db.Time, nullable=False)
    
    def __repr__(self):
        return self.cut_off_time
	 
class Food(db.Model) :
	'''Actual food listing. Each food belongs in a menu.'''
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	description = db.Column(db.String(200))
	price = db.Column(db.Float, nullable=False)
	is_available = db.Column(db.Boolean, default=False)
	image = db.Column(db.Unicode(128))
	hawker_id = db.Column(db.Integer, db.ForeignKey('hawker.id'))
	
	def get_map(self) :
	    return {
	        'fid' : self.id,
	        'name' : self.name,
	        'description' : self.description,
	        'price' : 'S$%.02f'%self.price,
	        'isAvailable': 'True' if self.is_available else 'False',
	    }
	def __repr__(self) :
		return '%s :: %s'%(self.name, self.description)
    
class PincodeCache(db.Model) :
	'''Cacheing by pincode to see which hawker accepts which codes. To reduce
		troubling google maps for previosuly seen codes'''
		
	id = db.Column(db.Integer, primary_key=True)
	pincode = db.Column(db.Integer, nullable=False)
	hawker_id = db.Column(db.Integer, db.ForeignKey('hawker.id'))
	
	def __repr__(self) :
		return 'Singapore, %d '%(self.pincode)

class Order(db.Model) :
	'''Orders placed by a customer.'''
	
	# Order Specific Fields
	id = db.Column(db.Integer, primary_key=True)
	date_time = db.Column(db.DateTime)
	# Customer Details
	customer_name = db.Column(db.String(100), nullable=False)
	customer_email = db.Column(db.String(100), nullable=False)
	customer_phone = db.Column(db.Integer, nullable=False)
	customer_pincode = db.Column(db.Integer, nullable=False)
	hawker_id = db.Column(db.Integer, db.ForeignKey('hawker.id'))
	# Order State
	accepted = db.Column(db.Boolean, default=False)
	
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
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self) :
        return '%s, %s'%(self.last_name, self.first_name)
        
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
        return self.login
