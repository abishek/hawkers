( function() {
angular.module("hawkerAppDS", []).factory('HawkerAppDS', function($rootScope) {
	var service = {};
	service.hawkerListMessage = "";
	service.hawkerList = [];
	service.orderList = [];
	service.currentHawker = null;

	service.setCurrentHawker = function(hawker) {
		this.currentHawker = hawker;
		$rootScope.$broadcast("currentHawkerSet");
	}

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

	service.removeFromOrderList = function(item) {
		this.orderList.splice(this.orderList.indexOf(item), 1);
		$rootScope.$broadcast("orderListUpdated");
		if(this.orderList.length == 0) {
			this.currentHawker = null;
			$rootScope.$broadcast("currentHawkerSet");
		}
	}

	return service;
});
} )();