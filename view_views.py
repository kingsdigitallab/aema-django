from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.gis.geos import GEOSGeometry

from aema_db.models import *
from aema_geography.models import *
from early_celtic_society.models import Core

def burial_view(request,id):
    id = id
    context = {}
    context['burial'] = Burials.objects.get(pk=id)
    return render_to_response('aema_db/burial.html',context,context_instance=RequestContext(request))


def burial_full_view(request,id):
    id = id
    context = {}
    burial = Burials.objects.get(pk=id)
    context['burial'] = burial
    # Get nearby burials 
    # transform the point
    p = GEOSGeometry( 'POINT(' + str(burial.point.x) + ' ' + str(burial.point.y) + ')', srid=4326)
    p.transform('EPSG:3857')
    tenpoly = p.buffer(10000,12)
    tenpoly.transform('EPSG:4326')
    ten = Burials.objects.filter(point__intersects=tenpoly).exclude(pk=id)
    for t in ten:
        tPoint = GEOSGeometry( 'POINT(' + str(t.point.x) + ' ' + str(t.point.y) + ')', srid=4326)
        tPoint.transform('EPSG:3857')
        t.distance = int(tPoint.distance(p)/1000)
    fiftytpoly = p.buffer(50000,12)
    fiftytpoly.transform('EPSG:4326')
    fifty = Burials.objects.filter(point__intersects=fiftytpoly).exclude(point__intersects=tenpoly).exclude(pk=id)
    for t in fifty:
        tPoint = GEOSGeometry( 'POINT(' + str(t.point.x) + ' ' + str(t.point.y) + ')', srid=4326)
        tPoint.transform('EPSG:3857')
        t.distance = int(tPoint.distance(p)/1000)
    # put burial point back again!
    context['ten'] = ten 
    context['fifty'] = fifty
    return render_to_response('aema_db/burial_full.html',context,context_instance=RequestContext(request))

def individuals_full_view(request,id):
    id = id
    context = {}
    individual = BurialIndividuals.objects.get(pk=id)
    context['individual'] = individual
    # Get nearby burials 
    # transform the point
    p = GEOSGeometry( 'POINT(' + str(individual.burial.point.x) + ' ' + str(individual.burial.point.y) + ')', srid=4326)
    p.transform('EPSG:3857')
    tenpoly = p.buffer(10000,12)
    tenpoly.transform('EPSG:4326')
    ten = Burials.objects.filter(point__intersects=tenpoly).exclude(pk=individual.burial.id)
    for t in ten:
        tPoint = GEOSGeometry( 'POINT(' + str(t.point.x) + ' ' + str(t.point.y) + ')', srid=4326)
        tPoint.transform('EPSG:3857')
        t.distance = int(tPoint.distance(p)/1000)
    fiftytpoly = p.buffer(50000,12)
    fiftytpoly.transform('EPSG:4326')
    fifty = Burials.objects.filter(point__intersects=fiftytpoly).exclude(point__intersects=tenpoly).exclude(pk=id)
    for t in fifty:
        tPoint = GEOSGeometry( 'POINT(' + str(t.point.x) + ' ' + str(t.point.y) + ')', srid=4326)
        tPoint.transform('EPSG:3857')
        t.distance = int(tPoint.distance(p)/1000)
    # put burial point back again!
    context['ten'] = ten 
    context['fifty'] = fifty    
    return render_to_response('aema_db/individuals_full.html',context,context_instance=RequestContext(request))  

def burial_popup(request,id):
    b =  Burials.objects.get(pk=id)
    content =  b.popup_content()
    return HttpResponse(content)
    
def pots_popup(request,id):
    p = Pot.objects.get(pk=id)
    b = Burials.objects.get(pk=p.burial.id)
    content =  b.popup_content()
    return HttpResponse(content)

def gravegoods_popup(request,id):
    p = GraveGood.objects.get(pk=id)
    b = Burials.objects.get(pk=p.burial.id)
    content =  b.popup_content()
    return HttpResponse(content)    

def toponyms_popup(request,id):
    b =  Toponyms.objects.get(pk=id)
    content =  b.popup_content()
    return HttpResponse(content)
    
    
