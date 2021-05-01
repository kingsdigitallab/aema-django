# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth import authenticate
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def geofield_js(request,field):
    context = {}
    context['geofield_js'] = field
    return render('geofield_js.js', context, content_type='application/text')
	
	
