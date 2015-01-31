
var nvd3SparkOptions = {
    chart: {
        type: 'sparklinePlus',
        height: 80,
        x: function(d, i){
        	return d.x;
        },
        xTickFormat: function(val) {	                	
            return d3.time.format('%x')(val);
        },
        yTickFormat: function(val) {	                	
            return '$' + val;
        },
        transitionDuration: 250,
        noData: ''
    }
};

var nvd3LineOptions = {	
    chart: {    	
        type: 'lineChart',
        height: 150,
        margin : {
            top: 20,
            right: 20,
            bottom: 40,
            left: 55
        },

        x: function(d){ return d.x; },  
        y: function(d){ return d.y; },
        useInteractiveGuideline: true,              
        xAxis: {
            //axisLabel: 'Date',
            tickFormat: function(d){
                 return  d3.time.format('%x')(new Date(d));
            },
            showMaxMin: false,            
        },
        yAxis: {
            axisLabel: 'Price ($)',
            tickFormat: function(d){
                return d3.format('.02f')(d);
            },
            axisLabelDistance: 30,
            showMaxMin: false,            
        },
        showLegend: false,
        noData: '',
        interpolate:'step-after',  
        lines:{
        	size: function(){ return 0;}
        }      
    }    
};