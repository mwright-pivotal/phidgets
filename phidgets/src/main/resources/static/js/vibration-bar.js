/**
 * 
 */

var data = {
	    labels: ["Vibration"],
	    datasets: [
	        {
	            label: "Value",
	            fillColor: "rgba(220,220,220,0.5)",
	            strokeColor: "rgba(220,220,220,0.8)",
	            highlightFill: "rgba(220,220,220,0.75)",
	            highlightStroke: "rgba(220,220,220,1)",
	            data: [65, 59, 80, 81, 56, 55, 40]
	        }
	    ]
	};

window.onload = function() {
	var ctx = document.getElementById("canvas-vibration").getContext("2d");
	window.myBarVibration = new Chart(ctx).Line(vibrationData, {
		responsive : false,
		scaleIntegersOnly : true,
		scaleOverride : false,

		// ** Required if scaleOverride is true **
		// Number - The number of steps in a hard coded scale
		// scaleSteps: 300,
		// Number - The value jump in the hard coded scale
		//scaleStepWidth: 0.5,
		// Number - The scale starting value
		animationSteps : 3,
		scaleStartValue : 0,
		
		//Boolean - Whether the scale should start at zero, or an order of magnitude down from the lowest value
	    scaleBeginAtZero : true,

	    //Boolean - Whether grid lines are shown across the chart
	    scaleShowGridLines : true,

	    //String - Colour of the grid lines
	    scaleGridLineColor : "rgba(0,0,0,.05)",

	    //Number - Width of the grid lines
	    scaleGridLineWidth : 1,

	    //Boolean - Whether to show horizontal lines (except X axis)
	    scaleShowHorizontalLines: true,

	    //Boolean - Whether to show vertical lines (except Y axis)
	    scaleShowVerticalLines: true,

	    //Boolean - If there is a stroke on each bar
	    barShowStroke : true,

	    //Number - Pixel width of the bar stroke
	    barStrokeWidth : 2,

	    //Number - Spacing between each of the X value sets
	    barValueSpacing : 5,

	    //Number - Spacing between data sets within X values
	    barDatasetSpacing : 1,

	    //String - A legend template
	    legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].fillColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"

	});
	//then you just need to generate the legend
	var legend = window.myBarVibration.generateLegend()
	//and append it to your page somewhere
	document.getElementById("vibrationLegendDiv").innerHTML = legend;
	
	var myBarChart = new Chart(ctx).Bar(vibrationData, options);
}