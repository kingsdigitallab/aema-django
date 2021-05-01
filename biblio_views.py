from django.template import RequestContext
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.gis.geos import GEOSGeometry
from aema_db.models import *


def biblio_view(request):
    context = {}
    context['biblios'] = Bibliography.objects.all().order_by('title').order_by('year')
    return render(request, 'aema_db/biblio.html', context)
