$.ajaxSetup({'cache':true});


var fakeObject = {
    "type": "Feature",
    "properties": {
    },
    "geometry": {
        "type": "Point",
        "coordinates": [-180,-90]
    }
};
//Map cache
var language;
var burials;
var hoards;
var metalwork;
var stelae;
var miscellaneous;
var ogam;
var inscriptions;
var individuals;
var pots;
var gravegoods;
var settlements;
var toponyms;
// Declare arrays to hold facet objects
//var facet_families = ['burials','hoards','stelae','ogam'];	
var facet_families = ['burials','pots','metalwork','stelae','inscriptions','gravegoods','individuals','toponyms','settlements','miscellaneous'];	
var selectedFacets = new Array();
var excludedFacets = new Array();
var selectedOrFacets = new Array();
var lastFacetedObjectType;
var selectedOrURL = '';
var selectedURL = '';
var excludedURL = '';
//var	datequeryURL = '';
var querytypeURL = '';
var geomQueryURL = '';
var burialsQuery = ''
var miscellaneousQuery = '';
var metalworkQuery = ''
var stelaeQuery = ''
var ogamQuery = ''
var gravegoodsQuery = ''
var inscriptionsQuery = ''
var individualsQuery = ''
var potsQuery = ''
var toponymsQuery = ''
var settlementsQuery = ''
var textQuery = ''
var geomQuery = ''
var geoJsonResults;
var uniqueTextSearchType = false;
  var chrono = ['Neolithic ','Neolithic-Beaker ','Neolithic-Early Bronze Age ','Neolithic-Middle Bronze Age ','Neolithic-Late Bronze Age ','Early Neolithic ','Late Neolithic ','Late Neolithic-Beaker ','Late Neolithic-Early Bronze Age ','Late Neolithic to Middle Bronze Age ','Beaker ','Beaker-Early Bronze Age ','Beaker-Middle Bronze Age ','Beaker-Late Bronze Age ','Early Bronze Age ','Early-Middle Bronze Age ','Middle Bronze Age ','Middle-Late Bronze Age ','Middle Bronze Age-Iron Age ','Late Bronze Age ','Late Bronze Age-Early Iron Age ','Bronze Age ','Bronze Age-Iron Age ','Early Iron Age ','Early-Middle Iron Age ','Middle Iron Age ','Middle-Late Iron Age ','Late Iron Age ','Iron Age ','Medieval '];
markerCategoryColours = ['rgb(166,206,227)','rgb(31,120,180)','rgb(178,223,138)','rgb(51,160,44)','rgb(251,154,153)','rgb(227,26,28)','rgb(253,191,111)',
						 'rgb(255,127,0)','rgb(202,178,214)','rgb(106,61,154)','rgb(255,255,153)','rgb(177,89,40)']
var markerStyles = {
					'inscriptions':{color:'#b16211',opacity:0.8,fillColor:'#b16211',fillOpacity:0.6,radius:5},
	                'individuals':{color:'#800080',opacity:0.9,fillColor:'purple',fillOpacity:0.6,radius:5},
					'burials':{opacity:0.8,fillOpacity:0.6,fillColor:'blue',color:'blue',radius:5},
					'stelae': {color:'#4d9e4d',opacity:0.8,fillColor:'#4d9e4d',fillOpacity:0.6,radius:5},
					'metalwork': {color:'#955A6F',opacity:0.8,fillColor:'#955A6F',fillOpacity:0.6,radius:5},
                    'toponyms': {color:'#cccc33',opacity:0.9,fillColor:'#cccc33',fillOpacity:0.6,radius:5},
					'settlements': {color:'#6666dd',opacity:0.8,fillColor:'#6666dd',fillOpacity:0.6,radius:5},
					'pots': {color:'#336666',opacity:0.8,fillColor:'#336666',fillOpacity:0.6,radius:5},
                    'gravegoods': {color:'#0099cc',opacity:0.8,fillColor:'#0099cc',fillOpacity:0.6,radius:5},                    
                    'miscellaneous': {color:'#4D0003',opacity:0.8,fillColor:'#4D0003',fillOpacity:0.6,radius:5},                    
}

var neil;
var cnvs;
var dtx;
// VERY specific sort for chronologies...
function getGeom(layer){
	var str = 'POLYGON(('
	for (p in layer.getLatLngs() ){
		str += ( layer.getLatLngs()[p].lng + ' ' + layer.getLatLngs()[p].lat + ',')
	}
	str += (layer.getLatLngs()[0].lng + ' ' + layer.getLatLngs()[0].lat )
	return str + '))'
};
function sortByChronology(){
  var myList = $('h4:contains("general chronology")').next('div').children('ul')
  var listItems = myList.children('li').get();
  listItems.sort(function(a,b){
    var compA = $.inArray($(a).find('label').text(), chrono);
    var compB = $.inArray($(b).find('label').text(), chrono);
    return (compA < compB) ? -1 : (compA > compB) ? 1 : 0;
  });
  $(myList).append(listItems);
  
  var myList = $('#facet-individuals').find('h4:contains("chronology")').next('div').children('ul')
  var listItems = myList.children('li').get();
  listItems.sort(function(a,b){
    var compA = $.inArray($(a).find('label').text(), chrono);
    var compB = $.inArray($(b).find('label').text(), chrono);
    return (compA < compB) ? -1 : (compA > compB) ? 1 : 0;
  });
  $(myList).append(listItems);  
  
  var myList = $('#facet-settlements').find('h4:contains("period]")').next('div').children('ul')
  var listItems = myList.children('li').get();
  listItems.sort(function(a,b){
    var compA = $.inArray($(a).find('label').text(), chrono);
    var compB = $.inArray($(b).find('label').text(), chrono);
    return (compA < compB) ? -1 : (compA > compB) ? 1 : 0;
  });
  $(myList).append(listItems); 
  
}

