from django.conf.urls import *
from django import forms
from haystack.forms import FacetedSearchForm,SearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView,SearchView
from haystack.inputs import AutoQuery, Exact, Clean

from django.template import RequestContext
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse,HttpResponseRedirect

from django.contrib.gis.geos import GEOSGeometry

from aema_db.models import *
from aema_db.auxilliaryModels import *
from early_celtic_society.models import Core
import datetime
# from . import settings
from django.conf import settings


burial_facets = ['burials_individual_burial_type',\
                 'burials_general_site_type','burials_site_type','burials_age','burials_burial_type',\
                 'burials_individuals_gender','burials_individual_orientation',\
                 'burials_individual_position','burials_grave_good_type','burials_pot_types',\
                 'burials_pot_condition','burials_site_usage','burials_head_position','burials_pot_position',\
                 'burials_head_direction','burials_pot_types_major','burials_grave_good_material','burials_general_chronology']
hoard_facets = ['hoards_general_object_type','hoards_period_summary','hoards_object_count',\
                'hoards_specific_object_type','hoards_context','hoards_context_type','hoards_material',\
                'hoards_object_condition','hoards_find_type']
metalwork_facets = ['metalwork_general_object_type','metalwork_period_summary','metalwork_object_count',\
                'metalwork_specific_object_type','metalwork_context','metalwork_context_type','metalwork_material',\
                'metalwork_object_condition','metalwork_find_type']
miscellaneous_facets = ['miscellaneous_general_object_type','miscellaneous_period_summary','miscellaneous_object_count',\
                'miscellaneous_specific_object_type','miscellaneous_context','miscellaneous_context_type','miscellaneous_material',\
                'miscellaneous_object_condition','miscellaneous_find_type']                
stelae_facets = ['stelae_region','stelae_stone_shape','stelae_rock','stelae_technique','stelae_motif',\
                 'stelae_type','stelae_land_type','stelae_location','stelae_chronology']
ogam_facets = ['ogam_script','ogam_micro_context','ogam_macro_context','ogam_language','ogam_etymology']
individuals_facets = ['individuals_gender','individuals_head_position','individuals_burial_type',\
                'individuals_age', 'individuals_head_position' ,'individuals_orientation',\
                'individuals_position', 'individuals_usage', 'individuals_grave_good_type','individuals_pot_type',\
                'individuals_chronology','individuals_site_type','individuals_grave_type','individuals_grave_good_material']
pots_facets = ['pots_position','pots_type','pots_placement',\
    'pots_burial_site_type','pots_burial_type','pots_burial_position','pots_burial_orientation',\
    'pots_burial_head_position','pots_burial_gender','pots_burial_individual_age','pots_associated_gravegoods_type',\
    'pots_position','pots_associated_gravegoods_material']
gravegoods_facets = ['gravegoods_placement','gravegoods_type','gravegoods_material',\
    'gravegoods_burial_type','gravegoods_burial_site_type','gravegoods_burial_position','gravegoods_burial_orientation',\
    'gravegoods_burial_head_position','gravegoods_burial_gender','gravegoods_burial_individual_age']
    
inscriptions_facets = ['inscriptions_script','inscriptions_micro_context','inscriptions_macro_context','inscriptions_etymology',\
        'inscriptions_language_of_inscription','inscriptions_language_of_name',]
toponyms_facets = ['toponyms_language','toponyms_element','toponyms_english_definition']
settlements_facets = ['settlements_settlement_type','settlements_funerary_type','settlements_others_type','settlements_period']
#facet_groups = {Burials:burial_facets,Hoards:hoard_facets,Stelae:stelae_facets,OgamSite:ogam_facets}
facet_groups = {Burials:burial_facets,Hoards:metalwork_facets,Stelae:stelae_facets,OgamSite:inscriptions_facets,BurialIndividuals:individuals_facets,\
                 Toponyms:toponyms_facets,Core:settlements_facets,Pot:pots_facets,GraveGood:gravegoods_facets,Miscellaneous:miscellaneous_facets}


object_type_for_sqs = {'burials':Burials,'hoards':Hoards,'stelae':Stelae,'ogam':OgamSite,'metalwork':Hoards,'inscriptions':OgamSite,\
                       'settlements':Core,'individuals':BurialIndividuals,'toponyms':Toponyms,'pots':Pot,'gravegoods':GraveGood,'miscellaneous':Miscellaneous}


