from django.conf.urls import *

urlpatterns = patterns('aema_geography',
    url(r'^$', 'views.geoJsonLayer'),
)