// Refine results
function updateFacetedResults(){
    // Force an unspiderfy on the cluster layer
	try {
		var lyrToUnspiderfy = window[lastFacetedObjectType+ '_markers'];
		lyrToUnspiderfy._unspiderfy();	
	}
	catch (e) {
		// Probably nothing to do then
	}
	// Assemble url for selected facets	
    querytypeURL = '&query_type=' + lastFacetedObjectType;
        if (geomQuery != ''){
                geomQueryURL =  '&polygon=' + geomQuery;
        }
        else {
                geomQueryURL = '';
        }

    selectedURL = '';
    for (sf in selectedFacets){
	    // Only compile facets that are the correct family
		if (selectedFacets[sf].type.indexOf(lastFacetedObjectType)!=-1 ) {
			//selectedURL += '&selected_filters=' + selectedFacets[sf].type + ':'+ selectedFacets[sf].value.replace(/[\/(),><-]/g,' ')
            //selectedURL += '&selected_filters=' + selectedFacets[sf].type + ':'+ selectedFacets[sf].value.replace(/[\/(),><]/g,' ')
            selectedURL += '&selected_filters=' + selectedFacets[sf].type + ':'+ selectedFacets[sf].value.replace(/[\/()><]/g,' ')
		}
	}
	
	selectedURL = geomQueryURL + selectedURL;
	
    selectedOrURL = '';
    for (sof in selectedOrFacets){
            // Only compile facets that are the correct family
                if (selectedOrFacets[sof].type.indexOf(lastFacetedObjectType)!=-1 ) {
                        //selectedOrURL +=  '&selected_facets=' + selectedOrFacets[sof].type + ':'+ selectedOrFacets[sof].value.replace(/[\/(),><-]/g,' ')
                        //selectedOrURL +=  '&selected_facets=' + selectedOrFacets[sof].type + ':'+ selectedOrFacets[sof].value.replace(/[\/(),><]/g,' ')
                        selectedOrURL +=  '&selected_facets=' + selectedOrFacets[sof].type + ':'+ selectedOrFacets[sof].value.replace(/[\/()><]/g,' ')                        
                }
        }
		
	selectedOrURL = geomQueryURL + selectedOrURL;		
		
    excludedURL = '';
    for (ef in excludedFacets){
	    // Only compile facets that are the correct family	
		if (excludedFacets[ef].type.indexOf(lastFacetedObjectType)!=-1 ) {
			//excludedURL += '&deselected_filters=' + excludedFacets[ef].type + ':'+ excludedFacets[ef].value.replace(/[\/(),><-]/g,' ')
            excludedURL += '&deselected_filters=' + excludedFacets[ef].type + ':'+ excludedFacets[ef].value.replace(/[\/(),><]/g,' ')
		}
	}
	
	excludedURL = geomQueryURL + excludedURL;			

	// Store the query for pagination purposes:
    window[lastFacetedObjectType + 'Query'] = selectedURL + selectedOrURL + excludedURL;

	// Get that stuff 
	// Results
	$.ajax('/search/refine/?' + selectedURL + selectedOrURL + excludedURL + /*datequeryURL +*/ querytypeURL ,{
        cache:true,
		success:function(data){
			$('#'+lastFacetedObjectType+'-results > div').html(data);  // List that stuff below the map in a nice table
			//var str = ""
			// Add filters to the result list...
				$('#'+lastFacetedObjectType+'-results ul.filters').remove()
				var selectLength = selectedURL.split("&selected_filters=").length;
				var andStr = '<ul class="filters inline-list">'

				for (f in selectedURL.split("&selected_filters=") ){
					var currFacet = selectedURL.split("&selected_filters=")[f];
					if ( currFacet.indexOf(":")!=-1 ){
						var type = currFacet.split(":")[0]
						var subType = type.split(lastFacetedObjectType)[1]
						var facet_value = currFacet.split(":")[1]
						andStr +=  '<li>'+ 
							toTitleCase( subType.replace(/_/g,' ') ) + ': <a href="#" class="green button radius less-padding"><i class="fa fa-check-circle"></i> '+ 
							facet_value+'</a>'
						if (f<selectLength-1 && f!= 0){
                            if (language=="es"){
                                andStr += '&nbsp;y&nbsp;'                                
                            }
                            else {
                                andStr += '&nbsp;and&nbsp;'
                            }
						}
						str += '</li>'						
					}
				}
				andStr += '</ul>'

				var orStr = '<ul class="filters inline-list">'

				var selectOrLength = selectedOrURL.split("&selected_facets=").length;

				for (f in selectedOrURL.split("&selected_facets=") ){
					var currFacet = selectedOrURL.split("&selected_facets=")[f];
					if ( currFacet.indexOf(":")!=-1 ){
						var type = currFacet.split(":")[0]
						var subType = type.split(lastFacetedObjectType)[1]
						var facet_value = currFacet.split(":")[1]
						orStr +=  '<li>'+ 
							toTitleCase( subType.replace(/_/g,' ') ) + ': <a href="#" class="yellow button radius less-padding"><i class="fa fa-plus-circle"></i> '+ 
							facet_value+'</a>'
						
						if (f<selectOrLength-1 && f!= 0){
                            if (language=='es'){
                                orStr += '&nbsp;o&nbsp;'
                            }
                            else {
                                orStr += '&nbsp;OR&nbsp;'                                
                            }
						}
						str += '</li>'						
					}
				}
				orStr += '</ul>'

				if (selectOrLength==0){
					orStr = ''
				}

				var notStr = '<ul class="filters inline-list">'

				var excludeLength = excludedURL.split("&deselected_filters=").length;


				for (f in excludedURL.split("&deselected_filters=") ){
					var currFacet = excludedURL.split("&deselected_filters=")[f];
					if ( currFacet.indexOf(":")!=-1 ){
						var type = currFacet.split(":")[0]
						var subType = type.split(lastFacetedObjectType)[1]
						var facet_value = currFacet.split(":")[1]
                            if (language=='es'){
                                notStr +=  '<li>'+ 
                                toTitleCase( subType.replace(/_/g,' ') ) + ' no es: <a href="#" class="red button radius less-padding"><i class="fa fa-times-circle"></i> '+ 
                                facet_value+'</a>'
                            }
                            else {
                                notStr +=  '<li>'+                                 
                                toTitleCase( subType.replace(/_/g,' ') ) + ' not: <a href="#" class="red button radius less-padding"><i class="fa fa-times-circle"></i> '+ 
                                facet_value+'</a>'                                
                                
                            }
						
						if (f<excludeLength-1 && f!= 0){
                            if (language=='es'){                            
                                notStr += '&nbsp;y&nbsp;'
                            }
                            else 
                                notStr += '&nbsp;and&nbsp;'                                
						}
						str += '</li>'						
					}
				}
				notStr += '</ul>'

				if (excludeLength==0){
					notStr = ''
				}

				var str = andStr + orStr + notStr;

				$('#'+lastFacetedObjectType+'-results > div').before(str);
                
                if (language=="es"){
                // Change the surrounding static text
                    changeTextLanguage('li',spanishHeader4Dict, $('#'+ lastFacetedObjectType +'-header') )
                // Change the facet labels
                    changeTextLanguage('li',spanishLabelDict, $('#'+ lastFacetedObjectType +'-header') )
                    changeInputValueLanguage(spanishInputDict)
                };
		},
		dataType:'text'
	});

	// Map
	$.ajax('/search/map/?&mime_type=application/json' + selectedURL + selectedOrURL + excludedURL + /* datequeryURL + */ querytypeURL ,{
		beforeSend: function(){
			$('.spinner').addClass('active').removeClass('inactive');
			$('.columns.large-3').addClass('waiting');
		},
		dataType:'jsonp',
        jsonpCallback: 'parseMapResults',
        cache:true,
        //jsonp: 'callback',
		async:true
	});

	reorderLists();
	
	// Event for cluster toggle
	$('.layer-toggle').on('change',function(){
		if ( $(this).attr('checked') ){
			unclusterLayer( $(this).attr('data-layer') );
			//$('.switch-button').toggleClass('green red');
			//$(this).parent().toggleClass('green red');
			$(this).parent().removeClass('green').addClass('red');
			//$('label.i-am-label').text('Off');
			$(this).next().text('Off');
		}
		else {
			reclusterLayer( $(this).attr('data-layer') );
			//$('label.i-am-label').text('On');
			$(this).next().text('On');
			//$('.switch-button').toggleClass('red green');
			//$(this).parent().toggleClass('red green');
			$(this).parent().removeClass('red').addClass('green');					
		}
	});			
};

function parseMapResults(data){
	try{
		mapKey.removeFrom(resultMap)
	}
	catch (err) {
		//
	}

    var layer;
    var marker_layer;
    var layersToUpdate = new Array()
    geoJsonResults = data;
    
    for (r in geoJsonResults.features){
        layer = window[geoJsonResults.features[r].properties.layer];
		marker_layer = window[geoJsonResults.features[r].properties.layer + '_markers'];
            // Clear the layer if it is due to be updated. Only needs to be done once...
            if (layersToUpdate.indexOf(layer)==-1){
				layersToUpdate.push(layer);
				//marker_layer.removeLayer(layer);
				// Changinging this as not clearing properly ??/
				marker_layer.clearLayers();				
                clearLayer(layer);
            };
        layer.addData(geoJsonResults.features[r]);
    };
	// If there were no results of this type, then clear the map layer
    try {
		if (layersToUpdate.indexOf(window[lastFacetedObjectType])==-1)
		{
			var bl = window[lastFacetedObjectType];
			var ml = window[lastFacetedObjectType + '_markers'];
			ml.removeLayer(bl);			
			clearLayer(bl);		
		}
   
		if (marker_layer){
			marker_layer.addLayer(layer);
		}
		else {
			marker_layer = window[lastFacetedObjectType + '_markers'];
			marker_layer.removeLayer(window[lastFacetedObjectType]); 		
		}
	}
	catch (e) {
		// Probably blank 
	}
	//resultMap.spin(false);
	$('.spinner').addClass('inactive').removeClass('active');
	$('.columns.large-3').removeClass('waiting');

	// Set the stringified json in id="[ type ]-json"
    $('#' + lastFacetedObjectType + '-json').val( JSON.stringify( window[lastFacetedObjectType].toGeoJSON()   ) );

    // NEW - Create analysis objects...

    gatherCollectionsAndFilters(lastFacetedObjectType);
};

function clearLayer(layerName){
    for (l in layerName._layers) 
        { layerName.removeLayer(layerName._layers[l])
        }
    // AND NEW - Clear analysis objects...
    gatherCollectionsAndFilters(lastFacetedObjectType);
};

