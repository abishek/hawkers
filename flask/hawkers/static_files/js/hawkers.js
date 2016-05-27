var main = function() {

}

$.postJSON = function(url, data, callback) {
    return $.ajax({
        'type': 'POST',
        'url': url,
        'contentType': 'application/json',
        'data': data,
        'dataType': 'json',
        'success': callback
    });
};

var submitpin = function(event) {
	var $pincode = $.trim($("#basic-pincode").val());
	if($pincode.length == 0) {
		alert("Enter a pincode to continue.")
		event.preventDefault();
		return;
	}
	if($pincode.length != 6) {
		alert("Pincodes are 6 digit numbers. Try again.");
		event.preventDefault();
		$("#basic-pincode").val('');
		return;
	}
	if(!$.isNumeric($pincode)) {
		alert("Pincodes are 6 digit numbers. Try again.");
		event.preventDefault();
		$("#basic-pincode").val('');
		return;		
	}
	$distance = getDistance($pincode);
	event.preventDefault();
}

$(document).ready(main);
$(document).on("click", "#submitpin", submitpin);