def toponyms_full_view(request,id):
    id = id
    context = {}
    toponym = Toponyms.objects.get(pk=id)
    context['toponym'] = toponym
    # Get nearby burials 
    # transform the point
    p = GEOSGeometry( 'POINT(' + str(toponym.point.x) + ' ' + str(toponym.point.y) + ')', srid=4326)
    p.transform('EPSG:3857')
    tenpoly = p.buffer(10000,12)
    tenpoly.transform('EPSG:4326')
    ten = Toponyms.objects.filter(point__intersects=tenpoly).exclude(pk=id)
    for t in ten:
        tPoint = GEOSGeometry( 'POINT(' + str(t.point.x) + ' ' + str(t.point.y) + ')', srid=4326)
        tPoint.transform('EPSG:3857')
        t.distance = int(tPoint.distance(p)/1000)
    fiftytpoly = p.buffer(50000,12)
    fiftytpoly.transform('EPSG:4326')
    fifty = Toponyms.objects.filter(point__intersects=fiftytpoly).exclude(point__intersects=tenpoly).exclude(pk=id)
    for t in fifty:
        tPoint = GEOSGeometry( 'POINT(' + str(t.point.x) + ' ' + str(t.point.y) + ')', srid=4326)
        tPoint.transform('EPSG:3857')
        t.distance = int(tPoint.distance(p)/1000)
    # put burial point back again!
    context['ten'] = ten 
    context['fifty'] = fifty    
    return render_to_response('aema_db/toponym_full.html',context,context_instance=RequestContext(request))      

def settlements_popup(request,id):
    b =  Core.objects.get(pk=id)
    content =  b.popup_content()
    return HttpResponse(content)

def settlements_full_view(request,id):
    id = id
    context = {}
    settlement = Core.objects.get(pk=id)
    context['settlement'] = settlement
    # Get nearby burials 
    # transform the point
    p = GEOSGeometry( 'POINT(' + str(settlement.point.x) + ' ' + str(settlement.point.y) + ')', srid=4326)
    p.transform('EPSG:3857')
    tenpoly = p.buffer(10000,12)
    tenpoly.transform('EPSG:4326')
    ten = Core.objects.filter(point__intersects=tenpoly).exclude(pk=id)
    for t in ten:
        tPoint = GEOSGeometry( 'POINT(' + str(t.point.x) + ' ' + str(t.point.y) + ')', srid=4326)
        tPoint.transform('EPSG:3857')
        t.distance = int(tPoint.distance(p)/1000)
    fiftytpoly = p.buffer(50000,12)
    fiftytpoly.transform('EPSG:4326')
    fifty = Core.objects.filter(point__intersects=fiftytpoly).exclude(point__intersects=tenpoly).exclude(pk=id)
    for t in fifty:
        tPoint = GEOSGeometry( 'POINT(' + str(t.point.x) + ' ' + str(t.point.y) + ')', srid=4326)
        tPoint.transform('EPSG:3857')
        t.distance = int(tPoint.distance(p)/1000)
    # put burial point back again!
    context['ten'] = ten 
    context['fifty'] = fifty    
    return render_to_response('aema_db/settlement_full.html',context,context_instance=RequestContext(request))   

def metalwork_popup(request,id):
    b =  Hoards.objects.get(pk=id)
    content =  b.popup_content()
    return HttpResponse(content)
    
def miscellaneous_view(request,id):
    id = id
    context = {}
    context['miscellaneous'] = Miscellaneous.objects.get(pk=id)
    return render_to_response('aema_db/miscellaneous.html',context,context_instance=RequestContext(request))

def miscellaneous_full_view(request,id):
    hoard = Miscellaneous.objects.get(pk=id)
    context = {}
    # resusing hoard here so as  not to rewrite template...
    context['hoard'] = Miscellaneous.objects.get(pk=id)
    p = GEOSGeometry( 'POINT(' + str(hoard.point.x) + ' ' + str(hoard.point.y) + ')', srid=4326)
    p.transform('EPSG:3857')
    tenpoly = p.buffer(10000,12)
    tenpoly.transform('EPSG:4326')
    ten = Miscellaneous.objects.filter(point__intersects=tenpoly).exclude(pk=id)
    for t in ten:
        tPoint = GEOSGeometry( 'POINT(' + str(t.point.x) + ' ' + str(t.point.y) + ')', srid=4326)
        tPoint.transform('EPSG:3857')
        t.distance = int(tPoint.distance(p)/1000)
    fiftytpoly = p.buffer(50000,12)
    fiftytpoly.transform('EPSG:4326')
    fifty = Miscellaneous.objects.filter(point__intersects=fiftytpoly).exclude(point__intersects=tenpoly).exclude(pk=id)
    for t in fifty:
        tPoint = GEOSGeometry( 'POINT(' + str(t.point.x) + ' ' + str(t.point.y) + ')', srid=4326)
        tPoint.transform('EPSG:3857')
        t.distance = int(tPoint.distance(p)/1000)
    # put burial point back again!
    context['ten'] = ten 
    context['fifty'] = fifty    
    return render_to_response('aema_db/misc_full.html',context,context_instance=RequestContext(request))    
    
