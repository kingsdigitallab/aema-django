
// Get all the unique filer types available for this dataset
var burialsCollection = new Array();
var individualsCollection = new Array();
var stelaeCollection = new Array();
var metalworkCollection = new Array();
var inscriptionsCollection = new Array();

var chart;

    function pieChart(){
        chart.transform('pie')        
    }
    
    function barChart(){
        chart.transform('bar')        
    }

function gatherCollectionsAndFilters(recType){
    	// Clear the actual data Collections as well....
        window[recType+'Collection'] = [];
        
	// Clear ALL value arrays if they exist for this recType
	try {
		for (f in window[recType + 'AvailableFilterTypes']){
			window[ recType + window[recType + 'AvailableFilterTypes'][f]+ '_values' ] = undefined;
		}
	}
	catch (e){
		//
	}

    	window[recType + 'AvailableFilterTypes']= []
	for (a in geoJsonResults.features){
		recType = geoJsonResults.features[a].properties.layer;
		window[geoJsonResults.features[a].properties.layer+'Collection'].push(geoJsonResults.features[a].properties.extra_properties)
		for ( k in geoJsonResults.features[a].properties.extra_properties ){
			for (key in geoJsonResults.features[a].properties.extra_properties[k]){
				if (window[recType + 'AvailableFilterTypes'].indexOf(key)==-1){
					window[recType + 'AvailableFilterTypes'].push(key)
				}
			}
		}
	}
	defineValues(recType);
}; //end gatherCollectionsAndFilters

// Then get all values of each category

// Define an array for each...

function defineValues(recType){
	for (f in window[recType + 'AvailableFilterTypes']){
		window[ recType + window[recType + 'AvailableFilterTypes'][f]+ '_values' ] = new Object();
	}
	for (a in geoJsonResults.features){
		for ( k in geoJsonResults.features[a].properties.extra_properties ){
			for (key in geoJsonResults.features[a].properties.extra_properties[k]){
				try {
					if ( geoJsonResults.features[a].properties.extra_properties[k][key].constructor === Array ) {
						for (v in geoJsonResults.features[a].properties.extra_properties[k][key]){
							if ( window[ recType + key + '_values' ][ geoJsonResults.features[a].properties.extra_properties[k][key][v] ] ){
								// It's already there so just increment the count by 1
								window[ recType + key + '_values' ][geoJsonResults.features[a].properties.extra_properties[k][key][v]]+=1
							}
							else {
								// It's not there, so record it
								window[ recType + key + '_values' ][geoJsonResults.features[a].properties.extra_properties[k][key][v]] = 1;
							}
						}
					}
					else {
						if ( window[ recType + key + '_values' ][geoJsonResults.features[a].properties.extra_properties[k][key] ] ){
							window[ recType + key + '_values' ][geoJsonResults.features[a].properties.extra_properties[k][key]] += 1
						}
						else {
							window[ recType + key + '_values' ][geoJsonResults.features[a].properties.extra_properties[k][key]] = 1
						}
					}
				}
					catch (e){
						// Pass
					}
			}
		}
	}
};// end defineFilters

