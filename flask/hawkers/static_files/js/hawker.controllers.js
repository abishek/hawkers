( function() {
	var app = angular.module("hawkerAppControllers", ["hawkerAppDS", "ui.bootstrap.modal"]);

	app.controller("PincodeController", ['$http', "$scope", 'HawkerAppDS', function($http, $scope, HawkerAppDS) {
		$scope.locateHawkers = function() {
			HawkerAppDS.setPincode($scope.pincode);
			// submit this pincode and get a list of hawkers as result.
			$http.get('/list/'+$scope.pincode)
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
		$scope.showModal = false;

		$scope.hawkerListMessage = "There are no hawkers to show. Please search by pincode.";

		$scope.$on('messageUpdated', function() {
			$scope.hawkerListMessage = HawkerAppDS.hawkerListMessage;
		});
		$scope.$on('hawkerListUpdated', function() {
			$scope.hawkerList = HawkerAppDS.hawkerList;
		});
		$scope.$on('currentHawkerSet', function() {
			$scope.currentHawker = HawkerAppDS.currentHawker;
		});

		$scope.open = function(itm) {
			$scope.image = itm.image;
			$scope.showModal = true;
		};

		$scope.close = function() {
			$scope.showModal = false;
		};
		
		$scope.addToOrder = function(hawker, item) {
			if(typeof $scope.currentHawker == "undefined" || $scope.currentHawker == null) {
				HawkerAppDS.setCurrentHawker(hawker);
				HawkerAppDS.addToOrderList(item);
			} else {
				if($scope.currentHawker == hawker) {
					HawkerAppDS.addToOrderList(item);
				} else {
					console.log("cannot mix order from multiple vendors.");
					alert("Sorry! In this version, we do not allow orders from multiple vendors in the same order.");
				}
			}
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
		$scope.$on('currentHawkerSet', function() {
			$scope.currentHawker = HawkerAppDS.currentHawker;
		});

		$scope.$on('pincodeSet', function() {
			$scope.pincode = HawkerAppDS.pincode;
		});

		$scope.removeFromOrder = function(item) {
			HawkerAppDS.removeFromOrderList(item);
		};

		$scope.submitOrder = function(orderData) {
			var postData = {};
			postData['orderData'] = orderData;
			postData['name'] = $scope.customerName;
			postData['email'] = $scope.customerEmail;
			postData['HP'] = $scope.customerHP;
			postData['totalCost'] = $scope.totalCost;
			postData['currentHawker'] = $scope.currentHawker;
			postData['pincode'] = $scope.pincode;
			console.log(postData);

			// send this data to flask`1                    2   
			$http.post('/order/place', postData )
			.success(function() {
				$scope.orderEmptyMessage = "Order Placed";
				$scope.orderData = [];
				$scope.customerHP = '';
				$scope.customerEmail = '';
				$scope.customerName = '';
				$scope.totalCost = 'S$0.00';
				HawkerAppDS.setCurrentHawker(null);
				HawkerAppDS.updateOrderList($scope.orderData);
			})
			.error(function() {
				// handle this.
				console.log("Error occured trying to place the order.")
				alert("Failed to place order");
			});
		};
	}]);

}) ();