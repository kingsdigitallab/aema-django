from django.template import RequestContext
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.gis.geos import GEOSGeometry
from django.views.decorators.csrf import csrf_exempt

import urllib2


from settings import *

"""
req = urllib2.Request("http://vimeo.com/api/v2/video/38356.json", None, {'user-agent':'syncstream/vimeo'})
opener = urllib2.build_opener()
f = opener.open(req)
simplejson.load(f)
"""


from aema_db.models import *


@csrf_exempt
def export_json(request,layer):
    context = {}
    context['json'] = request.POST.get('stringified-json','')
    return render(request, 'aema_db/db_query.js', context, content_type='application/force-download')

@csrf_exempt	
def export_csv(request,layer):
    context = {}
    query = request.POST.get('stringified-csv','')
    queryModelType = request.POST.get('textsearchmodel','')    
    req = urllib2.Request( 'https://' + request.META['HTTP_HOST'] + "/search/csv/?" + query.replace(' ','%20') + "&textsearchmodel=" + queryModelType )
    opener =  urllib2.build_opener()
    csv =  opener.open(req)
    return HttpResponse( csv.read(),mimetype='application/force-download')