function clearFacets( layertoclear ){
	// Get rid of any map key left on the map
	try{
		mapKey.removeFrom(resultMap)
	}
	catch (err) {
		//
	}	
	
	var toggleClusterElement = $('#facet-' + layertoclear);
	
	lastFacetedObjectType = layertoclear;
	selectedFacets = new Array();
	excludedFacets = new Array();
    selectedOrFacets = new Array();	
	// Clear all maps layers
	
	window[layertoclear+'_markers'].clearLayers()
	window[layertoclear].clearLayers()
	
	$('.facet-select[object-type="'+ lastFacetedObjectType+'"]').each(function(){$(this).attr('checked',false)});
    $('.facet-or-select[object-type="'+ lastFacetedObjectType+'"]').each(function(){$(this).attr('checked',false)});
    $('.facet-exclude[object-type="'+ lastFacetedObjectType+'"]').each(function(){$(this).attr('checked',false)});
	
	// Need to make this specific to the layer being edited....
		//$('.switch-button input').attr('disabled', true);
		//$('.switch-button').addClass('gray');
		$(toggleClusterElement).find('.switch-button input').attr('disabled', true);
		$(toggleClusterElement).find('.switch-button').addClass('gray');		

	//$(".facet-select").each(function(){$(this).attr('checked',false)});
	
	//resultMap.spin(true);
	$('.spinner').addClass('active').removeClass('inactive')
	$('.columns.large-3').addClass('waiting');

    // AND NEW - Clear analysis objects...
    gatherCollectionsAndFilters(lastFacetedObjectType);

	updateFacetedResults()
};

