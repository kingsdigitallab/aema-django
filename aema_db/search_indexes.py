from haystack import indexes
from aema_db.models import Burials,BurialIndividuals,Hoards,Stelae,OgamSite,Toponyms,Miscellaneous
###
from aema_db.auxilliaryModels import *
from django.contrib.gis.geos import GEOSGeometry,Point
from aema_db.choices import *


class BurialsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    non_facet_pot_type = indexes.CharField()
    non_facet_burial_detail = indexes.CharField()	
    non_facet_gravegood = indexes.CharField()
    non_facet_biblio = indexes.CharField(model_attr='biblio_for_site',null=True)
    non_facet_funerary_context = indexes.CharField(model_attr='funerary_context',null=True)
    burials_min_no_individuals = indexes.CharField(faceted=True)	
    burials_individuals_gender = indexes.MultiValueField(faceted=True)
    burials_general_site_type = indexes.MultiValueField(faceted=True)	
    burials_site_type = indexes.MultiValueField(faceted=True)
    burials_age = indexes.MultiValueField(faceted=True)
    burials_individual_burial_type = indexes.MultiValueField(faceted=True)
    burials_individual_orientation = indexes.MultiValueField(faceted=True)
    burials_individual_position = indexes.MultiValueField(faceted=True)
    burials_grave_good_type = indexes.MultiValueField(faceted=True)
    burials_pot_types = indexes.MultiValueField(faceted=True)
    burials_pot_types_major = indexes.MultiValueField(faceted=True)
    burials_pot_condition = indexes.MultiValueField(faceted=True)
    burials_site_usage = indexes.CharField(faceted=True)
    burials_burial_type = indexes.CharField(faceted=True)		
    burials_general_chronology = indexes.CharField(faceted=True)	
    burials_pot_position = indexes.MultiValueField(faceted=True)
    burials_head_direction = indexes.MultiValueField(faceted=True)
    burials_head_position = indexes.MultiValueField(faceted=True)
    burials_grave_good_material = indexes.MultiValueField(faceted=True)
    location = indexes.LocationField(model_attr='get_location')
    site_name = indexes.CharField()
    site_name_sort = indexes.CharField(indexed=True,faceted=True)
    spatial_exclude = indexes.CharField()

    def prepare_burials_min_no_individuals(self,obj):
        if obj.minimum_no_individuals:
            return obj.minimum_no_individuals.__str__()
        else:
            return 'Not recorded'


    def prepare_site_name_sort(self,obj):
        try:
            return obj.site_fk.site_name
        except Exception:
            return 'Unspecified'

    def prepare_burials_burial_type(self,obj):
        return obj.get_burial_type_display()
			
    def prepare_spatial_exclude(self,obj):
        return 'burial' + str( obj.id )

    def prepare_non_facet_pot_type(self,obj):
        ret = ''
        for b in obj.Burial.all():
            ret = ret + b.description
        return ret

    def prepare_non_facet_burial_detail(self,obj):
        ret = ''
        for b in obj.burialindividuals_set.all():
            if b.location_in_grave:
                ret = ret + b.location_in_grave
        return ret
		
    def prepare_non_facet_gravegood(self,obj):
        ret = ''
        for b in obj.gravegood_set.all():
            if b.description:
                ret = ret + b.description
        return ret
		
    def prepare_site_name(self,obj):
        try:
            return obj.site_fk.site_name
        except Exception:
            return 'Unspecified'

    def prepare_burials_pot_types_major(self,obj):
        ret = []
        for pot in obj.Burial.all():
            if pot.pot_type_fk:
                if pot.pot_type_fk.major_type:
                    if pot.pot_type_fk.major_type.description not in ret: 
                        ret.append(pot.pot_type_fk.major_type.description)
        return ret        


    def prepare_burials_burial_type(self,obj):
        try:
            return obj.get_burial_type_display()
        except Exception:
            return 'Undefined'


    def get_model(self):
        return Burials

    def prepare_burials_head_position(self,obj):
        ret = []
        for ind in obj.burialindividuals_set.all():
            try:
                hp = ind.head_position
                for choice in burial_direction_choices:
                    if choice[0] == hp:
                        if choice[1] not in ret:
                            ret.append(choice[1])
            except Exception:
                return ['Unspecified']
        return ret

    def prepare_burials_head_direction(self,obj):
        ret = []
        for ind in obj.burialindividuals_set.all():
            try:
                hd = ind.head_direction
                for choice in burial_direction_choices:
                    if choice[0] == hd:
                        if choice[1] not in ret:
                            ret.append(choice[1])
            except Exception:
                return ['Unspecified']
        return ret


    def prepare_burials_site_usage(self,obj):
        try:
            use = obj.usage
            for choice in burial_use_period_choice:
                if choice[0] == use:
                    return choice[1]
        except Exception:
            return 'Unspecified'

    def prepare_burials_pot_condition(self,obj):
        ret = []
        for pot in obj.Burial.all():
            for c in burial_pot_condition_choices:
                if c[0] == pot.condition:
                    if c[1] not in ret:
                        ret.append(c[1])
        return ret

    def prepare_burials_pot_position(self,obj):
        ret = []
        for pot in obj.Burial.all():
            if pot.get_pot_disposition_display() not in ret:
                ret.append( pot.get_pot_disposition_display() )
        return ret

    def prepare_burials_pot_types(self,obj):
        ret = []
        for pot in obj.Burial.all():
            if pot.pot_type_fk:
                if pot.pot_type_fk.description not in ret:
                    ret.append(pot.pot_type_fk.description)
        return ret   

    def prepare_burials_grave_good_type(self,obj):
        ret =[]
        for gravegood in obj.gravegood_set.all():
            if gravegood.functional_type_fk.description not in ret:
                ret.append(gravegood.functional_type_fk.description)
        return ret      


    def prepare_burials_grave_good_material(self,obj):
        ret =[]
        for gravegood in obj.gravegood_set.all():
            if gravegood.raw_materials_m2m.all():
                for material in gravegood.raw_materials_m2m.all():
                    if material.description not in ret:
                        ret.append(material.description)
        return ret

  

    def prepare_burials_individual_position(self,obj):
        ret =[]
        for burialindividual in obj.burialindividuals_set.all():
            if burialindividual.position_fk:
                if burialindividual.position_fk.description not in ret:
                    ret.append(burialindividual.position_fk.description)
            #for c in burial_position_choices:
            #    if c[0] == burialindividual.position:
            #        if c[1] not in ret:
            #            ret.append(c[1])
        return ret

    def prepare_burials_individual_orientation(self,obj):
        ret =[]
        for burialindividual in obj.burialindividuals_set.all():
            for c in burial_orientation_choices:
                if c[0] == burialindividual.orientation:
                    if c[1] not in ret:
                        ret.append(c[1])
        return ret

    def prepare_burials_individual_burial_type (self,obj):
        ret = []
        for burialindividual in obj.burialindividuals_set.all():
            for c in burial_type_choices:
                if c[0] == burialindividual.burial_type:
                    if c[1] not in ret:
                        ret.append(c[1])
        return ret


    def prepare_burials_general_chronology(self,obj):
        if obj.general_chronology_fk:
            return obj.general_chronology_fk.description

    def prepare_burials_general_site_type(self,obj):
        ret = []
        for specsitetype in obj.site_type_m2m.all():
            ret.append(specsitetype.site_type)
        return ret

    def prepare_burials_individuals_gender(self, obj):
        # Need to remove duplcate values here
        ret = []
        for burialindividual in obj.burialindividuals_set.all():
            #if burialindividual.get_gender_display() not in ret:
                ret.append(burialindividual.get_gender_display())
        return ret
        #return [burialindividual.get_gender_display() for burialindividual in obj.burialindividuals_set.all()]
    
    def prepare_burials_site_type(self,obj):
        ret = []
        for sitetype in obj.site_type_specific.all():
            if sitetype.description not in ret:
                ret.append(sitetype.description)
        return ret
        #return [sitetype for sitetype in obj.site_type_specific.all()]				

    def prepare_burials_age(self,obj):
        ret = []
        for burialindividual in obj.burialindividuals_set.all():
            #if burialindividual.get_age_display() not in ret:
                ret.append(burialindividual.get_age_display())
        return ret
        #return [burialindividual.get_age_display() for burialindividual in obj.burialindividuals_set.all()]

    def index_queryset(self,using=None):
        return Burials.objects.all()




class StelaeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    non_facet_site = indexes.CharField(model_attr='site_fk',null=True)
    non_facet_location_description = indexes.CharField(model_attr='location_description',null=True)
    non_facet_general_description = indexes.CharField(model_attr='general_description',null=True)
    non_facet_motif_overview = indexes.CharField(model_attr='motif_overview',null=True)
    non_facet_summary_of_human_figure = indexes.CharField(model_attr='summary_of_human_figure',null=True)
    non_facet_bibliography = indexes.CharField(model_attr='bibliography',null=True)	

    stelae_region = indexes.CharField(faceted=True)
    stelae_stone_shape = indexes.MultiValueField(faceted=True)
    stelae_rock = indexes.CharField(faceted=True)
    stelae_technique = indexes.MultiValueField(faceted=True)
    #stelae_motif = indexes.MultiValueField(faceted=True)
    stelae_type = indexes.MultiValueField(faceted=True)	
    stelae_land_type = indexes.MultiValueField(faceted=True)	
    stelae_location = indexes.MultiValueField(faceted=True)			
    #stelae_human_figure = indexes.MultiValueField(faceted=True)	
    stelae_motif = indexes.MultiValueField(faceted=True)
    stelae_chronology = indexes.CharField(faceted=True)
    location = indexes.LocationField(model_attr='get_location')
	
    site_name = indexes.CharField()
    site_name_sort = indexes.CharField(faceted=True)	
    spatial_exclude = indexes.CharField()
	

    def prepare_site_name_sort(self,obj):
        try:
            return obj.site_fk.site_name
        except Exception:
            return 'Unspecified'		

    def get_model(self):
        return Stelae	

    def prepare_spatial_exclude(self,obj):
        return 'stelae' + str( obj.id )

    def prepare_stelae_chronology(self,obj):
        return obj.chronology

    def prepare_site_name(self,obj):
        try:
            return obj.site_fk.site_name
        except Exception:
            return 'Not specified'

    def prepare_stelae_type(self,obj):
        ret = []
        for t in obj.stelae_type.all():
            if t.description not in ret:
                ret.append(t.description)
        return ret     
		
    def prepare_stelae_land_type(self,obj):
        ret = []
        for t in obj.type_of_land.all():
            if t.description not in ret:
                ret.append(t.description)
        return ret

    def prepare_stelae_location(self,obj):
        ret = []
        for t in obj.location_summary.all():
            if t.description not in ret:
                ret.append(t.description)
        return ret

    #def prepare_stelae_human_figure(self,obj):
    #    ret = []
    #    for t in obj.human_figure_m2m.all():
    #        if t.description not in ret:
    #            ret.append(t.description)
    #    return ret


    #def prepare_stelae_motif(self,obj):
    #    motif_list = ['human_figure_bool','lance_spear_bool','sword_bool','shield_bool','bow_and_arrow','wheeled_vehicle_bool','quadroped_bool','mirror_bool',\
    #        'fibula_bool','comb_bool','ornaments_bool','headdress_bool','helmet_bool','circles_cup_and_rings_bool','musical_instrument_bool',\
    #        'additional_features_bool','re_use_bool']
    #    ret = []
    #    for motif in motif_list:
    #        if obj.__getattribute__(motif) == True:
    #            ret.append(motif.replace('_bool','').replace('_',' '))
    #    return ret

    def prepare_stelae_motif(self,obj):
        ret = []
        for t in obj.motif.all():
            if t.description not in ret:
                ret.append(t.description)
        return ret
		
    def prepare_stelae_technique(self,obj):
        ret = []
        for t in obj.technique_m2m.all():
            if t.description not in ret:
                ret.append(t.description)
        return ret


    def prepare_stelae_region(self,obj):
        return obj.region

    def prepare_stelae_stone_shape(self,obj):
        ret =  []
        for s in obj.stone_shape_m2m.all():
            ret.append(s.description)
        return ret

    def prepare_stelae_rock(self,obj):
        if obj.specific_stone_type:
            return obj.specific_stone_type.description
        return 'None'


    def index_queryset(self,using=None):
        return Stelae.objects.all()


