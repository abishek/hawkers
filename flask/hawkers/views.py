from flask import request, json, jsonify
from hawkers import app
import googlemaps

key = 'AIzaSyDEvi2UJv7j7fnNWjsucmXoQpfu_SrMq2Y'
client = googlemaps.Client(key)

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