$(document).ready(function() {
	// Initialise a map
    resultMap = L.map('map',{scrollWheelZoom:false,minZoom:4,maxZoom:17,
  	//fullscreenControl: true
    }).setView([50,5], 4);

    var southWest = L.latLng(22, -38);
    var northEast = L.latLng(68,48);
    bounds = L.latLngBounds(southWest, northEast);
	
    graticules = L.graticule({style:{color:'rgb(0,0,255)',weight:0.5,opacity:0.45},interval:5 }).addTo(resultMap)

    labelGraticules();

    ancient_world = new L.TileLayer("http://{s}.tiles.mapbox.com/v3/isawnyu.map-knmctlkh/{z}/{x}/{y}.png",
	{attribution:'Map base by <a href="http://awmc.unc.edu/">AWMC</a>'}).addTo(resultMap);

	legacy_terrain = new L.TileLayer("/geoserver/gwc/service/tms/1.0.0/Project_data%3Adcow_backdrop_aema@EPSG%3A900913@jpeg/{z}/{x}/{y}.jpeg",
	{tms:true})//.addTo(resultMap);

	plain_map = new L.TileLayer("/geoserver/gwc/service/tms/1.0.0/world_simple@EPSG%3A900913@png/{z}/{x}/{y}.png",
	{tms:true})//.addTo(resultMap);
    
    landscape = new L.TileLayer('http://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png',{subdomains:['a','b','c'],attribution:'Map base by <a href="http://www.thunderforest.com/">Thunderforest</a>'});
    
	ba_roads = new L.TileLayer("/geoserver/gwc/service/tms/1.0.0/aema_wms:ba_roads@EPSG%3A900913@png/{z}/{x}/{y}.png",
	{tms:true,transparent:true})//.addTo(resultMap);    
	
	miniBase = new L.TileLayer('http://{s}.acetate.geoiq.com/tiles/acetate-base/{z}/{x}/{y}.png',{subdomains:['a1','a2','a3','a4'],maxzoom:5})
	
    var esri_streets = new L.TileLayer("http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}").addTo(resultMap);
		
	resultMap.on('zoomstart', function(e){
	    $('.spinner').addClass('active').removeClass('inactive')
	});
	
	resultMap.on('dragstart',function(){
		        $('.spinner').addClass('active').removeClass('inactive')
	});
	
	resultMap.on('dragend',function(e){
		    graticules.clearLayers();
			graticules.addData(graticules._getGraticule());
			labelGraticules();
			$('.spinner').addClass('inactive').removeClass('active')
	});

    resultMap.on('zoomend',function(e){
		if (e.target._zoom < 7 ) {
			graticules.clearLayers();
			graticules.options.interval = 4;
			graticules.addData(graticules._getGraticule());
			labelGraticules();
		}
		else if (e.target._zoom < 12 ) {
			graticules.clearLayers();
			graticules.options.interval = 1;
			graticules.addData(graticules._getGraticule());			
			labelGraticules();
		}
		else {
			graticules.clearLayers();
			graticules.options.interval = 1;
			graticules.addData(graticules._getGraticule());
			labelGraticules();			
		}

		$('.spinner').addClass('inactive').removeClass('active')
	})
			
    burials_markers = new L.MarkerClusterGroup({
    	spiderfyDistanceMultiplier: 3,
    	iconCreateFunction : function(cluster) {
    	    var className;
    	    switch ( true ){
				case (cluster.getChildCount()<11):
  				className = 'burials-small-cluster'
  				break;
				case (cluster.getChildCount()<101):
  				className = 'burials-medium-cluster'
  				break;
				default:
 				className = 'burials-large-cluster'
			};
    		return L.divIcon({
    			html:'<span class="cluster-count">' + cluster.getChildCount() +'</span>',
    			className: className,
    			iconSize: L.point(40,40)
    		})
    	},
    }).addTo(resultMap);
    
    miscellaneous_markers = new L.MarkerClusterGroup({
    	spiderfyDistanceMultiplier: 3,
    	iconCreateFunction : function(cluster) {
    	    var className;
    	    switch ( true ){
				case (cluster.getChildCount()<11):
  				className = 'miscellaneous-small-cluster'
  				break;
				case (cluster.getChildCount()<101):
  				className = 'miscellaneous-medium-cluster'
  				break;
				default:
 				className = 'miscellaneous-large-cluster'
			};
    		return L.divIcon({
    			html:'<span class="cluster-count">' + cluster.getChildCount() +'</span>',
    			className: className,
    			iconSize: L.point(40,40)
    		})
    	},
    }).addTo(resultMap);    

    pots_markers = new L.MarkerClusterGroup({
    	spiderfyDistanceMultiplier: 3,
    	iconCreateFunction : function(cluster) {
    	    var className;
    	    switch ( true ){
				case (cluster.getChildCount()<11):
  				className = 'pots-small-cluster'
  				break;
				case (cluster.getChildCount()<101):
  				className = 'pots-medium-cluster'
  				break;
				default:
 				className = 'pots-large-cluster'
			};
    		return L.divIcon({
    			html:'<span class="cluster-count">' + cluster.getChildCount() +'</span>',
    			className: className,
    			iconSize: L.point(40,40)
    		})
    	},
    }).addTo(resultMap);

        gravegoods_markers = new L.MarkerClusterGroup({
        spiderfyDistanceMultiplier: 3,
        iconCreateFunction : function(cluster) {
            var className;
            switch ( true ){
                                case (cluster.getChildCount()<11):
                                className = 'gravegoods-small-cluster'
                                break;
                                case (cluster.getChildCount()<101):
                                className = 'gravegoods-medium-cluster'
                                break;
                                default:
                                className = 'gravegoods-large-cluster'
                        };
                return L.divIcon({
                        html:'<span class="cluster-count">' + cluster.getChildCount() +'</span>',
                        className: className,
                        iconSize: L.point(40,40)
                })
        },
    }).addTo(resultMap);


    toponyms_markers = new L.MarkerClusterGroup({
        spiderfyDistanceMultiplier: 3,
        iconCreateFunction : function(cluster) {
            var className;
            switch ( true ){
                                case (cluster.getChildCount()<11):
                                className = 'toponyms-small-cluster'
                                break;
                                case (cluster.getChildCount()<101):
                                className = 'toponyms-medium-cluster'
                                break;
                                default:
                                className = 'toponyms-large-cluster'
                        };
                return L.divIcon({
                        html:'<span class="cluster-count">' + cluster.getChildCount() +'</span>',
                        className: className,
                        iconSize: L.point(40,40)
                })
        },
    }).addTo(resultMap);

    settlements_markers = new L.MarkerClusterGroup({
        spiderfyDistanceMultiplier: 3,
        iconCreateFunction : function(cluster) {
            var className;
            switch ( true ){
                                case (cluster.getChildCount()<11):
                                className = 'settlements-small-cluster'
                                break;
                                case (cluster.getChildCount()<101): 
                                className = 'settlements-medium-cluster'
                                break;
                                default:
                                className = 'settlements-large-cluster'
                        };
                return L.divIcon({
                        html:'<span class="cluster-count">' + cluster.getChildCount() +'</span>',
                        className: className,
                        iconSize: L.point(40,40)
                })
        },
    }).addTo(resultMap);

    metalwork_markers = new L.MarkerClusterGroup({
    	spiderfyDistanceMultiplier: 3,
    	iconCreateFunction : function(cluster) {
    	    var className;
    	    switch ( true ){
				case (cluster.getChildCount()<11):
  				className = 'metalwork-small-cluster'
  				break;
				case (cluster.getChildCount()<101):
  				className = 'metalwork-medium-cluster'
  				break;
				default:
 				className = 'metalwork-large-cluster'
			};
    		return L.divIcon({
    			html:'<span class="cluster-count">' + cluster.getChildCount() +'</span>',
    			className: className,
    			iconSize: L.point(40,40)
    		})
    	}
    }).addTo(resultMap);

    stelae_markers = new L.MarkerClusterGroup({
    	spiderfyDistanceMultiplier: 3,
    	iconCreateFunction : function(cluster) {
    	    var className;
    	    switch ( true ){
				case (cluster.getChildCount()<11):
  				className = 'stelae-small-cluster'
  				break;
				case (cluster.getChildCount()<101):
  				className = 'stelae-medium-cluster'
  				break;
				default:
 				className = 'stelae-large-cluster'
			};
    		return L.divIcon({
    			html:'<span class="cluster-count">' + cluster.getChildCount() +'</span>',
    			className: className,
    			iconSize: L.point(40,40)
    		})
    	}
    }).addTo(resultMap);	
    
    inscriptions_markers = new L.MarkerClusterGroup({
    	spiderfyDistanceMultiplier: 3,
    	iconCreateFunction : function(cluster) {
    	    var className;
    	    switch ( true ){
				case (cluster.getChildCount()<11):
  				className = 'inscriptions-small-cluster'
  				break;
				case (cluster.getChildCount()<101):
  				className = 'inscriptions-medium-cluster'
  				break;
				default:
 				className = 'inscriptions-large-cluster'
			};
    		return L.divIcon({
    			html:'<span class="cluster-count">' + cluster.getChildCount() +'</span>',
    			className: className,
    			iconSize: L.point(40,40)
    		})
    	}
    }).addTo(resultMap);	

    individuals_markers = new L.MarkerClusterGroup({
        spiderfyDistanceMultiplier: 3,
        iconCreateFunction : function(cluster) {
            var className;
            switch ( true ){
                                case (cluster.getChildCount()<11):
                                className = 'individuals-small-cluster'
                                break;
                                case (cluster.getChildCount()<101):
                                className = 'individuals-medium-cluster'
                                break;
                                default:
                                className = 'individuals-large-cluster'
                        };
                return L.divIcon({
                        html:'<span class="cluster-count">' + cluster.getChildCount() +'</span>',
                        className: className,
                        iconSize: L.point(40,40)
                })
        }
    }).addTo(resultMap);

    burials = new L.geoJson(fakeObject,{pointToLayer: function (feature, latlng) 
			{ 
			/*	
			var marker = L.marker(latlng,{icon:burialIcon});
			*/
			var marker = L.circleMarker(latlng,{opacity:0.9,fillOpacity:0.9}).setRadius(5) // Basic blue marker
			//marker.bindPopup(feature.properties.popupContent);
			//marker.on('click',function(){
			marker.on('mouseintent',function(){
                var m = this
				$.ajax('/view/get-burial-popup/' + feature.properties.id ,{
                    			cache:true,
					async:false,
					success: function(data){
						m.bindPopup(data);

					}
				})
				m.openPopup()
			})
			return marker;
			}			
	}		
	)//.addTo(resultMap);
    
    miscellaneous = new L.geoJson(fakeObject,{pointToLayer: function (feature, latlng) 
			{ 
			/*	
			var marker = L.marker(latlng,{icon:burialIcon});
			*/
			var marker = L.circleMarker(latlng,markerStyles['miscellaneous']).setRadius(5) // Basic blue marker
			//marker.bindPopup(feature.properties.popupContent);
			//marker.on('click',function(){
			marker.on('mouseintent',function(){
                var m = this
				$.ajax('/view/get-miscellaneous-popup/' + feature.properties.id ,{
					async:false,
					success: function(data){
						m.bindPopup(data);

					}
				})
				m.openPopup()
			})
			return marker;
			}			
	}		
	)//.addTo(resultMap);    
    
    gravegoods = new L.geoJson(fakeObject,{pointToLayer: function (feature, latlng)
                        { 
                        /*  
                        var marker = L.marker(latlng,{icon:burialIcon});
                        */
                        //var marker = L.circleMarker(latlng,{opacity:0.9,fillOpacity:0.9}).setRadius(5) // Basic blue marker
                        var marker = L.circleMarker(latlng,markerStyles['gravegoods']).setRadius(5) 
                        //marker.bindPopup(feature.properties.popupContent);
                        //marker.on('click',function(){
                        marker.on('mouseintent',function(){

                var m = this
			
                                $.ajax('/view/get-gravegoods-popup/' + feature.properties.id ,{
                                        async:false,
                                        success: function(data){
                                                m.bindPopup(data);

                                        }
                                })
                                m.openPopup()
			
                        })
			
                        return marker;
                        }
        })//.addTo(resultMap);

    pots = new L.geoJson(fakeObject,{pointToLayer: function (feature, latlng) 
			{ 
			/*	
			var marker = L.marker(latlng,{icon:burialIcon});
			*/
			//var marker = L.circleMarker(latlng,{opacity:0.9,fillOpacity:0.9}).setRadius(5) // Basic blue marker
            var marker = L.circleMarker(latlng,markerStyles['pots']).setRadius(5)             
			//marker.bindPopup(feature.properties.popupContent);
			//marker.on('click',function(){
			marker.on('mouseintent',function(){

                var m = this
                
				$.ajax('/view/get-pots-popup/' + feature.properties.id ,{
					async:false,
					success: function(data){
						m.bindPopup(data);

					}
				})
				m.openPopup()
			})
			return marker;
			}			
	}		
	)//.addTo(resultMap);    
	
    hoards = new L.geoJson(fakeObject,{pointToLayer: function (feature, latlng) 
			{ 
			/*
			var marker = L.marker(latlng,{icon:hoardIcon});
			*/
			var marker = L.circleMarker(latlng,{color:'#955A6F',opacity:0.9,fillColor:'#955A6F',fillOpacity:0.6}).setRadius(5)			
			//marker.bindPopup(feature.properties.popupContent);
			marker.on('mouseintent',function(){
                                var m = this
				$.ajax('/view/get-burial-popup/' + feature.properties.id ,{
					async:false,
					success: function(data){
						m.bindPopup(data);

					}
				})
				m.openPopup()
			})			
			return marker;
			}		
	}		
	
	)//.addTo(resultMap);
	
    metalwork = new L.geoJson(fakeObject,{pointToLayer: function (feature, latlng) 
			{ 
			/*
			var marker = L.marker(latlng,{icon:hoardIcon});
			*/
			var marker = L.circleMarker(latlng,{color:'#955A6F',opacity:0.9,fillColor:'#955A6F',fillOpacity:0.6}).setRadius(5)			
			//marker.bindPopup(feature.properties.popupContent);
			marker.on('mouseintent',function(){
                                var m = this
				$.ajax('/view/get-metalwork-popup/' + feature.properties.id ,{
					async:false,
					success: function(data){
						m.bindPopup(data);

					}
				})
				m.openPopup()
			})			
			return marker;
			}		
	})//.addTo(resultMap);

    toponyms = new L.geoJson(fakeObject,{pointToLayer: function (feature, latlng)
                        {
                        var marker = L.circleMarker(latlng,{color:'#cccc33',opacity:0.9,fillColor:'#cccc33',fillOpacity:0.6}).setRadius(5)
                        marker.on('mouseintent',function(){
                                var m = this
                                $.ajax('/view/get-toponyms-popup/' + feature.properties.id ,{
                                        async:false,
                                        success: function(data){
                                                m.bindPopup(data);
                                        }
                                })
                                m.openPopup()
                        })
                        return marker;
                        }
        })//.addTo(resultMap);

    settlements = new L.geoJson(fakeObject,{pointToLayer: function (feature, latlng)
                        {
                        /*
                        var marker = L.marker(latlng,{icon:hoardIcon});
                        */
                        var marker = L.circleMarker(latlng,{color:'#6666dd',opacity:0.9,fillColor:'#6666dd',fillOpacity:0.6}).setRadius(5)
                        //marker.bindPopup(feature.properties.popupContent);
                        marker.on('mouseintent',function(){
                                var m = this
                                $.ajax('/view/get-settlements-popup/' + feature.properties.id ,{
                                        async:false,
                                        success: function(data){
                                                m.bindPopup(data);
                                        }
                                })
                                m.openPopup()
                        })   
                        return marker;
                        }
        })//.addTo(resultMap);

	stelae = new L.geoJson(fakeObject,{pointToLayer: function (feature, latlng) 
			{ 
			/*
			var marker = L.marker(latlng,{icon:stelaeIcon});
			*/
			//alert(feature.properties.id)
			var marker = L.circleMarker(latlng,{color:'#4d9e4d',opacity:0.9,fillColor:'#4d9e4d',fillOpacity:0.6}).setRadius(5)
			//marker.bindPopup(feature.properties.popupContent);
			marker.on('mouseintent',function(){
                                var m = this
				$.ajax('/view/get-stelae-popup/' + feature.properties.id ,{
					async:false,
					success: function(data){
						m.bindPopup(data);
					}
				})
				m.openPopup()
			})			

			return marker;
			}			
	})
	
	inscriptions = new L.geoJson(fakeObject,{pointToLayer: function (feature, latlng) 
			{ 
			var marker = L.circleMarker(latlng,{color:'#b16211',opacity:0.9,fillColor:'#b16211',fillOpacity:0.6}).setRadius(5)			
			//marker.bindPopup(feature.properties.popupContent);
			marker.on('mouseintent',function(){
                                var m = this
				$.ajax('/view/get-inscriptions-popup/' + feature.properties.id ,{
					async:false,
					success: function(data){
						m.bindPopup(data);
					}
				})
				m.openPopup()
			})		
			return marker;
			}			
		})

    individuals = new L.geoJson(fakeObject,{pointToLayer: function (feature, latlng)
                        {
                        var marker = L.circleMarker(latlng,{color:'purple',opacity:0.9,fillColor:'purple',fillOpacity:0.6}).setRadius(5)                
                        //marker.bindPopup(feature.properties.popupContent);
                        marker.on('mouseintent',function(){
                                var m = this
                                $.ajax('/view/get-individuals-popup/' + feature.properties.id ,{
                                        async:false,
                                        success: function(data){
                                                m.bindPopup(data);
                                        }
                                })
                                m.openPopup()
                        })
                        return marker;
                        }   
                })//.addTo(resultMap);
	
	text_search_layer = new L.geoJson(fakeObject,{pointToLayer: function (feature, latlng) 
			{ 
			var marker = L.circleMarker(latlng, markerStyles[ feature.properties.layer ]  ).setRadius(5)			
			marker.bindPopup(feature.properties.popupContent);
			return marker;
			}			
		})	

    // var base_layers = {'Ancient':ancient_world,'Modern landscape':landscape,'Plain':plain_map,'Streets':esri_streets,'Legacy':legacy_terrain};
	// var base_layers = {'Legacy':legacy_terrain,'Modern landscape':landscape,'Plain':plain_map,'Streets':esri_streets};
	var base_layers = {'Default':esri_streets};

	layerSwitcher = new L.Control.Layers(base_layers,{'Burials':burials_markers,
	    //'Hoards':hoards_markers,'Stelae':stelae_markers,'Ogam':ogam_markers/*,'UK contours':uk_mainland_contours,'Surface water':surface_water*/}).addTo(resultMap);
		'Metalwork':metalwork_markers,'Stelae':stelae_markers,'Inscriptions':inscriptions_markers,'Grave goods':gravegoods_markers,'Buried individuals':individuals_markers,
		'Pots':pots_markers,'Toponyms':toponyms_markers,'Settlements':settlements_markers,'Roman roads':ba_roads }).addTo(resultMap);

	//surface_water.addTo(resultMap);	
	// Initial facet load requires multiple ajax calls:
	
	for (facet_family in facet_families) {
		$.ajax('/search/facet/?&query_type=' + facet_families[facet_family] ,
		    {
			async:false,
			success:function(data){
				$('#facet-' + facet_families[facet_family]).html(data);
			},
			dataType:'text'
		});
	};
	
	// Initialise slider
	
	$('#date-check').on('change', function(){
				//resultMap.spin(true);
				$('.spinner').addClass('active').removeClass('inactive')
				updateFacetedResults();
		}
	);

	// We need to initialise the event listeners ONLY on the NEW DOM elements other wise we get bubbling...
	
	intialiseFacetSearch();
	
    textSearchInitialise();	
	
	prepareContextLayerList();
	
    reorderLists();

	scaleBar = new L.control.scale({position:'bottomleft',metric:true}).addTo(resultMap);

    $(document).foundation();

    $('.leaflet-control-layers-overlays label').last().after(
        "<button class='expand button popup-extra radius less-padding' data-reveal-id='layer-modal' data-reveal>More layers...</button>");
	
	// Populate the more layers function
	$.ajax('/view/geojson_layers',{
		success:function(data){
			$('#layer-modal').html(data);
			
			$('.geojson-layer-select').on('click',function(){
				if ( $(this).attr('checked') ){
					addAjaxGeoJson( $(this).attr('data-verbose-name'),$(this).attr('id'),$(this).attr('data-category'), $(this).attr('data-src'));
					$(this).parent().addClass('selected');
				}
				else {
					window[$(this).attr('id')].clearLayers();
					window[$(this).attr('id')] = null;
					window[$(this).attr('id')] = undefined;
					$(this).parent().removeClass('selected');
				}
			});
		}
	})
	
	// Event for cluster toggle
	$('.layer-toggle').on('change',function(){
			if ( $(this).attr('checked') ){
				unclusterLayer( $(this).attr('data-layer') )
			}
			else {
				reclusterLayer( $(this).attr('data-layer') )			
			}
		});
    
    /*
	$('.layer-label-toggle').on('change',function(){
			if ( $(this).attr('checked') ){
				labelLayer( $(this).attr('data-layer') )
			}
			else {
				hideLabel( $(this).attr('data-layer') )			
			}
		}
	);    
    */
    
	$('.layer-label-toggle').on('change',function(){
		if ( $(this).attr('checked') ){
			labelLayer( $(this).attr('data-layer') );
			$(this).parent().removeClass('red').addClass('green');
			$(this).next().text('On');
		}
		else {
			hideLabel( $(this).attr('data-layer') );
			$(this).next().text('Off');
			$(this).parent().removeClass('green').addClass('red');					
		}
	});

// Initialise the FeatureGroup to store editable layers
drawnItems = new L.FeatureGroup();
resultMap.addLayer(drawnItems);

var options = {
    position: 'topright',
    draw: {
        polyline: false,
		polygon:false,
        circle: false, // Turns off this drawing tool
        rectangle: { shapeOptions: {
                color: 'rgba(0,0,0,0.25)',
				fillColor: 'rgba(255,255,255,0)',
				strokewidth: 0.5
			}},
        marker: false
    },
    edit: {
        featureGroup: drawnItems, //REQUIRED!!
        remove: true
    }
};

// Initialise the draw control and pass it the FeatureGroup of editable layers
var drawControl = new L.Control.Draw( options );

resultMap.addControl(drawControl);

resultMap.on('draw:created', function (e) {
    drawnItems.clearLayers()
    var type = e.layerType,
    layer = e.layer;
	resultMap.fitBounds(layer.getBounds());
    drawnItems.addLayer(layer);
    geomQuery = getGeom(layer)
    updateFacetedResults();
});

resultMap.on('draw:deleted', function (e) {
    geomQuery = '';
    var type = e.layerType,
        layer = e.layer;
    drawnItems.removeLayer(layer);
    updateFacetedResults();
});
	
});

