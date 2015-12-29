( function() {
	var app = angular.module("hawkerApp", [ "hawkerAppComponents", "hawkerAppControllers"]);
	app.controller("hawkerAppController", function() {
		// top level controller. Mostly acts as global data store :)
		this.hawkerList = [];
	});

} )();