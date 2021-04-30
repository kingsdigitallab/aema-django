from django.conf.urls.defaults import *

urlpatterns = patterns('aema_geography',
    url(r'^$', 'views.geoJsonLayer'),
)