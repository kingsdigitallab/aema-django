{% load i18n %}

$(document).ready(function(){
	formHTML = 
	'<div id="geo-wrapper" style="float:left;display:block;margin-left:20px;">'+
	'<p>Basic geocoding tools</p>'+
		'<span id="geo-fields">'+
		'<input id="geocode-string" style="display:block;margin-top:10px;" type="text"></input>'+
		'<label></label>'+
		'<input type="button"  style="display:block;margin-top:10px;" value="Sumbit search text" onclick="getPoints()"></input>'+
    	'<select id="geocode_select" style="display:block;margin-top:10px;"></select>'
		'<span>'+
	'</div>'

	$('#id_{{ geofield_js }}_admin_map').after(formHTML);
	
    $('#geocode_select').change(function(){
		centreMap(	$(this).val()	)
	})
});


function getPoints(){
    //Clear the list
	$('#geocode_select').html('');
    var val = $('#geocode-string').val();

		//base_url = '/nominatim.openstreetmap.org/search?';
                base_url = '/nominatim/search?';
		query_url = 'q='+val;
		params = '&format=json&json_callback=listPoints'
		
		url = base_url + query_url + params;
		
		$.ajax({
			url: url,
			dataType: "jsonp",
			async:true,
			jsonpCallback: "listPoints",
			jsonp: 'callback'
		});
}


function listPoints(locations){
	locationList = locations;
	$('#geocode_select').append('<option value="">...</option>');
	for (l in locations){
		var str = locations[l].display_name;
		var opt = l;
		$('#geocode_select').append('<option value='+l+'>'+str+'</option>');
	}
}


function centreMap(l){
	// First reproject the point
	rp = wgs84toWebmerc(parseFloat(locationList[l].lon),parseFloat(locationList[l].lat));
	// User returned value to recenter tha map
	var pnt = new OpenLayers.LonLat(
		rp.x,
		rp.y
	);
	geodjango_{{ geofield_js }}.map.setCenter(pnt,13);

	geodjango_{{ geofield_js }}.map.setCenter(pnt,12);
	// Create a point
        var map = geodjango_{{ geofield_js }}.map
        var op = new OpenLayers.Geometry.Point(rp.x,rp.y)
        var f = new OpenLayers.Feature.Vector(op)
        var l = geodjango_point.layers.vector
        l.addFeatures(f)
}

function wgs84toWebmerc(lon,lat){
	var world = new Proj4js.Proj('EPSG:4326');
	var webmerc = new Proj4js.Proj('EPSG:900913');
	var p = new Proj4js.Point(lon,lat);
	Proj4js.transform(world,webmerc,p);
	return p;
}


