app.controller('trackController', ['$scope', 'esClient', function($scope, esClient){
	$scope.docs = []
	// $scope.$parent.$watch('search_params', function(newValue, oldValue){

	// }, true);

	$scope.search_params = {
		//'brand': $scope.$parent.search_params.brand,
		//'category': $scope.$parent.search_params.category,
		// 'brand': 'forever21',
		// 'category': 'f21',
		'brand': 'jcrew',
		'category': 'sale',
		'sub_category': 'sale',
		'current_page': 0,
		'size': 12,				
	}

	$scope.$watch('search_params', function(newValue, oldValue) {
		//console.log(newValue)
		var query_body = {
			"size": newValue.size,
			"from": newValue.current_page * newValue.size,
			"query": {
				"bool":{
					"must":[
						{"match": { "item_name": newValue.searchStr}},
						// {"match": { "sub_category": newValue.sub_category}}
					]
				}
			},
			"sort" : [
				{ "datetime" : {"order" : "desc"}},	
				{ "perct_price_off" : {"order" : "desc"}},	
			]
		}
		console.log(query_body)
		// Query ES
		esClient.search({
		  index: newValue.brand,
		  type: newValue.category,
		  body: query_body
		}).then(function (body) {
		  var docs = body.hits.hits;
		  $scope.docs = [];
		  docs.forEach(function(entry){
		  	item_doc = entry._source;		  	
		  	// Loop through each item get price history
		  	var price_chart_data = [];
		  	var price_qbody = {	
		  		"size": 200,
	  			"query": {
				 	"match" : {'product_id': item_doc.product_id}
				},
				"sort" : [
    				{ "datetime" : {"order" : "desc"}},	
    			]
		  	};
		  	esClient.search({
			  index: newValue.brand,
			  type: 'price',
			  body: price_qbody
			}).then(function (price_resp) {				
				price_lst = price_resp.hits.hits.reverse();					
				price_lst.forEach(function(doc){
					price_chart_data.push({
						x: new Date(doc._source['datetime']),
						y: parseFloat(doc._source['price'])
					})
				})						
				//console.log(price_chart_data)						
			});
			// End price history

		  	//console.log(item_doc);

		  	entry._source.data = [{
		  		values: price_chart_data,
		  		key: 'price',
		  		//color: '#f44336'
		  		color: 'rgb(255,127,14)'
		  	}]
		  	$scope.docs.push(entry._source);
		  });

		}, function (error) {
		  console.trace(error.message);
		});
	}, true);

	// Chart Options
	$scope.sparkoptions = nvd3SparkOptions;
    $scope.lineOptions = nvd3LineOptions;		
	
}]);