function textSearchInitialise(){
	// Event listener for text search
	$("#text-search-submit").on('click',
		function(){
                var modelQ;
                if ( ($('input[name=model]:checked').val()) != 'all' ) {
                    modelQ = '&models=' + ( $('input[name=model]:checked').val());
                    uniqueTextSearchType = true;
                }
                else { 
                    modelQ = '';
                    uniqueTextSearchType = false;
                }
				updateTextResults(  $('#text-search').val() , modelQ );
		});

	$("#text-clear-submit").on('click',
		function(){
			updateTextResults('');
			$('#text-search').val('');
            textQuery = '';
		});
};

function updateTextResults(q, models){
	$.ajax('/search/text/?q=' + q + '&query_type=text' + models ,{
		success:function(data){
			$('#text-search-results > div').html(data); 
		},
		dataType:'text'
	});
	
    textQuery = '?q=' + q ;
    
	// Map
	$.ajax('/search/text/map/?q=' + q + '&query_type=text' + models + '&mime_type=application/json',{
		beforeSend: function(){
			$('.spinner').addClass('active').removeClass('inactive');
			$('.columns.large-3').addClass('waiting');
		},
		dataType:'jsonp',
        cache:true,
        jsonpCallback: 'parseMapTextResults',
        //jsonp: 'callback',
		async:true
	});
}

