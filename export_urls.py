from django.conf.urls.defaults import *

urlpatterns = patterns('export_views',
    url(r'^(\w+)/output.json','export_json'),
    url(r'^(\w+).csv$','export_csv'),		
)
