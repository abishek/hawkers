def get_distance(maps, src_pincode, dst_pincode) :
	'''Helper function to get google matrix distance.
	Returns the distance or -1 if the call failed.'''
	
	distance_op = maps.distance_matrix(origin, destination, mode="transit")
	if distance_op['status'] == 'OK' :
		result = distance_op['rows'][0]['elements'][0]['distance']
		return result['value']
	else :
		return -1