from flask import request, json, jsonify, render_template
from flask.ext.mail import Mail, Message
from hawkers import app, admin
import googlemaps
from datetime import datetime
from hawkers.models import *
from flask_admin.contrib.sqla import ModelView

client = googlemaps.Client(app.config['MATRIX_KEY'])
mail = Mail(app)

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

admin.add_view(ModelView(Hawker, db.session))
admin.add_view(ModelView(Menu, db.session))
admin.add_view(ModelView(MenuType, db.session))
admin.add_view(ModelView(Food, db.session))

@app.route('/')
@app.route('/index')
def index() :
  return "Start here!"

@app.route('/distance', methods=['POST'])
def distance() :
	req_data = request.get_json()
	pincode = req_data['pincode']
	origin = '349282, Singapore'
	destination = '%s, Singapore'%pincode
	distance_op = client.distance_matrix(origin, destination, mode="transit")
	output = {}
	if distance_op['status'] == 'OK' :
		output = distance_op['rows'][0]['elements'][0]['distance']
		output['status'] = distance_op['status']
		return jsonify(output)
	else :
		output['status'] = distance_op['status']
		return jsonify(output)

@app.route('/list/<int:pincode>')
def get_hawkers_by_pincode(pincode) :
	if pincode == 111111 :
		return jsonify(test_data)
	else :
		return jsonify({'hawkers':[]})

@app.route('/order/place', methods=['POST'])
def place_order() :
	print "processing order data"
	jsondata = request.get_json()
	msg = Message('Order placed %s'%str(datetime.now()), sender=app.config['DEFAULT_MAIL_SENDER'], recipients=['goda.abishek@gmail.com', jsondata['email']])
	msg.html = render_template("email.html", name=jsondata['name'], phone=jsondata['HP'], hawkerName=jsondata['currentHawker']['name'], totalCost=jsondata['totalCost'], items=jsondata['orderData'])
	#mail.send(msg)
	print msg.html
	return 'Success';

@app.route('/mail/test')
def send_test_mail() :
	msg = Message('test email from hawker app', sender=app.config['DEFAULT_MAIL_SENDER'], recipients=['goda.abishek@gmail.com'])
	msg.html = "This is a test email. I hope you can receive it."
	mail.send(msg)
	return "Email sent"	
