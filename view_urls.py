from django.conf.urls import *

urlpatterns = patterns('view_views',
    url(r'^burials/(\d+)/$','burial_view'),
    url(r'^burials_full/(\d+)/$','burial_full_view'),
    url(r'^get-burial-popup/(\d+)/$','burial_popup'),
    url(r'^hoards/(\d+)/$','hoard_view'),
    url(r'^hoard_full/(\d+)/$','hoard_full_view'),    
    url(r'^get-metalwork-popup/(\d+)/$','metalwork_popup'),
    url(r'^miscellaneous/(\d+)/$','miscellaneous_view'),    
    url(r'^miscellaneous_full/(\d+)/$','miscellaneous_full_view'),        
    url(r'^get-miscellaneous-popup/(\d+)/$','miscellaneous_popup'),    
    url(r'^stelae/(\d+)/$','stelae_view'),
    url(r'^stelae_full/(\d+)/$','stelae_full_view'),
    url(r'^get-stelae-popup/(\d+)/$','stelae_popup'),
    url(r'^ogamsite/(\d+)/$','ogam_view'),
    url(r'^ogamsite_full/(\d+)/$','ogam_full_view'),# Actually inscriptions!
    url(r'^get-ogam-popup/(\d+)/$','ogam_popup'),
    url(r'^get-inscriptions-popup/(\d+)/$','ogam_popup'),
    url(r'^get-individuals-popup/(\d+)/$','individuals_popup'),
    url(r'^get-pots-popup/(\d+)/$','pots_popup'),    
    url(r'^get-gravegoods-popup/(\d+)/$','gravegoods_popup'),     
    url(r'^individuals/(\d+)/$','individuals_view'),
    url(r'^individual_full/(\d+)/$','individuals_full_view'),
    url(r'^burialindividuals/(\d+)/$','individuals_view'),
    url(r'^geojson_layers/$', 'geojson_layers'),
    url(r'^get-toponyms-popup/(\d+)/$','toponyms_popup'),
    url(r'^toponym_full/(\d+)/$','toponyms_full_view'),    #
    url(r'^get-settlements-popup/(\d+)/$','settlements_popup'),
    url(r'^settlements_full/(\d+)/$','settlements_full_view'),   #
    url(r'^metallurgy_geojson/$', 'metallury_geojson'),    
) 