function parseMapTextResults(data){
	try{
		mapKey.removeFrom(resultMap)
	}
	catch (err) {
		//
	}		
	
	text_search_layer.clearLayers()
    geoJsonResults = data;
    for (r in geoJsonResults.features){
		if (r==0){
			
		}
        text_search_layer.addData(geoJsonResults.features[r]);
    };
	resultMap.addLayer(text_search_layer);
	$('.spinner').addClass('inactive').removeClass('active');
	$('.columns.large-3').removeClass('waiting');
};
	
function intialiseFacetSearch () {
	// Event listeners for checkboxes
	$(".facet-select").on('click',
		function(){

			$(this).parent().parent().parent().parent().parent().find('.switch-button input').attr('disabled', false);
			$(this).parent().parent().parent().parent().parent().find('.switch-button').removeClass('gray').addClass('green');
			
			
			$('.spinner').addClass('active').removeClass('inactive')

            lastFacetedObjectType = $(this).attr('object-type');
			var type = $(this).attr('facet-type');
			var value = $(this).attr('data-name');

			if ($(this).attr('checked')) {
				selectedFacets.push({type:type,value:value});
				// Make sure the exclude version is unchecked
				var toggleOff = '#' + $(this).attr('toggle_id');
					$(toggleOff).attr('checked',false);	
				var toggleOrOff = '#' + 'or_' + $(this).attr('id') ;
					$(toggleOrOff).attr('checked',false);	
					// And remove the associated excludedFacet reference
					for (ef in excludedFacets) {
						var currFact = excludedFacets[ef]
							if (currFact.type==type && currFact.value==value){
								excludedFacets.splice(ef,1);
								break;
							}
					}
					for (sof in selectedOrFacets) {
						var currFact = selectedOrFacets[sof]
							if (currFact.type==type && currFact.value==value){
								selectedOrFacets.splice(sof,1);
								break;
							}
					}					
			}
			else {
				for (sf in selectedFacets) {
					var currFact = selectedFacets[sf]
						if (currFact.type==type && currFact.value==value){
							selectedFacets.splice(sf,1);
							break;
						}
				}
			}
			//resultMap.spin(true);
			$('.spinner').addClass('active').removeClass('inactive')
			updateFacetedResults();
		}
	);

   	$(".facet-or-select").on('click',
		function(){
		
			$(this).parent().parent().parent().parent().parent().find('.switch-button input').attr('disabled', false);
			$(this).parent().parent().parent().parent().parent().find('.switch-button').removeClass('gray').addClass('green');
			
            lastFacetedObjectType = $(this).attr('object-type');
			var type = $(this).attr('facet-type');
			var value = $(this).attr('data-name');

			if ($(this).attr('checked')) {
				selectedOrFacets.push({type:type,value:value});
				// Make sure the exclude version is unchecked
				var toggleOff = '#' + $(this).attr('toggle_id');
					$(toggleOff).attr('checked',false);
				var toggleSelectedOff = '#' + $(this).attr('id').replace('or_','');
					$(toggleSelectedOff).attr('checked',false);	
					// And remove the associated excludedFacet reference
					for (ef in excludedFacets) {
						var currFact = excludedFacets[ef]
							if (currFact.type==type && currFact.value==value){
								excludedFacets.splice(ef,1);
								break;
							}
					}
					for (sf in selectedFacets) {
						var currFact = selectedFacets[sf]
							if (currFact.type==type && currFact.value==value){
								selectedFacets.splice(sf,1);
								break;
							}
					}					
			}
			else {
				for (sof in selectedOrFacets) {
					var currFact = selectedOrFacets[sof]
						if (currFact.type==type && currFact.value==value){
							selectedOrFacets.splice(sof,1);
							break;
						}
				}
			}
			//resultMap.spin(true);
			$('.spinner').addClass('active').removeClass('inactive')
			updateFacetedResults();
		});

	// Event listeners for checkboxes	
	$(".facet-exclude").on('click',
		function(){	
		
			$(this).parent().parent().parent().parent().parent().find('.switch-button input').attr('disabled', false);
			$(this).parent().parent().parent().parent().parent().find('.switch-button').removeClass('gray').addClass('green');
			
		
            lastFacetedObjectType = $(this).attr('object-type');                        
			var type = $(this).attr('facet-type');
			var value = $(this).attr('data-name');
			if ($(this).attr('checked')) {
				excludedFacets.push({type:type,value:value});
				// Make sure the select version is unchecked
				var toggleOff = '#' + $(this).attr('toggle_id');
				var toggleOrOff = '#' + 'or_' + $(this).attr('toggle_id');
					$(toggleOff).attr('checked',false);
					$(toggleOrOff).attr('checked',false);
					// And remove the associated selectedFacet reference
					for (sf in selectedFacets) {
						var currFact = selectedFacets[sf]
							if (currFact.type==type && currFact.value==value){
								selectedFacets.splice(sf,1);
								break;
							}
					}
					for (sof in selectedOrFacets) {
						var currFact = selectedOrFacets[sof]
							if (currFact.type==type && currFact.value==value){
								selectedOrFacets.splice(sof,1);
								break;
							}
					}				
			}
			else {
				for (ef in excludedFacets) {
					var currFact = excludedFacets[ef]
						if (currFact.type==type && currFact.value==value){
							excludedFacets.splice(ef,1);
							break;
						}
				}
			}
			//resultMap.spin(true);
			$('.spinner').addClass('active').removeClass('inactive')
			updateFacetedResults();
		});
};

// Is this redundant now?? NJ
function intialiseNewFacets(appendedDomElement){
	// Event listeners for checkboxes
	
	appendedDomElement.children('ul').children().children('li').children('.facet-select').on('click',
		function(){

			$(this).closest('div').parent('div').prev().prev().find('.switch-button input').attr('disabled', false);
			$(this).closest('div').parent('div').prev().prev().find('.switch-button').removeClass('gray').addClass('green');		
		
			$('.spinner').addClass('active').removeClass('inactive')

            lastFacetedObjectType = $(this).attr('object-type');
			// Testing recluster
			reclusterLayer( lastFacetedObjectType )		
			
			var type = $(this).attr('facet-type');
			var value = $(this).attr('data-name');
			// Get rid of punctuation			
			if ($(this).attr('checked')) {
				selectedFacets.push({type:type,value:value});
				// Make sure the exclude version is unchecked
				var toggleOff = '#' + $(this).attr('toggle_id');
					$(toggleOff).attr('checked',false);	
					// And remove the associated excludedFacet reference
					for (ef in excludedFacets) {
						var currFact = excludedFacets[ef]
							if (currFact.type==type && currFact.value==value){
								excludedFacets.splice(ef,1);
								break;
							}
					}
					for (sof in selectedOrFacets) {
						var currFact = selectedOrFacets[sof]
							if (currFact.type==type && currFact.value==value){
								selectedOrFacets.splice(sof,1);
								break;
							}
					}					
			}
			else {
				for (sf in selectedFacets) {
					var currFact = selectedFacets[sf]
						if (currFact.type==type && currFact.value==value){
							selectedFacets.splice(sf,1);
							break;
						}
				}
			}
			//resultMap.spin(true);
			$('.spinner').addClass('active').removeClass('inactive')
			updateFacetedResults();
		});
	
	// Or selections
	appendedDomElement.children('ul').children().children('li').children('.facet-or-select').on('click',
		function(){

			$(this).closest('div').parent('div').prev().prev().find('.switch-button input').attr('disabled', false);
			$(this).closest('div').parent('div').prev().prev().find('.switch-button').removeClass('gray').addClass('green');		
		
			$('.spinner').addClass('active').removeClass('inactive')

            lastFacetedObjectType = $(this).attr('object-type');
			// Testing recluster
			reclusterLayer( lastFacetedObjectType )		
			
			var type = $(this).attr('facet-type');
			var value = $(this).attr('data-name');
			// Get rid of punctuation			
			if ($(this).attr('checked')) {
				selectedOrFacets.push({type:type,value:value});
				// Make sure the exclude version is unchecked
				var toggleOff = '#' + $(this).attr('toggle_id');
					$(toggleOff).attr('checked',false);	
					// And remove the associated excludedFacet reference
					for (ef in excludedFacets) {
						var currFact = excludedFacets[ef]
							if (currFact.type==type && currFact.value==value){
								excludedFacets.splice(ef,1);
								break;
							}
					}
					for (sf in selectedFacets) {
						var currFact = selectedFacets[sf]
							if (currFact.type==type && currFact.value==value){
								selectedFacets.splice(sf,1);
								break;
							}
					}					
			}
			else {
				for (sof in selectedOrFacets) {
					var currFact = selectedOrFacets[sof]
						if (currFact.type==type && currFact.value==value){
							selectedOrFacets.splice(sof,1);
							break;
						}
				}
			}
			//resultMap.spin(true);
			$('.spinner').addClass('active').removeClass('inactive')
			updateFacetedResults();
		});	
	
	// Event listeners for checkboxes	
	
	appendedDomElement.children('ul').children().children('li').children('.facet-exclude').on('click',
		function(){

			$(this).closest('div').parent('div').prev().prev().find('.switch-button input').attr('disabled', false);
			$(this).closest('div').parent('div').prev().prev().find('.switch-button').removeClass('gray').addClass('green');		
		
            lastFacetedObjectType = $(this).attr('object-type');                        
			var type = $(this).attr('facet-type');
			var value = $(this).attr('data-name');
			// Get rid of numbers and punctuation
			/* Do this later - retain the original in the selectFacets array for matching later
			value = value.replace(/[\/,><-]/g,' ')
			*/
			if ($(this).attr('checked')) {
				excludedFacets.push({type:type,value:value});
				// Make sure the select version is unchecked
				var toggleOff = '#' + $(this).attr('toggle_id');
					$(toggleOff).attr('checked',false);
					// And remove the associated selectedFacet reference
					for (sf in selectedFacets) {
						var currFact = selectedFacets[sf]
							if (currFact.type==type && currFact.value==value){
								selectedFacets.splice(sf,1);
								break;
							}
					}
					for (sof in selectedOrFacets) {
						var currFact = selectedOrFacets[sof]
							if (currFact.type==type && currFact.value==value){
								selectedOrFacets.splice(sof,1);
								break;
							}
					}						
			}
			else {
				for (ef in excludedFacets) {
					var currFact = excludedFacets[ef]
						if (currFact.type==type && currFact.value==value){
							excludedFacets.splice(ef,1);
							break;
						}
				}
			}
			//resultMap.spin(true);
			$('.spinner').addClass('active').removeClass('inactive')
			updateFacetedResults();
		});	
}