$(document).ready(function(){
	$('.graph').on('click',function(){
		var str = '<div id="graph"><div class="columns large-2">';
		for ( f in window[ $(this).data('record-type') + 'AvailableFilterTypes'] ){
			str += '<input type="button" style="width:178px;" data-filter-name="' + $(this).data('record-type') + window[$(this).data('record-type') + 'AvailableFilterTypes'][f] + '_values' +
			    '" class="button secondary less-padding radius graph-select" value="'+ toTitleCase(
				window[$(this).data('record-type') + 'AvailableFilterTypes'][f].replace(/_/g,' ') )+ '">'
                        /*+'<input data-layer-name="'+ $(this).data('record-type') +'" data-value-list="' + $(this).data('record-type') + window[$(this).data('record-type') + 'AvailableFilterTypes'][f] + '_values' +
                            '" data-filter-name="'+ window[ $(this).data('record-type')+ 'AvailableFilterTypes'][f] +'" class="button secondary less-padding radius category-select" value="Categorise markers"></input></br>'*/
		}
		str += '</div><!--End 1st column-->'
		str += '<div id="graph-area" class="columns large-10"><h3>No graph category selected or no data</h3></div><!-- end 2nd column -->'
		$('#graph-modal').html( str );
        // sort those buttons
        reorderButtons();
        
		$('.category-select').on('click',function(){
			categoriseMarkers($(this).data('layer-name'),
					  $(this).data('filter-name'),
					  window[$(this).data('value-list')])
		})
		$('.graph-select').on('click',function(){
			var cols = []

			var f = window[ $(this).data('filter-name') ]
			for (k in f){
				cols.push([k,f[k]])
			}
			// Sort columns
			
			cols.sort(function(a,b) { 
				var compA = a[1];
				var compB = b[1];
			return (compA < compB) ? 1 : (compA > compB) ? -1 : 0;
			})
			
			chart = c3.generate({
    			bindto: '#graph-area',
    				data: {
      				columns: 
						cols
      				,
      				type:'bar'
    				}
			});
            $('#graph-area').append('<input style="margin-right:10px;"type="button" class="button secondary less-padding radius" value="Pie chart" onclick="pieChart()">' +
            '<input type="button" class="button secondary less-padding radius" value="Bar chart" onclick="barChart()">')
		})
	});
    
 

	
	$('.categorise').on('click',function(){
		var str = '<div class="row columns large-12"><div class="columns large-12">';
		str += '<input type="button" style="background-color:rgb(128,17,10) !important;color:rgb(187,176,166) !important;width:400px !important;margin-right:10px;" value="Uncategorise markers" class="green button secondary less-padding radius category-select" onclick="unCategoriseMarkers(&quot;'+$(this).data('record-type')+'&quot;)">'
		for ( f in window[ $(this).data('record-type') + 'AvailableFilterTypes'] ){
			str += '<input type="button" style="width:400px !important;margin-right:10px;" data-layer-name="'+ $(this).data('record-type') +'" data-value-list="' + $(this).data('record-type') + window[$(this).data('record-type') + 'AvailableFilterTypes'][f] + '_values' +
                            '" data-filter-name="'+ window[ $(this).data('record-type')+ 'AvailableFilterTypes'][f] +'" class="button secondary less-padding radius category-select" value="Categorise markers by '+ toTitleCase(
				window[$(this).data('record-type') + 'AvailableFilterTypes'][f].replace(/_/g,' ') ) + '">'
		}
		str += '</div><!-- end row --></div><!--End 1st column-->'
		//str += '<div id="graph-area" class="columns large-10"><h3>Test</h3></div><!-- end 2nd column -->'
		$('#category-modal').html( str );
		$('.category-select').on('click',function(){
			categoriseMarkers($(this).data('layer-name'),
					  $(this).data('filter-name'),
					  window[$(this).data('value-list')])
		})
	})	
})

function categoryColours(obj){
	var cArr = []
	for ( c in obj ){
		var col = '#'+Math.floor(Math.random()*16777215).toString(16);
		cArr.push(col);
	}
	return cArr
	//categoriseMarkers( cArr)
}

