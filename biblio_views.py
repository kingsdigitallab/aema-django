from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.gis.geos import GEOSGeometry

from aema_db.models import *


def biblio_view(request):
    context = {}
    context['biblios'] = Bibliography.objects.all().order_by('title').order_by('year')
    return render_to_response('aema_db/biblio.html',context,context_instance=RequestContext(request))