### Changing hoards to metawork
class MetalworkIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    non_facet_site = indexes.CharField(model_attr='site_fk',null=True)
    non_facet_deposit_overview = indexes.CharField(model_attr='deposit_overview',null=True)
    non_facet_deposit_context = indexes.CharField(model_attr='deposit_context',null=True)       
    non_facet_specific_object_description = indexes.CharField(model_attr='specific_object_description',null=True)
    non_facet_arrangement_of_objects = indexes.CharField(model_attr='arrangement_of_objects',null=True)
    non_facet_notes = indexes.CharField(model_attr='notes',null=True)       
    non_facet_ref = indexes.CharField(model_attr='refs',null=True)          
    metalwork_general_object_type = indexes.MultiValueField(faceted=True)
    metalwork_period_summary = indexes.CharField(faceted=True)
    metalwork_object_count = indexes.CharField(faceted=True)
    metalwork_specific_object_type = indexes.MultiValueField(faceted=True)
    metalwork_context = indexes.MultiValueField(faceted=True)
    metalwork_material = indexes.MultiValueField(faceted=True)
    metalwork_find_type = indexes.CharField(faceted=True)
    metalwork_context_type = indexes.CharField(faceted=True)
    metalwork_object_condition = indexes.CharField(faceted=True)
    site_name = indexes.CharField()
    site_name_sort = indexes.CharField(faceted=True)	
    location = indexes.LocationField(model_attr='get_location')	
    spatial_exclude = indexes.CharField()
	
    def get_model(self):
        return Hoards

    def prepare_spatial_exclude(self,obj):
        return 'hoard' + str( obj.id )

		
    def prepare_site_name_sort(self,obj):
        try:
            return obj.site_fk.site_name
        except Exception:
            return 'Unspecified'				

    def prepare_metalwork_object_condition(self,obj):
        return obj.get_object_condition_summary_choice_display()


    def prepare_site_name(self,obj):
        try:
            return obj.site_fk.site_name
        except Exception:
            return 'Not specified'

    def prepare_metalwork_context_type(self,obj):
        return obj.get_dry_wet_context_choice_display()

    def prepare_metalwork_find_type(self,obj):
        return obj.get_find_type_cleaned_display()

    def prepare_metalwork_material(self,obj):
        ret = []
        for mat in obj.material_type_fk.all():
            if mat.description not in ret:
                ret.append(mat.description)
        return ret

    def prepare_metalwork_context(self,obj):
        ret = []
        for con in obj.context_summary_m2m.all():
            if con.description not in ret:
                ret.append(con.description)
        return ret

    def prepare_metalwork_specific_object_type(self,obj):
        ret = []
        for type in obj.specific_object_type_m2m.all():
            if type.description not in ret:
                ret.append(type.description)
        return ret

    def prepare_metalwork_general_object_type(self,obj):
        ret = []
        for general_type in obj.general_type_m2m.all():
            if general_type.description not in ret:
                ret.append(general_type.description)
        return ret
   
    def prepare_metalwork_object_count(self,obj):
        n = obj.no_of_objects_clustered_choice
        for c in hoard_object_count:
            if c[0] == n:
                return c[1]

    def prepare_metalwork_period_summary(self,obj):
        if obj.period_summary_fk:	
            return obj.period_summary_fk.description
        return 'Undefined'

    def index_queryset(self,using=None):
        return Hoards.objects.all().order_by('no_of_objects_cleaned')