def miscellaneous_popup(request,id):
    b =  Miscellaneous.objects.get(pk=id)
    content =  b.popup_content()
    return HttpResponse(content)
    

def stelae_popup(request,id):
    b =  Stelae.objects.get(pk=id)
    content =  b.popup_content()
    return HttpResponse(content)

def ogam_popup(request,id):
    b =  OgamSite.objects.get(pk=id)
    content =  b.popup_content()
    return HttpResponse(content)

def individuals_popup(request,id):
    b =  BurialIndividuals.objects.get(pk=id)
    content =  b.popup_content()
    return HttpResponse(content)


def hoard_view(request,id):
    id = id
    context = {}
    context['hoard'] = Hoards.objects.get(pk=id)
    return render_to_response('aema_db/hoard.html',context,context_instance=RequestContext(request))

def hoard_full_view(request,id):
    id = id
    context = {}
    hoard = Hoards.objects.get(pk=id)
    context['hoard'] = hoard
    # Get nearby burials 
    # transform the point
    p = GEOSGeometry( 'POINT(' + str(hoard.point.x) + ' ' + str(hoard.point.y) + ')', srid=4326)
    p.transform('EPSG:3857')
    tenpoly = p.buffer(10000,12)
    tenpoly.transform('EPSG:4326')
    ten = Hoards.objects.filter(point__intersects=tenpoly).exclude(pk=id)
    for t in ten:
        tPoint = GEOSGeometry( 'POINT(' + str(t.point.x) + ' ' + str(t.point.y) + ')', srid=4326)
        tPoint.transform('EPSG:3857')
        t.distance = int(tPoint.distance(p)/1000)
    fiftytpoly = p.buffer(50000,12)
    fiftytpoly.transform('EPSG:4326')
    fifty = Hoards.objects.filter(point__intersects=fiftytpoly).exclude(point__intersects=tenpoly).exclude(pk=id)
    for t in fifty:
        tPoint = GEOSGeometry( 'POINT(' + str(t.point.x) + ' ' + str(t.point.y) + ')', srid=4326)
        tPoint.transform('EPSG:3857')
        t.distance = int(tPoint.distance(p)/1000)
    # put burial point back again!
    context['ten'] = ten 
    context['fifty'] = fifty        
    return render_to_response('aema_db/hoard_full.html',context,context_instance=RequestContext(request))
    
    
def stelae_view(request,id):
    id = id
    context = {}
    context['stelae'] = Stelae.objects.get(pk=id)
    return render_to_response('aema_db/stelae.html',context,context_instance=RequestContext(request))

def stelae_full_view(request,id):
    id = id
    context = {}
    stelae = Stelae.objects.get(pk=id)
    context['stelae'] = stelae
    # Get nearby burials 
    # transform the point
    p = GEOSGeometry( 'POINT(' + str(stelae.point.x) + ' ' + str(stelae.point.y) + ')', srid=4326)
    p.transform('EPSG:3857')
    tenpoly = p.buffer(10000,12)
    tenpoly.transform('EPSG:4326')
    ten = Stelae.objects.filter(point__intersects=tenpoly).exclude(pk=id)
    for t in ten:
        tPoint = GEOSGeometry( 'POINT(' + str(t.point.x) + ' ' + str(t.point.y) + ')', srid=4326)
        tPoint.transform('EPSG:3857')
        t.distance = int(tPoint.distance(p)/1000)
    fiftytpoly = p.buffer(50000,12)
    fiftytpoly.transform('EPSG:4326')
    fifty = Stelae.objects.filter(point__intersects=fiftytpoly).exclude(point__intersects=tenpoly).exclude(pk=id)
    for t in fifty:
        tPoint = GEOSGeometry( 'POINT(' + str(t.point.x) + ' ' + str(t.point.y) + ')', srid=4326)
        tPoint.transform('EPSG:3857')
        t.distance = int(tPoint.distance(p)/1000)
    # put burial point back again!
    context['ten'] = ten
    context['fifty'] = fifty
    return render_to_response('aema_db/stelae_full.html',context,context_instance=RequestContext(request))



