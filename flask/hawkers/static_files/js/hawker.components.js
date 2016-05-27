( function() {
	var app = angular.module("hawkerAppComponents", [ ]);
	// pincode form
	app.directive('pincodeForm', function() {
		return {
			restrict: 'E',
			templateUrl:'pincode-form.html'
		};
	});

	app.directive('hawkers', function() {
		return {
			restrict: 'E',
			templateUrl: 'hawkers.html'
		};
	});

	app.directive('orders', function() {
		return {
			restrict: 'E',
			templateUrl: 'orders.html'
		};
	});

} ) ();
