from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('geofield.views',
    # For creating custom js to append to admin screen as configured in app/admin.py
    (r'^(\w+)/geocode.js', 'geofield_js'),
)
