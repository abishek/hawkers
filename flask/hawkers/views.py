from flask import request, json, jsonify, render_template
from flask.ext.mail import Mail, Message
from hawkers import app, admin
from datetime import datetime
from hawkers.models import *
from hawkers.admin_views import HawkerAdminModelView, init_login
from helpers import get_distance
import googlemaps

gmaps = googlemaps.Client(app.config['MATRIX_KEY'])
mail = Mail(app)
# Initialize flask-login
init_login(app, db)

test_data = {'hawkers': [{'name':'Hawker One', 
						  'address':'Block 1', 
						  'pincode':'111111', 
						  'contact':'99991111',
						  'menu':[{
						  'name':'Mix Veg Curry',
						  'description':'North Indian Side dish for Rice and Roti',
						  'price': 'S$1.00',
						  'isAvailable':'True',
						  'image':'/hawkers/images/1.jpg'
						  }, {
						  'name':'South Indian Lunch',
						  'description':'Complete Platter with variety rice and side dish',
						  'price': 'S$3.20',
						  'isAvailable':'False',
						  'image':'/hawkers/images/2.jpg'
						  }, {
						  'name':'Brussels Sprouts',
						  'description':'Indian Style garnished with mustard',
						  'price': 'S$1.00',
						  'isAvailable':'True',
						  'image':'/hawkers/images/3.jpg'
						  }]}, 
						 {'name':'Hawker Two', 
						  'address':'Block 2', 
						  'pincode':'222222', 
						  'contact':'99992222',
						  'menu':[{
						  'name':'Idli Vada Combo',
						  'description':'Authentic South Indian Breakfast Combo',
						  'price': 'S$2.00',
						  'isAvailable':'True',
						  'image':'/hawkers/images/4.jpg'
						  }, {
						  'name':'Kadai Paneer',
						  'description':'North Indian side dish for Rotis and Pratas',
						  'price': 'S$2.20',
						  'isAvailable':'True',
						  'image':'/hawkers/images/5.jpg'
						  }, {
						  'name':'Indian Milk Sweets',
						  'description':'Milk and Cashew sweets to saitate the sweet tooth.',
						  'price': 'S$1.50',
						  'isAvailable':'True',
						  'image':'/hawkers/images/6.jpg'
						  }]}]}


@app.route('/')
@app.route('/index')
def index() :
  return "Start here!"

@app.route('/distance/<int:pincode>')
def distance(pincode) :
	origin = '349279, Singapore'
	destination = '%s, Singapore'%pincode
	distance_op = gmaps.distance_matrix(origin, destination, mode="transit")
	output = {}
	if distance_op['status'] == 'OK' :
		result = distance_op['rows'][0]['elements'][0]['distance']
		if result['value'] > 1000 :
			return "Sorry, we do not serve this locality yet."
		else :
			return "Hurray!! We serve your locality already!."
	else :
		return "Some error occurred trying to fetch this information"
			
@app.route('/list/<int:pincode>')
def get_hawkers_by_pincode(pincode) :
	hawker_list = []
	# See if this pincode exists in the cache. If yes, get hawker list from there
	pc_entries = PincodeCache.query.filter_by(pincode=pincode)
	for pc_entry in pc_entries :
		hawker_list.append(Hawker.query.get(pc_entry.hawker_id))
	
	# Loop through all the hawkers in your list and see who all would serve this pincode		
	hawkers = Hawker.query.all()
	for hawker in hawkers :
		# don't re-query known folks
		if hawker in hawker_list :
			continue
		start_location = '%d, Singapore'%hawker.pincode
		dest_location = '%d, Singapore'%pincode
		dist = get_distance(gmaps, start_location, dest_location)
		if dist <= 1000 and dist > 0 :
			hawker_list.append(hawker)
			# add hawker to cache
			pc = PincodeCache()
			pc.pincode = pincode
			pc.hawker_id = hawker.id
			db.session.add(pc)
			db.session.commit()
	return jsonify({'hawkers': hawker_list})

@app.route('/order/place', methods=['POST'])
def place_order() :
	print "processing order data"
	jsondata = request.get_json()
	msg = Message('Order placed %s'%str(datetime.now()), 
					sender=app.config['DEFAULT_MAIL_SENDER'], 
					recipients=['goda.abishek@gmail.com', jsondata['email']])
	msg.html = render_template("email.html", name=jsondata['name'], phone=jsondata['HP'], 
										hawkerName=jsondata['currentHawker']['name'], 
										totalCost=jsondata['totalCost'], 
										items=jsondata['orderData'])
	#mail.send(msg)
	print msg.html
	return 'Success';

@app.route('/mail/test')
def send_test_mail() :
	msg = Message('test email from hawker app', sender=app.config['DEFAULT_MAIL_SENDER'], 
												recipients=['goda.abishek@gmail.com'])
	msg.html = "This is a test email. I hope you can receive it."
	mail.send(msg)
	return "Email sent"	

admin.add_view(HawkerAdminModelView(Hawker, db.session))
admin.add_view(HawkerAdminModelView(Menu, db.session))
admin.add_view(HawkerAdminModelView(MenuType, db.session))
admin.add_view(HawkerAdminModelView(Food, db.session))
admin.add_view(HawkerAdminModelView(PincodeCache, db.session))
admin.add_view(HawkerAdminModelView(Order, db.session))
admin.add_view(HawkerAdminModelView(OrderItem, db.session))
