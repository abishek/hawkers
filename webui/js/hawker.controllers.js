( function() {
	var app = angular.module("hawkerAppControllers", [ ]);

	app.controller("PincodeController", ['$http', function($http, appController) {
		this.locateHawkers = function() {
			console.log(this.pincode);
			// submit this pincode and get a list of hawkers as result.
			$http.get('/hawkers/list/'+this.pincode+'/')
			.success(function(data) {
				// populate this data into the list group below
				console.log(data);
				appController.hawkerList = data.hawkers; 
			})
			.error(function(data, status) {
				console.warn(data, status);
			});
		};
	}]);

	app.controller("HawkerListController", ["$http", function($http) {
		this.hawkerList = [];
	}]);

	app.controller("OrderController", ["$http", function($http) {
		this.orderData = [];
	}]);

}) ();