var context_layers = ['regions_tribal_influence','sites_ritual_iron_age_roman'];

function prepareContextLayerList(){
	for (contextLayer in context_layers){
		$('#context-layers').append('<li><input class="layer-select" type="checkbox" layer-name="'+
		context_layers[contextLayer]+'"></input><label>'+
		context_layers[contextLayer]+'</label></li>')
	};
};

function labelGraticules(){
	for (i in graticules._layers) 
		{graticules._layers[i]._map.showLabel(graticules._layers[i].label)};
};

function reorderLists(){
	
	try {
		for (i in $('ul.atoz')){
			// Get list 
			var mylist = $('ul.atoz')[i]
			// Get list items
			var listitems = $($('ul.atoz')[i]).children('li')
			// Sort items
			listitems.sort(function(a,b){
				var compA = $(a).text().toUpperCase();
				var compB = $(b).text().toUpperCase();
				return (compA < compB) ? -1 : (compA > compB) ? 1 : 0; 
			})	
			// Append sorted list
			$.each(listitems,function(idx,itm) { 
				mylist.appendChild(itm);
			});
		}
	}
	catch (e) {
		//
	}
			// Get list 
			var mylist = $('.facetz.master') // Added master class
			// Get list items
			$(mylist).each(function(){
				var listitems = $(this).children('.facetz-container')
				// Sort items
				listitems.sort(function(a,b){
					var compA = $(a).children('h4').text().toUpperCase();
					var compB = $(b).children('h4').text().toUpperCase();
					return (compA < compB) ? -1 : (compA > compB) ? 1 : 0; 
				})	
				// Append sorted list
				
				/*
				$.each(listitems,function(idx,itm) { 
					this.appendChild(itm);
				});	
				*/
				$(this).children('form').after(listitems);
			})
	sortByChronology();
};

// Get that stuff yeah
function resultPaginate(pagenumber,query_type,query){
            if (query_type == 'text'){
				$.ajax('/search/text/?q=' + query + '&query_type=text&page=' + pagenumber,
				{
					success:function(data){
						$('#text-search-results > div').html(data);  
						dataType:'text'
					}
				})			
			}
			else {
				$.ajax('/search/refine/?' + window[query_type + 'Query' ]  + /* datequeryURL */ '&query_type=' + query_type + 
				'&page=' + pagenumber,
					{
						success:function(data){
							$('#'+ query_type +'-results > div').html(data);  
							dataType:'text'
					}
				})
			}
};

function unclusterLayer(layerToToggle){
	// remove cluster
	resultMap.removeLayer( window[layerToToggle + '_markers'] )
	resultMap.addLayer(window[layerToToggle])
	
	layerSwitcher.removeLayer( window[layerToToggle + '_markers'] )	
	layerSwitcher.addOverlay( window[layerToToggle], toTitleCase(layerToToggle) )

	$('.leaflet-control-layers-overlays label').last().after(
    "<button class='expand button popup-extra radius less-padding' data-reveal-id='layer-modal' data-reveal>More layers...</button>");
}

function reclusterLayer(layerToToggle){ 
	// remove cluster
	resultMap.removeLayer(window[layerToToggle])	
	resultMap.addLayer( window[layerToToggle + '_markers'] )
	
	layerSwitcher.removeLayer( window[layerToToggle] )	
	layerSwitcher.addOverlay( window[layerToToggle + '_markers'], toTitleCase(layerToToggle) )	
	
    $('.leaflet-control-layers-overlays label').last().after(
    "<button class='expand button popup-extra radius less-padding' data-reveal-id='layer-modal' data-reveal>More layers...</button>");
}

function toTitleCase(str)
{
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}
		
// Geojson stuff
// Peter Bray styles:

// GeoJson Styles
var lineStyle = {stroke:true,color:'#000000',weight:2,opacity:9}
var polyStyle = {stroke:true,color:'#000000',fill:true,fillColor:'#0000FF',fillOpacity:0.6,weight:2,opacity:7}

var icons = {'swords':( L.icon( {iconUrl: '/static/map_icons/swords.svg',iconSize:[32,32],iconAnchor:[16,32]}) ),
			 'shields':( L.icon( {iconUrl: '/static/map_icons/shields.svg',iconSize:[24,24],iconAnchor:[12,24]}) ),
			 'coins':( L.icon( {iconUrl: '/static/map_icons/coins.svg',iconSize:[24,24],iconAnchor:[12,24]}) ),
			 'roman':( L.icon( {iconUrl: '/static/map_icons/roman.svg',iconSize:[24,24],iconAnchor:[12,24]}) ),						
			 'ritual sites':( L.icon( {iconUrl: '/static/map_icons/ritual_sites.svg',iconSize:[22,22],iconAnchor:[11,22]}) ),
			 'souterrain':( L.icon( {iconUrl: '/static/map_icons/souterrain.svg',iconSize:[20,20],iconAnchor:[10,20]}) ),
			 'horse gear':( L.icon( {iconUrl: '/static/map_icons/horse.svg',iconSize:[32,32],iconAnchor:[16,32]}) ),
			 'axes':( L.icon( {iconUrl: '/static/map_icons/axes.svg',iconSize:[24,24],iconAnchor:[1,24]}) ),		
			 'spears':( L.icon( {iconUrl: '/static/map_icons/spears.svg',iconSize:[24,24],iconAnchor:[24,24]}) ),
			 'sculptures':( L.icon( {iconUrl: '/static/map_icons/sculptures.svg',iconSize:[24,24],iconAnchor:[1,24]}) ),
			 'pictish':( L.icon( {iconUrl: '/static/map_icons/pictish.svg',iconSize:[32,32],iconAnchor:[16,24]}) ),
             'personal ornaments':( L.icon( {iconUrl: '/static/map_icons/armlet.svg',iconSize:[32,32],iconAnchor:[16,24]}) )
			};

function onEachFeature(feature, layer) {
        layer.bindPopup( getPopup(feature,layer) );
};

function getMarkerStyle(cat){
	return icons[cat];
}

function getPopup(feat,lay){
	str = '<table><thead><tr><th colspan="2">'+ lay.options.layername +'</th></tr><tbody>';
	for (var k in feat.properties){
    	if (feat.properties.hasOwnProperty(k)) {
			if (k != 'ID'){
				str += "<tr><th>" + k + "</th><td>" + feat.properties[k] + "</td></tr>"
			}
    	}
	}
	str += "</tbody></thead>";
	return str;
};

