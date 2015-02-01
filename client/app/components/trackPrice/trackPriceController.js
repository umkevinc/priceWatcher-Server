app.controller('trackController', ['$scope', 'esClient', function($scope, esClient){
	$scope.docs = []
	$scope.search_params = {
		'brand': 'forever21',
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
						{"match": { "sub_category": "sale"}}		
					]
				}
			},
			"sort" : [
				{ "datetime" : {"order" : "desc"}},	
			]
		}
		console.log(query_body)
		//Query ES
		esClient.search({
		  index: newValue.brand,
		  type: 'f21',
		  body: query_body
		}).then(function (body) {
		  var docs = body.hits.hits;				  
		  $scope.docs = [];
		  docs.forEach(function(entry){
		  	item_doc = entry._source;

		  	// Loop through each item get price history
		  	var price_chart_data = [];
		  	var price_qbody = {				  		
		  		"size": 30,
	  			"query": {			  				
				 	"term" : { 'product_id': item_doc.product_id}
				}, 						
				"sort" : [
    				{ "datetime" : {"order" : "desc"}},	
    			]
		  	};
		  	esClient.search({
			  index: newValue.brand,
			  type: 'f21',
			  body: price_qbody
			}).then(function (price_resp) {										
				price_lst = price_resp.hits.hits.reverse();					
				price_lst.forEach(function(doc){
					price_chart_data.push({
						x: new Date(doc._source['datetime']),
						y: parseFloat(doc._source['price'])
					})
				})						
				// console.log(price_chart_data)						
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