def ogam_view(request,id):
    id = id
    context = {}
    context['ogam'] = OgamSite.objects.get(pk=id)
    return render_to_response('aema_db/ogam.html',context,context_instance=RequestContext(request))

def ogam_full_view(request,id):
    ogam = OgamSite.objects.get(pk=id)
    context = {}
    context['ogam'] = ogam
    # Get nearby burials 
    # transform the point
    p = GEOSGeometry( 'POINT(' + str(ogam.point.x) + ' ' + str(ogam.point.y) + ')', srid=4326)
    p.transform('EPSG:3857')
    tenpoly = p.buffer(10000,12)
    tenpoly.transform('EPSG:4326')
    ten = OgamSite.objects.filter(point__intersects=tenpoly).exclude(pk=id)
    for t in ten:
        tPoint = GEOSGeometry( 'POINT(' + str(t.point.x) + ' ' + str(t.point.y) + ')', srid=4326)
        tPoint.transform('EPSG:3857')
        t.distance = int(tPoint.distance(p)/1000)
    fiftytpoly = p.buffer(50000,12)
    fiftytpoly.transform('EPSG:4326')
    fifty = OgamSite.objects.filter(point__intersects=fiftytpoly).exclude(point__intersects=tenpoly).exclude(pk=id)
    for t in fifty:
        tPoint = GEOSGeometry( 'POINT(' + str(t.point.x) + ' ' + str(t.point.y) + ')', srid=4326)
        tPoint.transform('EPSG:3857')
        t.distance = int(tPoint.distance(p)/1000)
    # put burial point back again!
    context['ten'] = ten
    context['fifty'] = fifty    
    return render_to_response('aema_db/ogam_full.html',context,context_instance=RequestContext(request))    
    
    
def individuals_view(request,id):
    id = id
    context = {}
    context['burial'] = BurialIndividuals.objects.get(pk=id)
    return render_to_response('aema_db/individuals.html',context,context_instance=RequestContext(request))

 
	
def geojson_layers(request):
    context = {}
    context['layers'] = GeojsonFile.objects.filter(category__major_category__isnull=False).order_by('category__short_description','short_description')
    return render_to_response('aema_geography/layers.html',context,context_instance=RequestContext(request))

def metallury_geojson(request):
    from django.db import connection
    from decimal import Decimal
    import json
    AsTol = Decimal(request.GET.get("astol"))
    SbTol = Decimal(request.GET.get("sbtol"))
    AgTol = Decimal(request.GET.get("agtol"))
    NiTol = Decimal(request.GET.get("nitol"))
    SnTol = Decimal(request.GET.get("sbtol"))
    PbTol = Decimal(request.GET.get("agtol"))
    ZnTol = Decimal(request.GET.get("nitol"))	
    gridSize = Decimal(request.GET.get("gridsize",0))
    hexGrid = Decimal(request.GET.get("hexGrid",0))    
    cursor = connection.cursor()
    if gridSize > 0:
        cursor.execute("select * from getcoppergroupsgeojson(%s,%s,%s,%s,%s,%s,%s,%s);",[AsTol,SbTol,AgTol,NiTol,SnTol,PbTol,ZnTol,gridSize]) 	
        context = {}
        geoJsonArray = []
        for m in cursor.fetchall():
            geoJsonArray.append(json.dumps(m))
        context['metal_grid'] = geoJsonArray
        return render_to_response('aema_metallurgy/metal_geojson.js',context,context_instance=RequestContext(request)\
            ,mimetype="application/json")
    else:
        cursor.execute("select * from getcoppergroupsgeojson_hex%s(%s,%s,%s,%s,%s,%s,%s,%s);",[hexGrid,AsTol,SbTol,AgTol,NiTol,SnTol,PbTol,ZnTol,'hex']) 	
        context = {}
        geoJsonArray = []
        for m in cursor.fetchall():
            geoJsonArray.append(json.dumps(m))
        context['metal_grid'] = geoJsonArray
        return render_to_response('aema_metallurgy/metal_geojson.js',context,context_instance=RequestContext(request)\
            ,mimetype="application/json")
