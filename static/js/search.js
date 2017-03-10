$(document).ready(function() {
	//When loaded, fetch all the pubs
	$.ajax({
		type: 'GET',	
		url: '/taps_oan/getPubs',
		dataType: 'json'
		}).done(function(data){
			console.log(data);
			$.each(data, function (i, item) {
				//Add them to the select option
			    $('#pubGroup').append($('<option>', { 
			        value: "/taps_oan/pub/"+item.fields.slug,
			        text : item.fields.name 
			    }));
			});
				//Fetch all the beers
				$.ajax({
				type: 'GET',	
				url: '/taps_oan/getBeers',
				dataType: 'json'
				}).done(function(data){
					console.log(data);
					$.each(data, function (i, item) {
						//Add them to the select option
					    $('#beerGroup').append($('<option>', { 
					        value: "/taps_oan/beer/"+item.fields.slug,
					        text : item.fields.name 
					    }));
					});
					//Apply library to sort the search
					$("#main_search").chosen({no_results_text: "Oops, nothing found!"}).change(search_trigger);; 
				})
		})
})		

//Handle selection in the search
var search_trigger = function(){
	var link = $('#main_search').find(":selected").val();
	window.location = link;
}