class CustomSearchForm(FacetedSearchForm):

    def __init__(self, *args, **kwargs):
        self.selected_filters = kwargs.pop("selected_filters", [])
        self.deselected_filters = kwargs.pop("deselected_filters", [])
        self.query_type = kwargs.pop("query_type",'')
        self.date_range = kwargs.pop("date_range",'')		
        self.mime_type = kwargs.pop("mime_type",'')
        self.query_store = kwargs.pop("query_store",'')
        self.polygon = kwargs.pop("polygon",'')
        self.models = kwargs.pop("models",[])        
        super(CustomSearchForm, self).__init__(*args, **kwargs)


    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        sqs = SearchQuerySet()
        if self.models:
            for m in self.models:
                qmodel = object_type_for_sqs.get( m )
                sqs = sqs.models( qmodel )
        else:
            sqs = SearchQuerySet()
        return sqs.auto_query(self.cleaned_data.get('q') )

    def no_query_found(self):
        #NB Moving the sqs to gather results ONLY if a facet has been selected...
        #sqs = SearchQuerySet().all()
        #If there is no query string we want to filter based on selected facet(s) only...		
        ###
        # Use facets to narrow..! NB THIS amounts to an AND query... I think...

        if self.selected_facets or self.deselected_filters or self.selected_filters or self.date_range:
            model = self.query_type
            # AHGG hacky alert!
            if model == None:
                model = 'burials' #Stick any old crap in here, it'll work
            sqs = SearchQuerySet().models(object_type_for_sqs.get(model)) #.all()

            if self.polygon:
                #ret = []
                polygon = GEOSGeometry(self.polygon.replace('%20',' '))
                polygon.srid = 4326
                sqs = sqs.within('location',Point(polygon.extent[0],polygon.extent[1]),Point(polygon.extent[2],polygon.extent[3]))
                # This maybe too slow to implement porperly...
                # This is the SECOND time we analyse by polygon - 1st BB then true intersect...
                #for s in sqs:
                #    if s.object.point:
                #        if polygon.disjoint(s.object.point):
                #            sqs = sqs.exclude(spatial_exclude=s.spatial_exclude)

            if self.selected_facets:
                for facet in self.selected_facets:
                    if ":" not in facet:
                        continue
                    field,value = facet.split(":",1)
                    if value:
                        value = value.replace('%20',' ')
                        #sqs = sqs.narrow(u'%s_exact:"%s"' % (field,sqs.query.clean(value)))
                        sqs = sqs.filter_or(**{f'{field}_exact': Exact(sqs.query.clean(value))})

                #return sqs # Don't return here cos we want to process the filters as well as the facets

            # And filters to filter..!
                # print('Narrowed: ' + str(sqs.count()))

            if self.selected_filters:
                for filter in self.selected_filters:
                    if ":" not in filter:
                        continue
                    field, value = filter.split(":",1)
                    if value:
                        value = value.replace('%20',' ')
                        sqs = sqs.filter(**{f'{field}_exact': Exact(sqs.query.clean(value))})

            # And filters to exclude..!
            if self.deselected_filters:
                for filter in self.deselected_filters:
                    if ":" not in filter:
                        continue
                    field,value = filter.split(":",1)
                    if value:
                        value = value.replace('%20',' ')
                        sqs = sqs.exclude(**{f'{field}_exact': Exact(sqs.query.clean(value))})

            if self.date_range:
                # Parse the dates to to and from values:
                start_date = int(self.date_range.split('-')[0])
                end_date = int(self.date_range.split('-')[1])
                sqs = sqs.filter(date_from__gte=datetime.date(start_date,1,1)).filter(date_to__lte=datetime.date(end_date,1,1))

            sqs = sqs.order_by('site_name_sort_exact',)

            return sqs
        
        # Otherwise return the entire set
        else:
            #return sqs.all()
            return SearchQuerySet().none()


class CustomSearchView(FacetedSearchView):

    def __init__(self, *args, **kwargs):
        # Needed to switch out the default form class.
        if kwargs.get('form_class') is None:
            kwargs['form_class'] = CustomSearchForm
        super(CustomSearchView, self).__init__(*args, **kwargs)

    def extra_context(self):
        extra = super(CustomSearchView, self).extra_context()
        extra['selected_filters'] = self.request.GET.getlist("selected_filters")
        extra['deselected_filters'] = self.request.GET.getlist("deselected_filters")
        extra['selected_facets'] = self.request.GET.getlist("selected_facets")
        extra['date_range'] = self.request.GET.get("date_range")         		
        extra['query_type'] = self.request.GET.get("query_type")
        extra['query_store'] = self.request.GET.get("query_store")
        extra['polygon'] =  self.request.GET.get("polygon")		
        model = object_type_for_sqs.get(self.request.GET.get("query_type"))
        # AHGG hacky alert!

        if model == None:
            model = object_type_for_sqs.get('burials') #Stick any old crap in here, it'll work
        if self.results.count() == 0:
            #TO DO - Replace this facet string with a constant from somewhere else that is called based on the model being faceted ???
            sqs = SearchQuerySet().models(model)
            for facet in facet_groups.get(model):
                sqs = sqs.facet(facet)  
            extra['facets'] = sqs.facet_counts()
        else:
            sqs = self.results
            for facet in facet_groups.get(model):
                sqs = sqs.facet(facet)
            extra['facets'] = sqs.facet_counts()
        return extra

    def build_form(self, form_kwargs=None):
        if form_kwargs is None:
            form_kwargs = {}
        # This way the form can always receive a list containing zero or more
        # facet expressions:
        # form_kwargs['selected_facets'] = self.request.GET.getlist("selected_facets")
        form_kwargs['selected_filters'] = self.request.GET.getlist("selected_filters")
        form_kwargs['deselected_filters'] = self.request.GET.getlist("deselected_filters")
        form_kwargs['query_type'] = self.request.GET.get("query_type")
        form_kwargs['date_range'] = self.request.GET.get("date_range")
        form_kwargs['query_store'] = self.request.GET.get("query_store")
        form_kwargs['polygon'] =  self.request.GET.get("polygon")
        # Here adding an optionl format param which should be used to influence the mimetype 
        # in the create_repsonse below...
        form_kwargs['mime_type'] = self.request.GET.get("mime_type")		
        return super(CustomSearchView, self).build_form(form_kwargs)
        kwargs = {
            'load_all': self.load_all,
        }

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        (paginator, page) = self.build_page()
        print(self.request.GET.get("query_type"))		
        context = {
            'query': self.query,
            'form': self.form,
            'query_category': self.request.GET.get("query_type"),
            'page': page,
            'paginator': paginator,
            'suggestion': None,
        }
        #Get the mime type only if requested
        mime_type = self.request.GET.get("mime_type")
        if getattr(settings, 'HAYSTACK_INCLUDE_SPELLING', False):
            context['suggestion'] = self.form.get_suggestion()
        context.update(self.extra_context())

        return render(self.request, self.template, context, content_type=mime_type)


