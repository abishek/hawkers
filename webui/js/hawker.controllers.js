( function() {
	var app = angular.module("hawkerAppControllers", [ "hawkerAppDS"]);

	app.controller("PincodeController", ['$http', "$scope", 'HawkerAppDS', function($http, $scope, HawkerAppDS) {
		$scope.locateHawkers = function() {
			console.log($scope.pincode);
			// submit this pincode and get a list of hawkers as result.
			$http.get('/hawkers/list/'+$scope.pincode+'/')
			.success(function(data) {
				// populate this data into the list group below
				HawkerAppDS.updateHawkerList(data.hawkers);
				HawkerAppDS.updateHawkerListMessage("No Hawkers found near your location. Our teams are working on getting more listings to help you!");
			})
			.error(function(data, status) {
				HawkerAppDS.updateHawkerList([]);
				HawkerAppDS.updateHawkerListMessage("Some Error Occurred getting hawkers for your location. Try again later.");
			});
		};
	}]);

	app.controller("HawkerListController", ['$scope', '$http', 'HawkerAppDS', function($scope, $http, HawkerAppDS) {
		$scope.hawkerList = [];
		$scope.hawkerListMessage = "There are no hawkers to show. Please search by pincode.";

		$scope.$on('messageUpdated', function() {
			$scope.hawkerListMessage = HawkerAppDS.hawkerListMessage;
		});

	}]);

	app.controller("OrderController", ["$http", "$scope", "HawkerAppDS", function($http, $scope, HawkerAppDS) {
		$scope.orderData = [];
		$scope.orderEmptyMessage = "No Orders yet";
	}]);

}) ();