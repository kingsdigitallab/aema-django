addContextLayer(
{ "type": "FeatureCollection",
  "layerName" : "{{ layer_name }}",
  "features": [

{% for feature in layer %}
		{
        "type": "Feature",
        "properties": {
                "id" :  "{{ feature.id }}",
				"popupContent" : "{{ feature.popup_content|safe }}"
        }                                        
                ,"geometry":
                	{{ feature.point.geojson|safe }}
                	
}{% if not forloop.last %},{% endif %}

{% endfor %}
]}
);