#ChangingOgam to inscriptions

class InscriptionsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)
    non_facet_site = indexes.CharField(model_attr='site_fk',null=True)
    inscriptions_script = indexes.MultiValueField(faceted=True)
    inscriptions_morphology = indexes.MultiValueField(faceted=True)
    inscriptions_micro_context = indexes.CharField(faceted=True)
    inscriptions_macro_context = indexes.CharField(faceted=True)
    #inscriptions_language = indexes.CharField(faceted=True)
    inscriptions_language_of_name = indexes.MultiValueField(faceted=True)    
    inscriptions_language_of_inscription = indexes.MultiValueField(faceted=True)        
    inscriptions_etymology = indexes.MultiValueField(faceted=True)
    site_name = indexes.CharField()
    site_name_sort = indexes.CharField(faceted=True)	
    location = indexes.LocationField(model_attr='get_location')	
    spatial_exclude = indexes.CharField()

    def prepare_spatial_exclude(self,obj):
        return 'ogam' + str( obj.id )

    def prepare_site_name(self,obj):
        try:
            return obj.site_fk.site_name
        except Exception:
            return 'Unspecified'

    def get_model(self):
        return OgamSite
        
    def prepare_inscriptions_language_of_name(self,obj):
        ret = []
        for i in obj.ogaminscription_set.all():
            if i.language_fk:
                if i.language_fk not in ret:
                    ret.append(i.language_fk.description)
        return ret
        
    def prepare_inscriptions_language_of_inscription(self,obj):
        ret = []
        for i in obj.ogaminscription_set.all():
            if i.language_of_inscription:
                if i.language_of_inscription not in ret:
                    ret.append(i.language_of_inscription.description)
        return ret        

    def prepare_inscriptions_etymology(self,obj):
        ret = []
        for i in obj.ogaminscription_set.all():
            if i.etymology_fk:
                if i.get_etymology_fk_display() not in ret:
                    ret.append(i.get_etymology_fk_display())
        return ret

    def prepare_site_name_sort(self,obj):
        try:
            return obj.site_fk.site_name
        except Exception:
            return 'Unspecified'		

    def prepare_inscriptions_language(self,obj):
        try:
            return obj.language_fk
        except Exception:
            return 'Undefined'

    def prepare_inscriptions_macro_context(self,obj):
        try:
            return obj.get_context_macro_display()
        except Exception:
            return 'Undefined'

    def prepare_inscriptions_micro_context(self,obj):
        try:
            return obj.get_context_micro_display()
        except Exception:
            return 'Undefined'

    def prepare_inscriptions_morphology(self,obj):
        ret = []
        for i in obj.ogaminscription_set.all():
            if i.morphology not in ret:
                ret.append(i.morphology)
        return ret
  

    def prepare_inscriptions_script(self,obj):
        ret = []
        if obj.ogaminscription_set.all().__len__() > 0:
            for o in obj.ogaminscription_set.all():
                try:			
                    if o.script_fk.description not in ret:
                        ret.append(o.script_fk.description)
                except Exception:
                    ret.append('Not defined')				
        return ret


    def index_queryset(self,using=None):
        return OgamSite.objects.all()
		
class IndividualsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)
    site_name = indexes.CharField()
    site_name_sort = indexes.CharField(faceted=True)	
    location = indexes.LocationField(model_attr='get_location')	
    individuals_grave_good_type = indexes.MultiValueField(faceted=True)
    individuals_pot_type  = indexes.MultiValueField(faceted=True)
    non_facet_pot_type = indexes.CharField()
    individuals_gender = indexes.CharField(faceted=True)
    individuals_gender = indexes.CharField(faceted=True)
    individuals_age = indexes.CharField(faceted=True)
    individuals_burial_type = indexes.CharField(faceted=True)
    individuals_head_direction = indexes.CharField(faceted=True)
    individuals_head_position = indexes.CharField(faceted=True)
    individuals_orientation = indexes.CharField(faceted=True)
    individuals_position = indexes.CharField(faceted=True)
    individuals_usage = indexes.CharField(faceted=True)
    individuals_chronology = indexes.CharField(faceted=True)
    individuals_grave_type = indexes.CharField(faceted=True)
    individuals_site_type  = indexes.MultiValueField(faceted=True)
    individuals_grave_good_material = indexes.MultiValueField(faceted=True)
    


    def prepare_individuals_grave_good_type(self,obj):
        ret = []
        for g in obj.grave_good_m2m.all():
            if g.functional_type_fk.description not in ret:
                ret.append(g.functional_type_fk.description)
        return ret


    def prepare_individuals_grave_good_material(self,obj):
        ret =[]
        for gravegood in obj.grave_good_m2m.all():
            if gravegood.raw_materials_m2m.all():
                for material in gravegood.raw_materials_m2m.all():
                    if material.description not in ret:
                        ret.append(material.description)
        return ret


    def prepare_individuals_grave_type(self,obj):
        if obj.site_type:
            return obj.site_type.description
        else:
            return ''
        #return [sitetype for sitetype in obj.site_type_specific.all()]	

    #def prepare_individuals_site_type(self,obj):
    #    ret = []
    #    for specsitetype in obj.burial.site_type_m2m.all():
    #        ret.append(specsitetype.site_type)
    #    return ret


    def prepare_individuals_site_type(self,obj):
        ret = []
        for sitetype in obj.burial.site_type_specific.all():
            if sitetype.description not in ret:
                ret.append(sitetype.description)
        return ret

    def prepare_individuals_chronology(self,obj):
        if obj.general_chronology_fk:
            return obj.general_chronology_fk.description
        else:
            return obj.general_chronology

    def prepare_individuals_gender(self,obj):
        return obj.get_gender_display()

    def prepare_individuals_age(self,obj):
        return obj.get_age_display()

    def prepare_individuals_burial_type(self,obj):
        return obj.get_burial_type_display()

    def prepare_individuals_head_direction(self,obj):
        return obj.get_head_direction_display()

    def prepare_individuals_head_position(self,obj):
        return obj.get_head_position_display()

    def prepare_individuals_orientation(self,obj):
        return obj.get_orientation_display()

    def prepare_individuals_position(self,obj):
        if obj.position_fk:
            return obj.position_fk.description
        else:
            return ''

    def prepare_individuals_pot_type(self,obj):
        ret = []
        for p in obj.pot_m2m.all():
            if p.pot_type_fk:
                ret.append(p.pot_type_fk.description)
        return ret


    def prepare_non_facet_pot_type(self,obj):
        ret = ''
        for b in obj.pot_m2m.all():
            ret = ret + b.description
        return ret


    def prepare_individuals_usage(self,obj):
        return obj.get_usage_display()

    def prepare_individuals_grave_good_type(self,obj):
        ret = []
        for g in obj.grave_good_m2m.all():
            if g.functional_type_fk.description not in ret:
                ret.append(g.functional_type_fk.description)
        return ret

    def prepare_site_name(self,obj):
        try:
            return obj.burial.site_fk.site_name
        except Exception:
            return 'Undefined'

    def prepare_site_name_sort(self,obj):
        try:
            return obj.burial.site_fk.site_name
        except Exception:
            return 'Undefined'

    def get_model(self):
        return BurialIndividuals	

    def index_queryset(self,using=None):
        return BurialIndividuals.objects.all()	



class ToponymsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    toponyms_language = indexes.CharField(faceted=True)
    toponyms_element = indexes.MultiValueField(faceted=True)
    toponyms_english_definition = indexes.MultiValueField(faceted=True)
    location = indexes.LocationField(model_attr='get_location')

    def prepare_toponyms_english_definition(self,obj):
        ret = []
        if obj.cognate:
            for r in obj.cognate.split(','):
                ret.append( r.strip() )
        return ret

    def prepare_toponyms_language(self,obj):
        return obj.language

    def prepare_toponyms_element(self,obj):
        ret = []
        if obj.briga:
            if obj.briga.__contains__('X'):
                ret.append('Briga')
        if obj.dunon:
            if obj.dunon.__contains__('X'):
                ret.append('Dunon')
        if obj.duron:
            if obj.duron.__contains__('X'):
                ret.append('Duron')
        if obj.ebur:
            if obj.ebur.__contains__('X'):
                ret.append('Ebur')
        if obj.magos:
            if obj.magos.__contains__('X'):
                ret.append('Magos')
        if obj.nemeton:
            if obj.nemeton.__contains__('X'):
                ret.append('Nemeton')
        if obj.novios:
            if obj.novios.__contains__('X'):
                ret.append('Novios')
        if obj.sego_field:
            if obj.sego_field.__contains__('X'):
                ret.append('Sego')
        return ret


    def get_model(self):
        return Toponyms

    def index_queryset(self,using=None):
        return Toponyms.objects.all()



# Burial Type, Position, Orientation, Head Position, Gender, Age

class PotsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pots_position = indexes.CharField(faceted=True)
    pots_type = indexes.CharField(faceted=True)
    pots_placement = indexes.CharField(faceted=True)
    pots_condition = indexes.CharField(faceted=True)    
    pots_burial_site_type = indexes.MultiValueField(faceted=True)
    pots_burial_type = indexes.MultiValueField(faceted=True)    
    pots_burial_position = indexes.MultiValueField(faceted=True)
    pots_burial_orientation = indexes.MultiValueField(faceted=True)
    pots_burial_head_position = indexes.MultiValueField(faceted=True)
    pots_burial_gender = indexes.MultiValueField(faceted=True)
    pots_burial_individual_age = indexes.MultiValueField(faceted=True)
    pots_associated_gravegoods_type = indexes.MultiValueField(faceted=True)        
    pots_associated_gravegoods_material = indexes.MultiValueField(faceted=True)
    pots_description = indexes.CharField(model_attr='description')            
    location = indexes.LocationField(model_attr='get_location')

    #location = indexes.LocationField(model_attr='get_location')
    
    def prepare_pots_condition(self,obj):
        return obj.get_condition_display()
    
    def prepare_pots_associated_gravegoods_type(self,obj):
        ret = []
        if obj.burialindividuals_set.all().__len__() > 0:
            for i in obj.burialindividuals_set.all():
                if i.grave_good_m2m.all().__len__() > 0:
                    for g in i.grave_good_m2m.all():
                        if g.functional_type_fk:    
                            ret.append(g.functional_type_fk.description)
        return ret
        
    def prepare_pots_associated_gravegoods_material(self,obj):
        ret = []
        if obj.burialindividuals_set.all().__len__() > 0:
            for i in obj.burialindividuals_set.all():
                if i.grave_good_m2m.all().__len__() > 0:
                    for g in i.grave_good_m2m.all():
                        if g.raw_materials_m2m.all().__len__() > 0:
                            for m in g.raw_materials_m2m.all():
                                ret.append(m.description)
        return ret        

    def prepare_pots_burial_site_type(self,obj):
        ret = []
        if obj.burialindividuals_set.all().__len__() > 0:
            for i in  obj.burialindividuals_set.all():
                if i.site_type:
                    ret.append(i.site_type.description)
        return ret

    def prepare_pots_burial_type(self,obj):
        ret = []
        if obj.burialindividuals_set.all().__len__() > 0:
            for i in  obj.burialindividuals_set.all():
                if i.burial_type:
                    ret.append(i.get_burial_type_display())
        return ret

    def prepare_pots_burial_position(self,obj):
        ret = []
        if obj.burialindividuals_set.all().__len__() > 0:
            for i in  obj.burialindividuals_set.all():
                if i.position_fk:
                    ret.append(i.position_fk.description)
        return ret

    def prepare_pots_burial_orientation(self,obj):
        ret = []
        if obj.burialindividuals_set.all().__len__() > 0:
            for i in obj.burialindividuals_set.all():
                ret.append( i.get_orientation_display() )
        return ret

    def prepare_pots_burial_head_position(self,obj):
        ret = []
        if obj.burialindividuals_set.all().__len__() > 0:
            for i in  obj.burialindividuals_set.all():
                ret.append(i.get_head_position_display())
        return ret

    def prepare_pots_burial_gender(self,obj):
        ret = []
        if obj.burialindividuals_set.all().__len__() > 0:
            for i in  obj.burialindividuals_set.all():
                ret.append( i.get_gender_display() )
        return ret

    def prepare_pots_burial_individual_age(self,obj):
        ret = []
        if obj.burialindividuals_set.all().__len__() > 0:
            for i in  obj.burialindividuals_set.all():
                ret.append(i.get_age_display())
        return ret

    def prepare_pots_type(self,obj):
        if obj.pot_type_fk:
            return obj.pot_type_fk.description

    def prepare_pots_position(self,obj):
        return obj.get_pot_disposition_display()

    def prepare_pots_placement(self,obj):
        if obj.pot_placement_fk:
            return obj.pot_placement_fk.description

    def get_model(self):
        return Pot

    def index_queryset(self,using=None):
        return Pot.objects.all()

class GraveGoodsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    gravegoods_type = indexes.CharField(faceted=True)
    gravegoods_placement = indexes.CharField(faceted=True)
    gravegoods_material = indexes.MultiValueField(faceted=True)
    #gravegoods_burial_type = indexes.CharField(faceted=True)
    gravegoods_burial_site_type = indexes.MultiValueField(faceted=True)
    gravegoods_burial_type = indexes.MultiValueField(faceted=True)      
    gravegoods_burial_position = indexes.CharField(faceted=True)
    gravegoods_burial_orientation = indexes.CharField(faceted=True)
    gravegoods_burial_head_position = indexes.CharField(faceted=True)
    gravegoods_burial_gender = indexes.CharField(faceted=True)
    gravegoods_burial_individual_age = indexes.CharField(faceted=True)
    location = indexes.LocationField(model_attr='get_location')

    #location = indexes.LocationField(model_attr='get_location'

    def prepare_gravegoods_material(self,obj):
        ret = []
        if obj.raw_materials_m2m.all().__len__() > 0:
            for m in obj.raw_materials_m2m.all():
                ret.append(m.description)
        return ret

    def prepare_gravegoods_type(self,obj):
        if obj.functional_type_fk:
            return obj.functional_type_fk.description

    def prepare_gravegoods_placement(self,obj):
        if obj.placement_fk:
            return obj.placement_fk.description
            
    def prepare_gravegoods_burial_site_type(self,obj):
        ret = []
        if obj.burialindividuals_set.all().__len__() > 0:
            for i in  obj.burialindividuals_set.all():
                if i.site_type:
                    ret.append(i.site_type.description)
        return ret
        
    def prepare_gravegoods_burial_type(self,obj):
        ret = []
        if obj.burialindividuals_set.all().__len__() > 0:
            for i in  obj.burialindividuals_set.all():
                if i.burial_type:
                    ret.append(i.get_burial_type_display())
        return ret        

    def prepare_gravegoods_burial_position(self,obj):
        ret = []
        if obj.burialindividuals_set.all().__len__() > 0:
            for i in  obj.burialindividuals_set.all():
                if i.position_fk:
                    ret.append(i.position_fk.description)
        return ret

    def prepare_gravegoods_burial_orientation(self,obj):
        ret = []
        if obj.burialindividuals_set.all().__len__() > 0:
            for i in obj.burialindividuals_set.all():
                ret.append( i.get_orientation_display() )
        return ret

    def prepare_gravegoods_burial_head_position(self,obj):
        ret = []
        if obj.burialindividuals_set.all().__len__() > 0:
            for i in  obj.burialindividuals_set.all():
                ret.append(i.get_head_position_display())
        return ret

    def prepare_gravegoods_burial_gender(self,obj):
        ret = []
        if obj.burialindividuals_set.all().__len__() > 0:
            for i in  obj.burialindividuals_set.all():
                ret.append( i.get_gender_display() )
        return ret

    def prepare_gravegoods_burial_individual_age(self,obj):
        ret = []
        if obj.burialindividuals_set.all().__len__() > 0:
            for i in  obj.burialindividuals_set.all():
                ret.append(i.get_age_display())
        return ret            

    def get_model(self):
        return GraveGood

    def index_queryset(self,using=None):
        return GraveGood.objects.all()

        

