from django.contrib.gis import admin
from django import forms
from django.contrib.admin import TabularInline,StackedInline, ModelAdmin
from models import *


class BasicAdmin(admin.OSMGeoAdmin):
    pass

class FindInline(StackedInline):
    model = Finds
    extra = 1
	
class EnviroDataInline(StackedInline):
    model = EnviroData
    extra = 1
	
class GeneralInfoInline(StackedInline):
    model = GeneralInfo
    extra = 1
	
class HouseDataInline(StackedInline):
    model = HouseData
    extra = 1
	
class SiteAttributesInline(StackedInline):
    model = SiteAttributes
    extra = 1

class RadioCarbonDatesInline(StackedInline):
    model = RadioCarbonDates
    extra = 1

class SourcesInline(StackedInline):
    model = Sources
    extra = 1	
	

class CoreAdmin(admin.OSMGeoAdmin):
    list_display = ('name','type',)
    search_fields = ('name','type')
    filter_horizontal = ('type_m2m',)
    fieldsets = (
        ('Basic',{
            'fields':('name','point','type','type_m2m','status','reference'),
            'classes':('collapse-open',)        
        }),
        ('Further details',{
            'fields':('desc_1','no_of_houses','form','period','periodspec','broadclass','project','compiledon',\
                'category','grade','unitary','community','map','wat'),
            'classes':('collapse-closed',)                     
        }),
    )
    inlines = [GeneralInfoInline,SiteAttributesInline,FindInline,HouseDataInline,EnviroDataInline,\
        SourcesInline,RadioCarbonDatesInline]
    class Media:
        geocodefield = 'point'
        js = ['/geofield/%s/geocode.js' % (geocodefield),\
        '/static/js/proj4js/lib/proj4js-compressed.js']	
	
admin.site.register(Core,CoreAdmin)
admin.site.register(Finds,BasicAdmin)
admin.site.register(EnviroData,BasicAdmin)
admin.site.register(GeneralInfo,BasicAdmin)
admin.site.register(HouseData,BasicAdmin)
admin.site.register(SiteAttributes,BasicAdmin)
admin.site.register(RadioCarbonDates,BasicAdmin)
admin.site.register(Sources,BasicAdmin)
admin.site.register(Type,BasicAdmin)
admin.site.register(SubType,BasicAdmin)
