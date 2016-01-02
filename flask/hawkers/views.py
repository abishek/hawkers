from flask import request, json, jsonify
from flask.ext.mail import Mail, Message
from hawkers import app
import googlemaps
from datetime import datetime

client = googlemaps.Client(app.config['MATRIX_KEY'])
mail = Mail(app)

test_data = {'hawkers': [{'name':'Hawker One', 
						  'address':'Block 1', 
						  'pincode':'111111', 
						  'contact':'99991111',
						  'menu':[{
						  'name':'Item 1',
						  'description':'Desc 1',
						  'price': 'S$1.00',
						  'isAvailable':'True',
						  'image':'http://placehold.it/140x140'
						  }, {
						  'name':'Item 2',
						  'description':'Desc 2',
						  'price': 'S$1.20',
						  'isAvailable':'False',
						  'image':'http://placehold.it/140x140'
						  }, {
						  'name':'Item 3',
						  'description':'Desc 3',
						  'price': 'S$1.30',
						  'isAvailable':'True',
						  'image':'http://placehold.it/140x140'
						  }]}, 
						 {'name':'Hawker Two', 
						  'address':'Block 2', 
						  'pincode':'222222', 
						  'contact':'99992222',
						  'menu':[{
						  'name':'Item 1',
						  'description':'Desc 1',
						  'price': 'S$2.00',
						  'isAvailable':'True',
						  'image':'http://placehold.it/140x140'
						  }, {
						  'name':'Item 2',
						  'description':'Desc 2',
						  'price': 'S$2.20',
						  'isAvailable':'True',
						  'image':'http://placehold.it/140x140'
						  }, {
						  'name':'Item 3',
						  'description':'Desc 3',
						  'price': 'S$1.50',
						  'isAvailable':'True',
						  'image':'http://placehold.it/140x140'
						  }]}]}

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
	msg = Message('Order placed %s'%str(datetime.now()), sender=app.config['DEFAULT_MAIL_SENDER'], recipients=['goda.abishek@gmail.com'])
	msg.html = str(request.get_json())
	mail.send(msg)
	return 'Success';

@app.route('/mail/test')
def send_test_mail() :
	msg = Message('test email from hawker app', sender=app.config['DEFAULT_MAIL_SENDER'], recipients=['goda.abishek@gmail.com'])
	msg.html = "This is a test email. I hope you can receive it."
	mail.send(msg)
	return "Email sent"	
