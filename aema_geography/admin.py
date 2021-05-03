from django.contrib.gis import admin
from django import forms
from django.contrib.admin import TabularInline,StackedInline, ModelAdmin
from .models import *
from django.contrib.gis import admin
from django import forms
from django.contrib.admin import TabularInline,StackedInline, ModelAdmin


class RitualSitesIronAgeRomanAdmin(admin.OSMGeoAdmin):
    list_display = ('location','description')
    search_fields = ('description','location')

    class Media:
        geocodefield = 'point'
        js = ['/geofield/%s/geocode.js' % (geocodefield),\
        '/static/js/proj4js/lib/proj4js-compressed.js']


class TribalRegalExtentAdmin(admin.OSMGeoAdmin):
    list_display = ('description',)
    search_fields = ('description',)


class GeojsonFileAdmin(admin.OSMGeoAdmin):
    list_display = ('friendly_description','category',)
    search_fields = ['friendly_description',]

class BasicAdmin(admin.OSMGeoAdmin):
    pass


admin.site.register(RitualSitesIronAgeRoman, RitualSitesIronAgeRomanAdmin)
admin.site.register(TribalRegalExtent, TribalRegalExtentAdmin)


admin.site.register(GeojsonFile,GeojsonFileAdmin)
admin.site.register(GeojsonCategory,BasicAdmin)
admin.site.register(GeojsonMajorCategory,BasicAdmin)