function categoriseMarkers(layer,filter,valueObject){

    var colourArray = categoryColours(valueObject);
    var notCategorised = []
	var valueArray = []

	for (k in valueObject){
		valueArray.push(k)
	}

	getMapKeyByLayer(layer,valueArray,colourArray,filter)

	var layerToStyle = 	window[layer]
	for ( l in layerToStyle._layers ){
		try { // Need a catch here, as not features are categorised properly
                 console.log(filter)
			if ( (layerToStyle._layers[l].feature.properties.extra_properties[0][filter].constructor === Array) && 
				(layerToStyle._layers[l].feature.properties.extra_properties[0][filter].length == 1)	 ){
				//Find indes of value
				var colourIndex = valueArray.indexOf( layerToStyle._layers[l].feature.properties.extra_properties[0][filter][0] )
				// And use to restyle the marker
				layerToStyle._layers[l].setStyle({color:colourArray[colourIndex],fillColor:colourArray[colourIndex],opacity:0.9,fillOpacity:0.7}).setRadius(5)
				console.log('1.' + colourArray[colourIndex])
			}
			// If not an Array, just get the value
                        else if (layerToStyle._layers[l].feature.properties.extra_properties[0][filter].constructor === Array){
				console.log('2. A long array - do nothing')
				// Return marker to original style ...
				//layerToStyle._layers[l].setStyle(markerStyles[layer])
				layerToStyle._layers[l].setStyle({opacity:0,fillOpacity:0,radius:1})
				notCategorised.push(layerToStyle._layers[l])
			}
			else {
				var colourIndex = valueArray.indexOf( layerToStyle._layers[l].feature.properties.extra_properties[0][filter])
				layerToStyle._layers[l].setStyle({color:colourArray[colourIndex],fillColor:colourArray[colourIndex],opacity:0.9,fillOpacity:0.7}).setRadius(5)
				console.log('3. ' + colourIndex + ' - not an Array')
			}
		}
		catch (err){
			notCategorised.push(layerToStyle._layers[l])
			//layerToStyle._layers[l].setStyle(markerStyles[layer])
			layerToStyle._layers[l].setStyle({opacity:0,fillOpacity:0,radius:1})
			console.log('4. Errored')
		}
	}
	alert(notCategorised.length + ' records could not be reliably styled according to this parameter. These records will be hidden');
}


function unCategoriseMarkers(layerStr){
	try{
		mapKey.removeFrom(resultMap)
	}
	catch (err) {
		//
	}	
	var layerToStyle = window[layerStr]
	for (l in layerToStyle._layers){
		layerToStyle._layers[l].setStyle(markerStyles[layerStr])
	}
}


var burialsMapKeyArray;
var indiviudlasMapKeyArray;
var stelaeMapKeyArray;
var metalworkMapKeyArray;
var inscriptionsMapKeyArray;


function getMapKeyByLayer(layer,vals,cols,filter){
	window[layer + 'MapKeyArray'] = new Object; // e.g. burialsMapKeyArray
	for (v in vals){
		window[layer + 'MapKeyArray'][vals[v]] = cols[v] 
	}
	addMapKey(window[layer + 'MapKeyArray'],layer,filter)
}

var mapKey;

function addMapKey( mapKeyObjects,layer,filter ){
	try{
		mapKey.removeFrom(resultMap)
	}
	catch (err) {
		//
	}
	mapKey = undefined;
	var content = []
	content.push({'content': '<strong>' + toTitleCase(layer) + ' by ' + filter.replace(/_/g,' ') + '</strong>' })
	for (v in mapKeyObjects){
		content.push({'content': toTitleCase(v) + ' <svg height="20" width="20"><circle cx="10" cy="10" r="5" fill="' + mapKeyObjects[v] 
			+ '"/></svg>'})
	}
	mapKey = L.functionButtons(content,{position:'bottomright'});
	resultMap.addControl(mapKey);
};


function reorderButtons(){
	
	try {
			var mylist = $('#graph div')[0]
			// Get list items
			var listitems = $($('#graph div input'))
			// Sort items
			listitems.sort(function(a,b){
				var compA = $(a).val().toUpperCase();
				var compB = $(b).val().toUpperCase();
				return (compA < compB) ? -1 : (compA > compB) ? 1 : 0; 
			})	
			// Append sorted list
			$.each(listitems,function(idx,itm) { 
				mylist.appendChild(itm);
			});
		}
	catch (e) {
		//
	}

};   