### Changing hoards to metawork
class MiscellaneousIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    non_facet_site = indexes.CharField(model_attr='site_fk',null=True)
    non_facet_deposit_overview = indexes.CharField(model_attr='deposit_overview',null=True)
    non_facet_deposit_context = indexes.CharField(model_attr='deposit_context',null=True)       
    non_facet_specific_object_description = indexes.CharField(model_attr='specific_object_description',null=True)
    non_facet_arrangement_of_objects = indexes.CharField(model_attr='arrangement_of_objects',null=True)
    non_facet_notes = indexes.CharField(model_attr='notes',null=True)       
    non_facet_ref = indexes.CharField(model_attr='refs',null=True)          
    miscellaneous_general_object_type = indexes.MultiValueField(faceted=True)
    miscellaneous_period_summary = indexes.CharField(faceted=True)
    miscellaneous_object_count = indexes.CharField(faceted=True)
    miscellaneous_specific_object_type = indexes.MultiValueField(faceted=True)
    miscellaneous_context = indexes.MultiValueField(faceted=True)
    miscellaneous_material = indexes.MultiValueField(faceted=True)
    miscellaneous_find_type = indexes.CharField(faceted=True)
    miscellaneous_context_type = indexes.CharField(faceted=True)
    miscellaneous_object_condition = indexes.CharField(faceted=True)
    site_name = indexes.CharField()
    site_name_sort = indexes.CharField(faceted=True)	
    location = indexes.LocationField(model_attr='get_location')	
    spatial_exclude = indexes.CharField()
	
    def get_model(self):
        return Miscellaneous

    def prepare_spatial_exclude(self,obj):
        return 'hoard' + str( obj.id )

		
    def prepare_site_name_sort(self,obj):
        try:
            return obj.site_fk.site_name
        except Exception:
            return 'Unspecified'				

    def prepare_miscellaneous_object_condition(self,obj):
        return obj.get_object_condition_summary_choice_display()


    def prepare_site_name(self,obj):
        try:
            return obj.site_fk.site_name
        except Exception:
            return 'Not specified'

    def prepare_miscellaneous_context_type(self,obj):
        return obj.get_dry_wet_context_choice_display()

    def prepare_miscellaneous_find_type(self,obj):
        return obj.get_find_type_cleaned_display()

    def prepare_miscellaneous_material(self,obj):
        ret = []
        for mat in obj.material_type_fk.all():
            if mat.description not in ret:
                ret.append(mat.description)
        return ret

    def prepare_miscellaneous_context(self,obj):
        ret = []
        for con in obj.context_summary_m2m.all():
            if con.description not in ret:
                ret.append(con.description)
        return ret

    def prepare_miscellaneous_specific_object_type(self,obj):
        ret = []
        for type in obj.specific_object_type_m2m.all():
            if type.description not in ret:
                ret.append(type.description)
        return ret

    def prepare_miscellaneous_general_object_type(self,obj):
        ret = []
        for general_type in obj.general_type_m2m.all():
            if general_type.description not in ret:
                ret.append(general_type.description)
        return ret
   
    def prepare_miscellaneous_object_count(self,obj):
        n = obj.no_of_objects_clustered_choice
        for c in hoard_object_count:
            if c[0] == n:
                return c[1]

    def prepare_miscellaneous_period_summary(self,obj):
        if obj.period_summary_fk:	
            return obj.period_summary_fk.description
        return 'Undefined'

    def index_queryset(self,using=None):
        return Miscellaneous.objects.all()        
