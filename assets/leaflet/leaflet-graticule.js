/*
 Graticule plugin for Leaflet powered maps.
 */
 
function onEachFeature(feature, layer) {
		if (feature.properties.name.indexOf('° S')!=-1 || feature.properties.name.indexOf('° N')!=-1 || feature.properties.name.indexOf('rime')!=-1){		
			layer.bindLabel(feature.properties.name, {noHide: true,direction:'auto',className:'lat-label'});
			layer.label.setLatLng([layer._latlngs[0].lat,resultMap.getBounds()._southWest.lng]	);		
		}

		if (feature.properties.name.indexOf('° E')!=-1 || feature.properties.name.indexOf('° W')!=-1 || feature.properties.name.indexOf('quator')!=-1){
			layer.bindLabel(feature.properties.name, {noHide: true,direction:'left',className:'lng-label',offset:[-4,15]});
			layer.label.setLatLng([(resultMap.getBounds()._northEast.lat),layer._latlngs[0].lng]	);		
		}
		if (feature.properties.name.indexOf('blank')!=-1){
			layer.bindLabel('', {noHide: true,direction:'left',className:'lng-label',offset:[-4,15]});
			layer.label.setLatLng([(resultMap.getBounds()._northEast.lat),layer._latlngs[0].lng]	);		
		}

};




 
L.Graticule = L.GeoJSON.extend({

    options: {
        style: {
            color: '#333',
            weight: 1
        },
    interval: 20,
	onEachFeature: onEachFeature
    },

    initialize: function (options) {
        L.Util.setOptions(this, options);
        this._layers = {};

        if (this.options.sphere) {
            this.addData(this._getFrame());
        } else {
            this.addData(this._getGraticule());      
        }
    },

	
	
	
    _getFrame: function() {
        return { "type": "Polygon",
          "coordinates": [
              this._getMeridian(-180).concat(this._getMeridian(180).reverse())
          ]
        };
    },

    _getGraticule: function () {
        var features = [], interval = this.options.interval;

        // Meridians
        //for (var lng = 0; lng <= 180; lng = lng + interval) {
        for (var lng = Math.floor(resultMap.getBounds()._southWest.lng)-(Math.floor(resultMap.getBounds()._southWest.lng)%interval);
        lng <= Math.ceil(resultMap.getBounds()._northEast.lng)+ (interval - (Math.ceil(resultMap.getBounds()._northEast.lng)%interval)); 
        	lng = lng + interval) {
					
            features.push(this._getFeature(this._getMeridian(lng), {
                "name": (lng) ? lng.toString() + "° E" : "Prime meridian"    
            }));
            if (lng !== 0) {
                features.push(this._getFeature(this._getMeridian(-lng), {
                    "name": lng.toString() + "°blank W"
                }));    
            }
        }

        // Parallels
        //for (var lat = 0; lat <= 90; lat = lat + interval) {  
        for (var lat = Math.floor(resultMap.getBounds()._southWest.lat); lat <= Math.ceil(resultMap.getBounds()._northEast.lat); 
        	lat = lat + interval) {
	
            features.push(this._getFeature(this._getParallel(lat), {
                "name": (lat) ? lat.toString() + "° N" : "Equator"   
            }));
            if (lat !== 0) {
                features.push(this._getFeature(this._getParallel(-lat), {
                    "name": lat.toString() + "° S"
                }));      
            }
        } 

        return {
            "type": "FeatureCollection",
            "features": features
        };
    },

    _getMeridian: function (lng) {
        lng = this._lngFix(lng);
        var coords = [];
        for (var lat = -90; lat <= 90; lat++) {
            coords.push([lng, lat]);
        }
        return coords;
    },

    _getParallel: function (lat) {
        var coords = [];
        for (var lng = -180; lng <= 180; lng++) {
            coords.push([this._lngFix(lng), lat]);
        }
        return coords;    
    },

    _getFeature: function (coords, prop) {
        return {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coords
            },
            "properties": prop
        }
    },

    _lngFix: function (lng) {
        if (lng >= 180) return 179.999999;
        if (lng <= -180) return -179.999999;
        return lng;        
    }  

});

L.graticule = function (options) {
    return new L.Graticule(options);
};