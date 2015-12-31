( function() {
angular.module("hawkerAppDS", []).factory('HawkerAppDS', function($rootScope) {
	var service = {};
	service.hawkerListMessage = "";
	service.hawkerList = [];
	service.orderList = [];

	service.updateHawkerListMessage = function(message) {
		this.hawkerListMessage = message;
		$rootScope.$broadcast("messageUpdated");
	}

	service.updateHawkerList = function(hList) {
		this.hawkerList = hList;
		$rootScope.$broadcast("hawkerListUpdated");
	}

	service.updateOrderList = function(oList) {
		this.orderList = oList;
		$rootScope.$broadcast("orderListUpdated");
	}

	service.addToOrderList = function(item) {
		this.orderList.push(item);
		$rootScope.$broadcast("orderListUpdated");
	}

	return service;
});
} )();