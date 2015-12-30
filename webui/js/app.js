( function() {
	var app = angular.module("hawkerApp", [ ]);
	app.controller('HawkerAppController', ['$http', function($http) {
		var ctrl = this;
		ctrl.hawkers = [];
		$http.get('js/hawker-data.json').success(function(data) {
			ctrl.hawkers = data.hawkers;
		});
	}]);
	app.controller('PinCodeController', ['$http', function($http) {
		this.refine = function() {
			console.log(this.pinCode);
		};
	}]);

	app.directive('pincodeForm', function() {
		return {
			restrict: 'E',
			templateUrl:'pincodeForm.html'
		};
	});
} )();