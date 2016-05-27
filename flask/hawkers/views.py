from datetime import datetime
import os

from flask import request, json, jsonify, render_template, send_from_directory, redirect
from flask.ext.mail import Mail, Message

import googlemaps

from hawkers import app
from hawkers.models import *
from hawkers.admin_views import HawkerAdminModelView, ImageAdminView
from helpers import get_distance

gmaps = googlemaps.Client(app.config['MATRIX_KEY'])
mail = Mail(app)

# Actual App
@app.route('/index')
@app.route('/')
def goto_webapp() :
    return redirect('/web/index.html')

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
            
    # now we have the list of hawkers. construct the response in the format needed
    hlist = []
    for h in hawker_list :
        hlist.append(h.get_map())
        
    return jsonify({'hawkers': hlist})

@app.route('/order/place', methods=['POST'])
def place_order() :
    jsondata = request.get_json()
    dt = datetime.utcnow()
    o = Order()
    o.date_time = dt
    o.customer_name = jsondata['name']
    o.customer_email = jsondata['email']
    o.customer_phone = jsondata['HP']
    o.hawker = Hawker.query.get(jsondata['currentHawker']['vid'])
    o.menu = Menu.query.get(jsondata['currentHawker']['mid'])
    db.session.add(o)
    
    for item in jsondata['orderData'] :
        f = Food.query.get(item['fid'])
        oi = OrderItem()
        oi.food = f
        oi.order = o
        db.session.add(oi)
        
    db.session.commit()   
        
    msg = Message('Order placed %s'%str(dt), 
                    sender=app.config['DEFAULT_MAIL_SENDER'], 
                    recipients=['goda.abishek@gmail.com', jsondata['email']])
    msg.html = render_template("email.html", name=jsondata['name'], phone=jsondata['HP'], 
                                        hawkerName=jsondata['currentHawker']['name'], 
                                        totalCost=jsondata['totalCost'], 
                                        items=jsondata['orderData'])
    #mail.send(msg)
    print msg.html
    return 'Success'

@app.route('/mail/test')
def send_test_mail() :
	msg = Message('test email from hawker app', sender=app.config['DEFAULT_MAIL_SENDER'], 
												recipients=['goda.abishek@gmail.com'])
	msg.html = "This is a test email. I hope you can receive it."
	mail.send(msg)
	return "Email sent"	

#admin.add_view(HawkerAdminModelView(Hawker, db.session))
#admin.add_view(HawkerAdminModelView(Menu, db.session))
#admin.add_view(HawkerAdminModelView(MenuType, db.session))
#admin.add_view(ImageAdminView(Image, db.session))
#admin.add_view(HawkerAdminModelView(Food, db.session))
#admin.add_view(HawkerAdminModelView(PincodeCache, db.session))
#admin.add_view(HawkerAdminModelView(Order, db.session))
#admin.add_view(HawkerAdminModelView(OrderItem, db.session))

