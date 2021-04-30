from django.contrib.gis import admin
from django.contrib.admin import TabularInline,StackedInline, ModelAdmin
from models import *

#class PalstavesRawAdmin(admin.OSMGeoAdmin):
    #list_display = ('id','site_name','object','datasheet_name','museum','analysis_code')
    #search_fields = ('object','site_name','datasheet_name','museum','analysis_code')
    #
    #fieldsets = (
     #   ('Description',{
      #      'fields':('object','site_name','database_code','datasheet_name','museum','analysis_code'),
       #     'classes':('collapse-closed',)        
       # }),
        #('Core measures',{
         #   'fields':('pb','sn','averages','ad_as_0_1_bool','ad_sb_0_1_bool','ad_ag_0_1_bool','ad_ni_0_1_bool',\
			#'adjusted_as','adjusted_sb','adjusted_ag','adjusted_ni'),
            #'classes':('collapse-open',)        
        #}),		
    #)

class BasicAdmin(admin.OSMGeoAdmin):
    pass
	
#admin.site.register(PalstavesRaw, PalstavesRawAdmin)

#admin.site.register(PalstaveAverageValues,admin.OSMGeoAdmin) 

admin.site.register(Metallurgy,BasicAdmin)

