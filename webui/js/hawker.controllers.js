( function() {
	var app = angular.module("hawkerAppControllers", [ "hawkerAppDS"]);

	app.controller("PincodeController", ['$http', "$scope", 'HawkerAppDS', function($http, $scope, HawkerAppDS) {
		$scope.locateHawkers = function() {
			console.log($scope.pincode);
			// submit this pincode and get a list of hawkers as result.
			$http.get('http://localhost:5000/list/'+$scope.pincode)
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
		$scope.$on('hawkerListUpdated', function() {
			$scope.hawkerList = HawkerAppDS.hawkerList;
		});

		$scope.addToOrder = function(item) {
			HawkerAppDS.addToOrderList(item);
		};
	}]);

	app.controller("OrderController", ["$http", "$scope", "HawkerAppDS", function($http, $scope, HawkerAppDS) {
		$scope.orderData = [];
		$scope.orderEmptyMessage = "No Orders yet";
		$scope.totalCost = 'S$0.00';
		$scope.$on('orderListUpdated', function() {
			$scope.orderData = HawkerAppDS.orderList;
			var price = 0;
			for(i=0; i< $scope.orderData.length; i++) {
				price += parseFloat($scope.orderData[i].price.substring(2));
			}
			$scope.totalCost = 'S$' + price.toFixed(2);
		});

		$scope.submitOrder = function(orderData) {
			console.log(orderData);
			console.log($scope.customerName);
			console.log($scope.customerEmail);
			console.log($scope.customerHP);
			var postData = {};
			postData['orderData'] = orderData;
			postData['name'] = $scope.customerName;
			postData['email'] = $scope.customerEmail;
			postData['HP'] = $scope.customerHP;
			// send this data to flask
			$http.post('http://localhost:5000/order/place', postData )
			.success(function() {
				$scope.orderEmptyMessage = "Order Placed";
				$scope.orderData = [];
				$scope.customerHP = '';
				$scope.customerEmail = '';
				$scope.customerName = '';
			})
			.error(function() {
				// handle this.
				alert("Failed to place order");
			});
		};
	}]);

}) ();