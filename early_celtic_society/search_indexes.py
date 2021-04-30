from haystack import indexes
from early_celtic_society.models import *
from django.contrib.gis.geos import GEOSGeometry,Point



class SettlementsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    settlements_settlement_type = indexes.MultiValueField(indexed=True,faceted=True)
    settlements_funerary_type = indexes.MultiValueField(indexed=True,faceted=True)
    settlements_others_type = indexes.MultiValueField(indexed=True,faceted=True)     
    location = indexes.LocationField(model_attr='get_location')
    settlements_period = indexes.CharField(indexed=True,faceted=True)
   

    def get_model(self):
        return Core

    def index_queryset(self,using=None):
        return Core.objects.all()

    def prepare_settlements_settlement_type(self,obj):
        ret = []
        for t in obj.type_m2m.all():
            if t.sub_type and t.sub_type.description == 'Settlement':
                ret.append(t.description)
        return ret

    def prepare_settlements_funerary_type(self,obj):
        ret = []
        for t in obj.type_m2m.all():
            if t.sub_type and t.sub_type.description == 'Funerary':
                ret.append(t.description)
        return ret

    def prepare_settlements_others_type(self,obj):
        ret = []
        for t in obj.type_m2m.all():
            if t.sub_type and t.sub_type.description == 'Other':
                ret.append(t.description)
        return ret
        
    def prepare_settlements_period(self,obj):
        return obj.period