function addAjaxGeoJson(layerName,shortName,category,filePath){
    window[shortName] = new L.GeoJSON.AJAX(filePath, {
    	onEachFeature:onEachFeature,
    	"layername":layerName,
		
    	style: function(feature) {
        	switch (feature.geometry.type) {
            	case 'LineString': return lineStyle;
            	case 'Polygon':  return polyStyle;
				case 'MultiPolygon':  return polyStyle;

            }
        },
		
        pointToLayer: function (feature, latlng) {
        	return L.marker(latlng,{ icon:getMarkerStyle(category),"layername":layerName} );
    	}
    } );
    resultMap.addLayer(window[shortName])
};

/* Sticky map in Search */

function zoomToRecord(lon,lat){
	if (lat != undefined) {
	    resultMap.setView([lat,lon],10)
	}
	else {
		alert('Record not mapped')
	}
}

function printMap() {
	leafletImage(resultMap, function(err, canvas) {
		var img = document.createElement('img');
		var dimensions = resultMap.getSize();
        img.width = (dimensions.x)*2;
        img.height = (dimensions.y)*2;
		extraCanvas()
		img.src = canvas.toDataURL();
		document.getElementById('map-image').innerHTML = '';
		document.getElementById('map-image').appendChild(img);
	});
	
	$('#map-image-details').find('h3').remove();
	$('#map-image-details').find('ul.filters').remove();	
	
    $.each($('.result-container.content'),function(){
		if ( $(this).find('ul.filters').length > 0){
			$('#map-image-details').append('<h3>'+ toTitleCase(($(this).attr('id')).replace('-results','')) +'</h3>')
			$(this).find('ul.filters').clone().appendTo('#map-image-details')
		}
	})
};

function extraCanvas(){
		//transX,transY
		//kmScaleWidth = $($('.leaflet-control-scale-line')[0]).css('width');
		kmScaleWidth = Math.ceil($($('.leaflet-control-scale-line')[0]).css('width').replace('px',''))
		kmValue = parseInt($($('.leaflet-control-scale-line')[0]).html().replace(' km','')) * 2

		//sw.distanceTo(L.latLng(sw.lat,resultMap.getBounds()._northEast.lng))/1000
		
		trans = resultMap.layerPointToContainerPoint( L.point( 0,0 ) )
		if ( trans.x > 0) {
			transX = 0 - trans.x;
		}
		else if ( trans.x < 0) {
			transX = Math.abs(trans.x) 
		}
		else {
			transX = 0;
		}

		if ( trans.y > 0) {
			transY = 0 - trans.y;
		}
		else if ( trans.x < 0) {
			transY = Math.abs(trans.y) 
		}
		else {
			transY = 0;
		}		

		cnvs = $('.leaflet-overlay-pane canvas')[0];
    	dtx =  cnvs.getContext('2d')
        dtx.font = "12px Arial";
        dtx.translate(transX,transY)
        dtx.fillText(resultMap.getBounds()._northEast.lat.toFixed(3) + ', ' + resultMap.getBounds()._southWest.lng.toFixed(3),10,15)
		dtx.fillText(kmValue + ' km',50, resultMap.getSize().y -50 )
		dtx.fillRect(25,resultMap.getSize().y -30,1,10)
		dtx.fillRect(25,resultMap.getSize().y -25, Math.ceil(kmScaleWidth), 1)
		dtx.fillRect(25 + Math.ceil(kmScaleWidth),resultMap.getSize().y -30,1,10)
		dtx.fillRect(25 + Math.ceil(kmScaleWidth) ,resultMap.getSize().y -25, Math.ceil(kmScaleWidth), 1)
		dtx.fillRect(25 + Math.ceil(kmScaleWidth) + Math.ceil(kmScaleWidth),resultMap.getSize().y -30,1,10)	
};

function makeTabActive(objectType){
	// Make correct tabe indicate active
	$('.tab-title').removeClass('active')	
	$('a[href="#'+objectType+'-results"]').parent().addClass('active')
	// Make correct content active
	$('.result-container.content').removeClass('active')
	$('#'+objectType+'-results').addClass('active')
}

function zoomToEngland(){
	resultMap.fitBounds(L.latLngBounds([47.17477833929903,-8.349609375],[57.7862326105289,4.7021484375]));
}

function zoomToIberia(){
	resultMap.fitBounds(L.latLngBounds([33.17434155100208,-10.8544921875],[46.55886030311719,2.79052734375]));
}

function zoomToEurope(){
	resultMap.fitBounds(L.latLngBounds([22, -38], [68,48]));
}

function zoomToFrance(){
	resultMap.fitBounds(L.latLngBounds([40.38002840251183,-5.4931640625],[52.40241887397332,7.55859375]));
}

function zoomToIreland(){
	resultMap.fitBounds(L.latLngBounds([50.91688748924508,-11.239013671875],[56.1210604250441,-4.713134765624999]));
}

/// Test functionality for pulsing chronological information

var pulseBurialsMarkersInterval;
var pulseIndividualsMarkersInterval;

chronoClean = [];
chrono.forEach( function(id){ chronoClean.push(id.trim()) })

timeSlice = 0; // To deal with unclassified at zero index

function pulseBurialsMarkers(){
    for (b in burials._layers) {
        if ( chronoClean.indexOf(burials._layers[b].feature.properties.extra_properties[0]['_general_chronology'] ) == timeSlice ) {
            
            setChronoPulseDisplay(chronoClean[timeSlice])
                        
            burials._layers[b].setRadius(10)
            burials._layers[b].setStyle({
                //radius: 15,
                fillColor: "#ff7800",
                color: "#000",
                weight: 1,
                opacity: 1,
            fillOpacity: 0.8})	
        }
        
        else {
            setChronoPulseDisplay(chronoClean[timeSlice])             
            burials._layers[b].setRadius(5)
            burials._layers[b].setStyle(markerStyles['burials'])	
        }
    }

    timeSlice ++;
    //console.log(timeSlice)
    if (timeSlice>chronoClean.length){
        //console.log('Finished!')
        clearInterval(pulseBurialsMarkersInterval)
        timeSlice = 0;
        btn.removeFrom(resultMap)        
    };
};

function pulseIndividualsMarkers(){

    for (b in individuals._layers) {
        if ( chronoClean.indexOf(individuals._layers[b].feature.properties.extra_properties[0]['_chronology'] ) == timeSlice ) {
            
            setChronoPulseDisplay(chronoClean[timeSlice])
            //console.log('match ' + b )
            individuals._layers[b].setRadius(10)
            individuals._layers[b].setStyle({
                fillColor: "#ff7800",
                color: "#000",
                weight: 1,
                opacity: 1,
                fillOpacity: 0.8,
                className:'z-up'})	
        }
        
        else {
            //console.log('not match ' + b )
            setChronoPulseDisplay(chronoClean[timeSlice])            
            individuals._layers[b].setRadius(5)
            //console.log(individuals._layers[b].getRadius())
            individuals._layers[b].setStyle(markerStyles['individuals'])	
        }       
    }

    timeSlice ++;
    //console.log(timeSlice)
    if (timeSlice>chronoClean.length){
        console.log('Finished!')
        clearInterval(pulseIndividualsMarkersInterval)
        timeSlice = 0;
        btn.removeFrom(resultMap)
    };
};

function pulseBurials(){
    if (timeSlice == 0){
    btn = L.functionButtons([{content:''}]).addTo(resultMap)           
        pulseBurialsMarkersInterval = setInterval(pulseBurialsMarkers,600);
    }
}

function pulseIndividuals(){
    if (timeSlice == 0){
    btn = L.functionButtons([{content:''}]).addTo(resultMap)        
    
    pulseIndividualsMarkersInterval = setInterval(pulseIndividualsMarkers,600);
    
    }
}

var btn;

function setChronoPulseDisplay(period){
    btn.setContent(period)
};

function labelLayer(layer){
    var layerToLabel = window[layer];
    for (var l in layerToLabel._layers){
        var m = layerToLabel._layers[l]
        m.bindLabel(
            getLabel(m)
            /*
            function () {
                console.log('yep')
                if (m.feature.properties["name"].indexOf(',')==-1){
                    return m.feature.properties["name"]
                }
                else {
                    return m.feature.properties["name"].substring(0,m.feature.properties["name"].indexOf(','))
                }
            }
            */
        )
        m.showLabel();        
    }
}

function hideLabel(layer){
    var layerToUnlabel = window[layer];
    for (l in layerToUnlabel._layers){
        var m = layerToUnlabel._layers[l]        
        m.unbindLabel()
    }    
}

function getLabel(m) {
    if (m.feature.properties["name"].indexOf(',')==-1){
        return m.feature.properties["name"]
    }
    else {
        return m.feature.properties["name"].substring(0,m.feature.properties["name"].indexOf(','))
    }
}
