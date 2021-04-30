from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.gis.geos import GEOSGeometry

from aema_geography.models import *

layers_dictionary = {'regions_tribal_influence': TribalRegalExtent, 'sites_ritual_iron_age_roman': RitualSitesIronAgeRoman}

def geoJsonLayer(request):
    layer = request.GET.get('layer')
    context = {}
    context['layer_name'] = layer
    print layer
    model = layers_dictionary.get(layer)
    print model
    context['layer'] = model.objects.all()
    if hasattr(model.objects.all()[0],'polygon'):
        #Return a geojson polygon?
        return render_to_response('aema_geography/poly_layer.js',context,context_instance=RequestContext(request),mimetype='application/text')
    if hasattr(model.objects.all()[0],'point'):
        return render_to_response('aema_geography/point_layer.js',context,context_instance=RequestContext(request),mimetype='application/text')