class CustomTextSearchView(SearchView):
    def __init__(self, *args, **kwargs):
        # Needed to switch out the default form class.
        #if kwargs.get('form_class') is None:
            #kwargs['models'] = self.request.GET.get("models")        
        kwargs['form_class'] = CustomSearchForm
        super(CustomTextSearchView, self).__init__(*args, **kwargs)
    def build_form(self, form_kwargs=None):
        if form_kwargs is None:
            form_kwargs = {}
        # This way the form can always receive a list containing zero or more
        # facet expressions:
        # form_kwargs['selected_facets'] = self.request.GET.getlist("selected_facets")
        form_kwargs['selected_filters'] = self.request.GET.getlist("selected_filters")
        form_kwargs['deselected_filters'] = self.request.GET.getlist("deselected_filters")
        form_kwargs['query_type'] = self.request.GET.get("query_type")
        form_kwargs['date_range'] = self.request.GET.get("date_range")
        form_kwargs['query_store'] = self.request.GET.get("query_store")
        form_kwargs['polygon'] =  self.request.GET.get("polygon")
        form_kwargs['models'] =  self.request.GET.getlist("models")        
        # Here adding an optionl format param which should be used to influence the mimetype 
        # in the create_repsonse below...
        form_kwargs['mime_type'] = self.request.GET.get("mime_type")		
        return super(CustomTextSearchView, self).build_form(form_kwargs)
        kwargs = {
            'load_all': self.load_all,
        }        
    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        (paginator, page) = self.build_page()
        context = {
            'query': self.query,
            'form': self.form,
            #'model' : self.request.GET.get("models"),  
            'query_type': 'text',
            'query_category': self.request.GET.get("textsearchmodel",""),
            'page': page,
            'paginator': paginator,
            'suggestion': None,
        }
        #Get the mime type only if requested
        mime_type = self.request.GET.get("mime_type")
        if getattr(settings, 'HAYSTACK_INCLUDE_SPELLING', False):
            context['suggestion'] = self.form.get_suggestion()
        context.update(self.extra_context())

        return render(self.request, self.template, context, content_type=mime_type)

urlpatterns = patterns('',
    url(r'^facet/$', CustomSearchView(template='search/search_facet_list.html',\
       form_class=CustomSearchForm,results_per_page=100000), name='haystack_search'),
   
    url(r'^facet-refresh/$', CustomSearchView(template='search/search_facet_list.html',\
       form_class=CustomSearchForm,results_per_page=100000), name='haystack_search'),

    url(r'^refine/$', CustomSearchView(template='search/search_results_individual_search.html',\
       form_class=CustomSearchForm,results_per_page=15), name='haystack_search'),
   
    url(r'^map/$', CustomSearchView(template='search/search_map_results.js',\
       form_class=CustomSearchForm,results_per_page=100000), name='haystack_search'),

    url(r'^csv/$', CustomSearchView(template='search/search_csv.txt',\
       form_class=CustomSearchForm,results_per_page=100000), name='haystack_search'),

    url(r'^$', CustomSearchView(template='search/search_form.html',\
       form_class=CustomSearchForm,results_per_page=100000), name='haystack_search'),
	   
    url(r'^text/map/$', CustomTextSearchView(template='search/search_map_text_results.js',\
       form_class=SearchForm,results_per_page=10000), name='haystack_search'),	   
	   
    url(r'^text/$', CustomTextSearchView(template='search/search_results_individual_search.html',\
       form_class=SearchForm,results_per_page=15), name='haystack_search'),

)

