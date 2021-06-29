from django.db import models

# Create your models here.

from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry,Point

from auxilliaryModels import *
from choices import *

from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from django.utils.text import normalize_newlines



def remove_newlines(text):
    """
    Removes all newline characters from a block of text.
    """
    # First normalize the newlines using Django's nifty utility
    normalized_text = normalize_newlines(text)
    # Then simply remove the newlines like so.
    return normalized_text.replace('\n', '<\br>').replace('\r','')


### Core models

class Burials(models.Model):
    """
    Burials model uploaded from Excel spreadsheet
    TO DO: 
    1. Remove non boolean fields (eg dagger etc)
    5. Drop down list for Date summary 
    7. Standardise Ages
    """ 
    # world borders shapefile.
    date_ref = models.CharField(max_length=50,null=True,blank=True)
    site = models.CharField(max_length=100,null=True,blank=True)
    # FK Inserted
    site_fk = models.ForeignKey('Site',null=True,blank=True,verbose_name='Location summary',help_text=\
        "Currently displaying ID as there needs to be some checking and rationalisation of site name records (according to the original values below)")
    area = models.CharField(max_length=100,null=True,blank=True)    
    region = models.CharField(max_length=50,null=True,blank=True)    
    country = models.CharField(max_length=50,null=True,blank=True)    
    lon = models.FloatField(null=True,blank=True)
    lat = models.FloatField(null=True,blank=True)
    organic_material = models.CharField(max_length=50,null=True,blank=True)
    organic_material_sub_type = models.CharField(max_length=50,null=True,blank=True)        
    #FK Inserted
    organic_material_fk = models.ForeignKey('OrganicMaterial',null=True,blank=True,verbose_name='Organic Material')
    site_type = models.CharField(max_length=50,null=True,blank=True)
    #M2M type inserted
    site_type_m2m = models.ManyToManyField('SiteType',verbose_name='Site type(s)')
    site_type_specific = models.ManyToManyField('SiteTypeSpecific',verbose_name='Specific site type(s)')
    cemetery =  models.NullBooleanField()
    usage = models.CharField(max_length='2',choices=burial_use_period_choice,null=True,blank=True)
    funerary_context = models.TextField(null=True,blank=True)
    burial_type = models.CharField(max_length='2',choices=burial_type_choices,null=True,blank=True)
    burial_summary = models.TextField(null=True,blank=True)
    skeleton_summary = models.TextField(null=True,blank=True)
    minimum_no_individuals = models.IntegerField(null=True,blank=True)
    date_summary = models.CharField(max_length=200,null=True,blank=True)
    coords =  models.CharField(max_length=50,null=True,blank=True) #
    no_of_grave_goods = models.IntegerField(null=True,blank=True,help_text='Redundant - to be replaced/moved')    
    gender = models.CharField(max_length=20,null=True,blank=True)
    #M2M Field added
    gender_m2m = models.ManyToManyField('Gender',verbose_name='Gender assemblage')
    age = models.CharField(max_length=20,null=True,blank=True,help_text='Redundant - to be replaced/moved')    
    pot = models.CharField(max_length=20,null=True,blank=True)
    # Bool field added    
    pot_bool = models.NullBooleanField(default=False,verbose_name="Pot")
    arrowhead = models.CharField(max_length=20,null=True,blank=True)
    # Bool field added
    arrowhead_bool = models.NullBooleanField(default=False,verbose_name="Arrowhead")
    dagger = models.CharField(max_length=20,null=True,blank=True)
    # Bool field added
    dagger_bool = models.NullBooleanField(default=False,verbose_name="Dagger")    
    wristguard = models.CharField(max_length=20,null=True,blank=True)
    # Bool field added
    wristguard_bool = models.NullBooleanField(default=False,verbose_name="Wristguard")
    flint_or_stone = models.CharField(max_length=20,null=True,blank=True)
    # Bool field added    
    flint_or_stone_bool = models.NullBooleanField(default=False,verbose_name="Flint or Stone")
    bone_object = models.CharField(max_length=20,null=True,blank=True)
    # Bool field added    
    bone_object_bool = models.NullBooleanField(default=False,verbose_name="Bone object")
    jewellery = models.CharField(max_length=20,null=True,blank=True)
    # Bool field added    
    jewellery_bool = models.NullBooleanField(default=False,verbose_name="Jewellery")
    weapons = models.CharField(max_length=20,null=True,blank=True)
    # Bool field added
    weapons_bool = models.NullBooleanField(default=False,verbose_name="Weapons")
    gold_silver = models.CharField(max_length=20,null=True,blank=True)
    # Bool field added
    gold_silver_bool = models.NullBooleanField(default=False,verbose_name="Gold and Silver")
    faience = models.CharField(max_length=20,null=True,blank=True)
    # Bool field added
    faience_bool = models.NullBooleanField(default=False,verbose_name="Faience")
    amber = models.CharField(max_length=20,null=True,blank=True)
    # Bool field added
    amber_bool = models.NullBooleanField(default=False,verbose_name="Amber")
    cu_cu_alloy = models.CharField(max_length=20,null=True,blank=True)
    # Bool field added
    cu_cu_alloy_bool = models.NullBooleanField(default=False,verbose_name="Copper/Copper alloy")
    jet_lignite_shale = models.CharField(max_length=20,null=True,blank=True)
    # Bool field added
    jet_lignite_shale_bool = models.NullBooleanField(default=False,verbose_name="Jet/Lignite/Shale")
    grave_good_short_summary = models.TextField(max_length=1000,null=True,blank=True)
    grave_good_class_m2m = models.ManyToManyField('GraveGoodClass',verbose_name='Grave good classes')
    calibrated_date_bc_2_sigma = models.CharField(max_length=50,null=True,blank=True)
    pot_type =  models.CharField(max_length=1000,null=True,blank=True)
    pot_type_summary =  models.CharField(max_length=100,null=True,blank=True)    
    uncalibrated_date_bp = models.CharField(max_length=100,null=True,blank=True)   #
    uncalibrated_date_bc = models.CharField(max_length=100,null=True,blank=True)
    calibrated_date_bc_1_sigma = models.CharField(max_length=50,null=True,blank=True)
    calibrated_date_bc_2_sigma_repeated_field = models.CharField(max_length=50,null=True,blank=True)
    general_chronology = models.CharField(max_length=50,null=True,blank=True,help_text='Redundant field - use the one below')
    general_chronology_fk = models.ForeignKey('GeneralChronology',null=True,blank=True,verbose_name='General chronology')
    biblio_for_site = models.CharField(max_length=1000,null=True,blank=True,help_text='Redundant - to be replaced/moved')

    # GeoDjango-specific: a geometry field (PointField) and
    # overriding the default manager with a GeoManager instance.
    point = models.PointField(null=True,blank=True)
    objects = models.GeoManager()
    location_approximate = models.NullBooleanField()
    local_coordinates_string = models.CharField(max_length=50,null=True,blank=True)
    local_coordinates_epsg_code = models.IntegerField(null=True,blank=True)
    # Returns the string representation of the model.
    def __unicode__(self):
        if self.site:
            if self.date_ref:
                return "%s, %s, %s" % (self.site,self.date_ref,self.id)
            else:
                return "%s, %s" % (self.site,self.id)
        else:
            return "%s" % (self.id)

    #For elastic search spatial query
    def get_location(self):
        if self.point:
            return Point(self.point.x,self.point.y)
        return Point(0,0)

    def get_geojson(self):
        string = ''
        try:
            if self.point:
                string += '[' + str(self.point.x) + ',' + str(self.point.y) + ']'
                return string
        except Exception:
            pass
            return None
    
    def cname(self):
        return self.__class__.__name__

    def haystack_name(self):
        return 'burials'

    def popup_content(self):
        str = "<table><thead>"
        if self.site_fk:
            siteName = self.site_fk.site_name
        else:
            siteName = 'Unnamed'
        str += "<tr><th colspan='2'><a target='_blank' href='/view/burials_full/" + \
            self.id.__str__() + "'>" + siteName + "</a></th></tr></thead><tbody>"
        str += "<tr><th>Site type</th><td>"
        for st in self.site_type_m2m.all():
            str += st.site_type + ', '
        #if self.site_type_m2m.all().__len__() != 1:
        #    str = str[0:-2]
        if self.site_type_specific.all().count() >0:
            str += ' ('
        for sts in self.site_type_specific.all():
            str += sts.description + ', '
        str = str[0:-2]
        if self.site_type_specific.all().count() >0:
            str += ')'        
        str += "</td></tr>"
        str += "<tr><th>General chronology</th><td>"
        if self.general_chronology_fk:
            chr = self.general_chronology_fk.description
        else:
            chr = 'Not specified'
        str += chr + "</td></tr>"
        str += "<tr><th>Usage</th><td>"
        if self.usage:
            usage = self.get_usage_display() 
        else:
            usage = 'Not specified'
        str += usage + "</td></tr>"
        str += "<tr><th>Min. individuals</th><td>"
        if self.minimum_no_individuals:
            ind = self.minimum_no_individuals.__str__() 
        else:
            ind = 'Not specified'
        str += ind + "</td></tr>"
        if self.gravegood_set.all().count() > 0:
            str += "<tr><th>Grave goods</th><td>"
            for gd in self.gravegood_set.all():
                str +=  gd.functional_type_fk.description + ', '
            str = str[0:-2]
            str += "</td></tr>"
        if self.Burial.all().count() > 0:
            str += "<tr><th>Pots</th><td>"
            for gd in self.Burial.all():
                if gd.pot_type_fk:
                    str +=  gd.pot_type_fk.description + ', '
            str = str[0:-2]
            str += "</td></tr>"            
        str += "</tbody></table>"
        #str += "<a href='#' data-reveal-id='myModal'>Click Me For A Modal</a>"
        str += "<button class='button tiny popup-extra' data-reveal-id='more-detail-modal' data-reveal-ajax='https://aemap.ac.uk/view/burials/"+ self.id.__str__() +"'>More</button>"

        return str

    class Meta:
        verbose_name_plural = 'Burial'
        ordering = ('site','date_ref')
		
    def save(self, *args, **kwargs):
        if self.lat and self.lon:
            self.point = GEOSGeometry('POINT(' + str(self.lon ) + ' ' + str(self.lat) + ')')
        elif self.point:
            p = self.point
            self.lat = p.y
            self.lon = p.x
        super(Burials, self).save(*args, **kwargs)
     
    @staticmethod
    def autocomplete_search_fields():
        return ('id_exact','site_fk__site_name__icontains')



class Stelae(models.Model):
    stelae_number = models.IntegerField(null=True,blank=True)
    site_name = models.CharField(max_length=50,null=True,blank=True)
    #FK Added
    site_fk = models.ForeignKey('Site',null=True,blank=True)
    area  = models.CharField(max_length=100,null=True,blank=True)
    region  = models.CharField(max_length=50,null=True,blank=True)
    location_description  = models.TextField(max_length=50,null=True,blank=True)
    coordinates  = models.CharField(max_length=50,null=True,blank=True)
    summary_location  = models.TextField(null=True,blank=True)
    lon  = models.FloatField(null=True,blank=True)
    lat  = models.FloatField(null=True,blank=True)
    type_of_land  = models.CharField(max_length=200,null=True,blank=True)
    dimensions_height_m  = models.FloatField(null=True,blank=True)
    dimensions_width_m  = models.FloatField(null=True,blank=True)
    dimensions_thickness_m  = models.FloatField(null=True,blank=True)
    stone_shape  = models.CharField(max_length=100,null=True,blank=True)
    #m2m
    stone_shape_m2m = models.ManyToManyField('StelaeStoneShape',blank=True)

    condition  = models.TextField(null=True,blank=True)
    technique_of_creation  = models.CharField(max_length=200,null=True,blank=True)
    technique_m2m = models.ManyToManyField('StelaeTechnique',blank=True)
    stone_type_and_description  = models.TextField(null=True,blank=True)
	#fk
    specific_stone_type = models.ForeignKey('SpecificRockType',null=True,blank=True)
    general_description  = models.TextField(null=True,blank=True)
    motif_overview  = models.TextField(null=True,blank=True)
    no_of_motifs  = models.CharField(max_length=50,null=True,blank=True)
    human_figure  = models.CharField(max_length=10,null=True,blank=True)
    human_figure_bool = models.NullBooleanField()
    summary_of_human_figure  = models.TextField(max_length=50,null=True,blank=True)
    no_of_humans  = models.IntegerField(null=True,blank=True)
    disposition_of_human_in_relation_to_other_motifs = models.TextField(max_length=50,null=True,blank=True)
    lance_spear  = models.CharField(max_length=100,null=True,blank=True)
    lance_spear_bool = models.NullBooleanField()
    spearhead_location  = models.CharField(max_length=200,null=True,blank=True)
    sword  = models.CharField(max_length=200,null=True,blank=True)
    sword_bool = models.NullBooleanField()
    sword_summary  = models.CharField(max_length=50,null=True,blank=True)
    sword_location  = models.TextField(null=True,blank=True)
    shield_summary  = models.CharField(max_length=50,null=True,blank=True)
    shield  = models.TextField(null=True,blank=True)
    shield_bool = models.NullBooleanField()
    shield_location  = models.CharField(max_length=200,null=True,blank=True)
    bow_and_arrow_bool  = models.CharField(max_length=10,null=True,blank=True)
    bow_and_arrow = models.NullBooleanField()
    bow_and_arrow_description  = models.CharField(max_length=200,null=True,blank=True)
    wheeled_vehicle  = models.CharField(max_length=10,null=True,blank=True)
    wheeled_vehicle_bool = models.NullBooleanField()
    quadropeds_animals_bool  = models.CharField(max_length=10,null=True,blank=True)
    quadroped_bool = models.NullBooleanField()
    quadroped_summary  = models.CharField(max_length=200,null=True,blank=True)
    vehicle_composition = models.TextField(null=True,blank=True)
    ornaments_accessories  = models.TextField(null=True,blank=True)
    mirror  = models.CharField(max_length=10,null=True,blank=True)
    mirror_bool = models.NullBooleanField()
    fibula  = models.CharField(max_length=10,null=True,blank=True)
    fibula_bool = models.NullBooleanField()
    comb  = models.CharField(max_length=10,null=True,blank=True)
    comb_bool = models.NullBooleanField()
    ornaments  = models.CharField(max_length=10,null=True,blank=True)
    ornaments_bool = models.NullBooleanField()
    headdress  = models.CharField(max_length=10,null=True,blank=True)
    headdress_bool = models.NullBooleanField()
    helmet  = models.CharField(max_length=10,null=True,blank=True)
    helmet_bool = models.NullBooleanField()
    helmet_type  = models.CharField(max_length=100,null=True,blank=True)
    musical_instrument  = models.CharField(max_length=50,null=True,blank=True)
    musical_instrument_bool = models.NullBooleanField()
    musical_instrument_description  = models.TextField(max_length=200,null=True,blank=True)
    circles_cup_and_rings  = models.CharField(max_length=10,null=True,blank=True)
    circles_cup_and_rings_bool = models.NullBooleanField()
    circle_etc_description  = models.TextField(null=True,blank=True)
    other_motifs  = models.TextField(max_length=50,null=True,blank=True)
    unusual_motifs  = models.TextField(max_length=50,null=True,blank=True)
    re_use  = models.CharField(max_length=100,null=True,blank=True)
    re_use_bool = models.NullBooleanField()
    additional_features  = models.CharField(max_length=100,null=True,blank=True)
    additional_features_bool = models.NullBooleanField()
    re_use_additional_features  = models.TextField(null=True,blank=True)
    other_points_of_note  = models.TextField(null=True,blank=True)
    association_with_other_stelae_and_archaeology  = models.TextField(null=True,blank=True)
    notes  = models.TextField(null=True,blank=True)
    chronology  = models.CharField(max_length=100,null=True,blank=True)
    chronology_fk  = models.ForeignKey('PeriodSummary',null=True,blank=True)
    finding  = models.TextField(null=True,blank=True)
    bibliography  = models.TextField(null=True,blank=True)
    # GeoDjango-specific: a geometry field (PointField) and
    # overriding the default manager with a GeoManager instance.
    point = models.PointField(null=True,blank=True)
    objects = models.GeoManager()
    # New field Jan 2015
    discovery = models.ForeignKey('Discovery',null=True,blank=True)
    location_summary = models.ManyToManyField('LocationSummary',blank=True)
    stelae_type = models.ManyToManyField('StelaeType',blank=True)
    type_of_land = models.ManyToManyField('TypeOfLand',blank=True)
    human_figure_m2m = models.ManyToManyField('HumanFigure',blank=True)

    discovery_raw = models.CharField(max_length=100,null=True,blank=True)
    location_summary_raw = models.CharField(max_length=100,null=True,blank=True)
    stelae_type_raw = models.CharField(max_length=100,null=True,blank=True)
    type_of_land_raw = models.CharField(max_length=100,null=True,blank=True)
    human_figure_m2m_raw = models.CharField(max_length=1000,null=True,blank=True)

    motif = models.ManyToManyField('Motif',blank=True)

    chronology_start_bc = models.IntegerField(null=True,blank=True)
    chronology_end_bc = models.IntegerField(null=True,blank=True)	

    def __unicode__(self):
        return u'%s' % (self.site_fk)
		
    #For elastic search spatial query
    def get_location(self):
        if self.point:
            return Point(self.point.x,self.point.y)
        return Point(0,0)

    def get_geojson(self):
        string = ''
        try:
            if self.point:
                string += '[' + str(self.point.x) + ',' + str(self.point.y) + ']'
                return string
        except Exception:
            pass
            return None
    
    def haystack_name(self):
        return 'stelae'

        
    def popup_content(self):
        #try:	
            str = "<table><thead>"
            try:			
                str += "<tr><th colspan='2'><a target='_blank' href='/view/stelae_full/" + \
                    self.id.__str__() + "'>" + u'%s' % self.site_fk.site_name + "</a></th></tr></thead><tbody>"
            except Exception as e:
                str += "<tr><th colspan='2'><a target='_blank' href='/admin/aema_db/stelae/" + \
                    self.id.__str__() + "'>No site assigned</a></th></tr></thead><tbody>"			
            if self.type_of_land.all().count() > 0:            
                str += "<tr><th>Land type</th><td>"
                for m in self.type_of_land.all():
                    str += m.description + ', '
                str = str[0:-2]
                str += "</td></tr>"				
            str += "</td></tr>"
            if self.stone_shape_m2m.all().count() > 0:
                str += "<tr><th>Stone shape</th><td>"			
                for m in self.stone_shape_m2m.all():
                    str += m.description + ', '
                str = str[0:-2]
                str += "</td></tr>"
            str += "<tr><th>Motif</th><td>"
            str += self.motif_overview
            str += "</td></tr>"
            str += "<tr><th>Condition</th><td>"
            str += self.condition
            str += "</td></tr>"			
            if self.technique_m2m.all().count() > 0:
                str += "<tr><th>Technique</th><td>"
                for cn in self.technique_m2m.all():
                    str +=  cn.__unicode__() + ', '
                str = str[0:-2]
                str += "</td></tr>"		
            str += "</tbody></table>"
            str += "<button class='button tiny popup-extra' data-reveal-id='more-detail-modal' data-reveal-ajax='/view/stelae/"+ self.id.__str__() +"'>More</button>"
            return str
        #except Exception as e:
        #    str = '<p>Some problem with stelae ID: ' + self.id.__str__() + '</p> '
        #    str += "<button class='button tiny popup-extra' data-reveal-id='more-detail-modal' data-reveal-ajax='/view/stelae/"+ self.id.__str__() +"'>More</button>"			
        #    return str

    class Meta:
        verbose_name_plural = 'Stelae'
        ordering = ('site_name','id')

    def save(self, *args, **kwargs):
        if self.lat and self.lon:
            self.point = GEOSGeometry('POINT(' + str(self.lon ) + ' ' + str(self.lat) + ')')
        elif self.point:
            p = self.point
            self.lat = p.y
            self.lon = p.x
        super(Stelae, self).save(*args, **kwargs)

   
class Ogam(models.Model):
    site = models.CharField(max_length=100,null=True,blank=True)
    site_fk = models.ForeignKey('Site',null=True,blank=True)
    ancient_name = models.CharField(max_length=100,null=True,blank=True)
    province = models.CharField(max_length=100,null=True,blank=True)
    rmp = models.CharField(max_length=100,null=True,blank=True,verbose_name='Record of Monument and Place')
    coords = models.CharField(max_length=200,null=True,blank=True,help_text='Irish Transverse Mercator, please use Map or WGS84 Lat/Lon from here on')
    lon = models.FloatField(null=True,blank=True)
    lat = models.FloatField(null=True,blank=True)
    text = models.CharField(max_length=100,null=True,blank=True)
    expansion = models.CharField(max_length=100,null=True,blank=True)
    number = models.CharField(max_length=100,null=True,blank=True)
    type = models.CharField(max_length=100,null=True,blank=True)
    context = models.TextField(max_length=1000,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    script = models.CharField(max_length=100,null=True,blank=True)
    script_fk = models.ForeignKey('Script',null=True,blank=True)
    language = models.CharField(max_length=100,null=True,blank=True)
    language_fk = models.ForeignKey('Language',null=True,blank=True)
    contains_pn = models.CharField(max_length=100,null=True,blank=True)
    contains_pn_bool = models.NullBooleanField(verbose_name='Contains personal names?')
    comment = models.CharField(max_length=100,null=True,blank=True)
    nf = models.CharField(max_length=100,null=True,blank=True,verbose_name='Name formulae')
    name_forms_present = models.ManyToManyField('NameForm',verbose_name='Name formulae M2M')
    # GeoDjango-specific: a geometry field (PointField) and
    # overriding the default manager with a GeoManager instance.
    point = models.PointField(null=True,blank=True)
    objects = models.GeoManager()	

    def __unicode__(self):
        id = str(self.site_fk)
        return id

    def save(self, *args, **kwargs):
        if self.lat and self.lon:
            self.point = GEOSGeometry('POINT(' + str(self.lon ) + ' ' + str(self.lat) + ')')
        elif self.point:
            p = self.point
            self.lat = p.y
            self.lon = p.x
        super(Ogam, self).save(*args, **kwargs)
		
    class Meta:
        verbose_name_plural = 'Ogam'
        ordering = ('site',)


class OgamFernandoRaw(models.Model):
    word = models.CharField(max_length=500,null=True,blank=True)
    nr = models.CharField(max_length=500,null=True,blank=True)
    source  = models.CharField(max_length=500,null=True,blank=True)
    context  = models.TextField(null=True,blank=True)
    leptonic  = models.TextField(max_length=500,null=True,blank=True)
    pie_etymology  = models.CharField(max_length=500,null=True,blank=True)
    ie_etymology  = models.CharField(max_length=500,null=True,blank=True)
    gaulish  = models.CharField(max_length=500,null=True,blank=True)
    proto_celtic_etymology  = models.CharField(max_length=500,null=True,blank=True)
    celtic_etymology  = models.CharField(max_length=1000,null=True,blank=True)
    celtic_cognates = models.CharField(max_length=500,null=True,blank=True)	
    galatian  = models.CharField(max_length=500,null=True,blank=True)
    morphology  = models.CharField(max_length=500,null=True,blank=True)
    syntax  = models.CharField(max_length=500,null=True,blank=True)
    semantic  = models.CharField(max_length=500,null=True,blank=True)
    other_hispano_celtic  = models.CharField(max_length=500,null=True,blank=True)
    other_hispano_celtic_2  = models.CharField(max_length=500,null=True,blank=True)	
    phonology  = models.CharField(max_length=500,null=True,blank=True)
    script = models.CharField(max_length=500,null=True,blank=True)
    irish = models.CharField(max_length=500,null=True,blank=True)
    welsh = models.CharField(max_length=500,null=True,blank=True)	
    cornish = models.CharField(max_length=500,null=True,blank=True)   
    breton = models.CharField(max_length=500,null=True,blank=True)   
    cont_celtic = models.CharField(max_length=500,null=True,blank=True)
    cont_celtic_2 = models.CharField(max_length=500,null=True,blank=True)
    cumbric = models.CharField(max_length=500,null=True,blank=True)
    brittonic = models.CharField(max_length=500,null=True,blank=True)
    insular_celtic = models.CharField(max_length=500,null=True,blank=True)
    pictish_celtic = models.CharField(max_length=500,null=True,blank=True)
    pictish_celtic_2 = models.CharField(max_length=500,null=True,blank=True)
    scottish_gaelic = models.CharField(max_length=500,null=True,blank=True)
    scottish_gaelic_2 = models.CharField(max_length=500,null=True,blank=True)	
    manx = models.CharField(max_length=500,null=True,blank=True)
    goidelic = models.CharField(max_length=500,null=True,blank=True)
    findspot = models.CharField(max_length=500,null=True,blank=True)
    mod_province = models.CharField(max_length=500,null=True,blank=True)
    materials = models.CharField(max_length=500,null=True,blank=True)
    type = models.CharField(max_length=500,null=True,blank=True)
    dates = models.CharField(max_length=500,null=True,blank=True)
	
    def __unicode__(self):
        if self.word:
            return self.word
        return self.id
		
class AbrazoFernandoRaw(models.Model):
    word = models.CharField(max_length=500,null=True,blank=True)
    #toponyms = models.ManyToManyField('Toponyms',blank=True,through='Ab_to_Topo')
    toponyms = models.ManyToManyField('Toponyms',blank=True)
    #etymologies = models.ManyToManyField('EtymologyDescription',blank=True,through='Ab_to_Etym')
    etymologydescription = models.ManyToManyField('EtymologyDescription',verbose_name='Etymology description')
    nr = models.CharField(max_length=1000,null=True,blank=True)
    source  = models.CharField(max_length=1000,null=True,blank=True)
    context  = models.TextField(null=True,blank=True)
    leptonic  = models.CharField(max_length=1000,null=True,blank=True)
    pie_etymology  = models.CharField(max_length=1000,null=True,blank=True)
    ie_etymology  = models.CharField(max_length=1000,null=True,blank=True)
    gaulish  = models.CharField(max_length=1000,null=True,blank=True)
    proto_celtic_etymology  = models.CharField(max_length=1000,null=True,blank=True)
    celtic_etymology  = models.CharField(max_length=1000,null=True,blank=True)
    celtic_cognates = models.CharField(max_length=1000,null=True,blank=True)	
    galatian  = models.CharField(max_length=1000,null=True,blank=True)
    morphology  = models.CharField(max_length=1000,null=True,blank=True)
    syntax  = models.CharField(max_length=1000,null=True,blank=True)
    semantic  = models.CharField(max_length=1000,null=True,blank=True)
    other_hispano_celtic  = models.CharField(max_length=1000,null=True,blank=True)
    other_hispano_celtic_2  = models.CharField(max_length=1000,null=True,blank=True)	
    phonology  = models.CharField(max_length=1000,null=True,blank=True)
    script = models.CharField(max_length=1000,null=True,blank=True)
    irish = models.CharField(max_length=1000,null=True,blank=True)
    welsh = models.CharField(max_length=1000,null=True,blank=True)	
    cornish = models.CharField(max_length=1000,null=True,blank=True)   
    breton = models.CharField(max_length=1000,null=True,blank=True)   
    cont_celtic = models.CharField(max_length=1000,null=True,blank=True)
    cont_celtic_2 = models.CharField(max_length=1000,null=True,blank=True)
    cumbric = models.CharField(max_length=1000,null=True,blank=True)
    brittonic = models.CharField(max_length=1000,null=True,blank=True)
    insular_celtic = models.CharField(max_length=1000,null=True,blank=True)
    pictish_celtic = models.CharField(max_length=1000,null=True,blank=True)
    pictish_celtic_2 = models.CharField(max_length=1000,null=True,blank=True)
    scottish_gaelic = models.CharField(max_length=1000,null=True,blank=True)
    scottish_gaelic_2 = models.CharField(max_length=1000,null=True,blank=True)	
    manx = models.CharField(max_length=1000,null=True,blank=True)
    goidelic = models.CharField(max_length=1000,null=True,blank=True)
    findspot = models.CharField(max_length=1000,null=True,blank=True)
    mod_province = models.CharField(max_length=1000,null=True,blank=True)
    materials = models.CharField(max_length=1000,null=True,blank=True)
    type = models.CharField(max_length=1000,null=True,blank=True)
    dates = models.CharField(max_length=1000,null=True,blank=True)
    bibliography = models.CharField(max_length=1000,null=True,blank=True)
    # GeoDjango-specific: a geometry field (PointField) and
    # overriding the default manager with a GeoManager instance.
    lon = models.FloatField(null=True,blank=True)
    lat = models.FloatField(null=True,blank=True)
    point = models.PointField(null=True,blank=True)
    objects = models.GeoManager()

    def save(self, *args, **kwargs):
        #if self.lat != None and self.lon != None:
        #    self.point = GEOSGeometry('POINT(' + str(self.lon ) + ' ' + str(self.lat) + ')')
        if self.point:
            p = self.point
            self.lat = p.y
            self.lon = p.x
        super(AbrazoFernandoRaw, self).save(*args, **kwargs)
        
	
    def __unicode__(self):
        if self.word:
            return self.word
        return self.id

    class Meta:
        verbose_name = 'Celtiberian Word'
        verbose_name_plural = 'Celtiberian Words'        


#class Ab_to_Topo(models.Model):
#    abrazo = models.ForeignKey('AbrazoFernandoRaw')
#    toponym = models.ForeignKey('Toponyms')

#class Ab_to_Etym(models.Model):
#    abrazo = models.ForeignKey('AbrazoFernandoRaw')
#    etymology = models.ForeignKey('EtymologyDescription')

class OgamSite(models.Model):
    site = models.CharField(max_length=100,null=True,blank=True)
    site_fk = models.ForeignKey('Site',null=True,blank=True)
    ancient_name = models.CharField(max_length=100,null=True,blank=True)
    province = models.CharField(max_length=100,null=True,blank=True)
    rmp = models.CharField(max_length=100,null=True,blank=True,verbose_name=\
        'Record of Monument and Place')
    coords = models.CharField(max_length=200,null=True,blank=True,\
        help_text='Irish Transverse Mercator, \
        please use Map or WGS84 Lat/Lon from here on')
    lon = models.FloatField(null=True,blank=True)
    lat = models.FloatField(null=True,blank=True)
    full_text = models.CharField(max_length=100,null=True,blank=True) #Equiv to text in previous model
    expanded_text = models.CharField(max_length=100,null=True,blank=True) #Equiv to expansion in previous model
    expanded_text_cleaned = models.CharField(max_length=100,null=True,blank=True)
    number = models.CharField(max_length=100,null=True,blank=True)#Number of inscriptions 
    type = models.CharField(max_length=100,null=True,blank=True)
 
    context_description = models.TextField(max_length=1000,null=True,blank=True) #Equiv to context in previous model
    #Choice fields:
    context_micro = models.CharField(max_length=2,null=True,blank=True,choices=context_micro_choices)
    context_micro_free_text = models.CharField(max_length=50,null=True,blank=True,\
        help_text='To be moved into drop down list')
    context_secondary = models.NullBooleanField()
    context_secondary_text = models.CharField(max_length=10,null=True,blank=True,\
        help_text='To be moved into tick box')
    context_macro = models.CharField(max_length=2,null=True,blank=True,choices=context_macro_choices)
    context_macro_free_text = models.CharField(max_length=50,blank=True,null=True,\
        help_text='to be moved into drop down list')
    etymology = models.TextField(null=True,blank=True,\
        help_text='Temporary field to hold imported data. Contents should probably migrate to Fernandos data below')
    meaning = models.TextField(null=True,blank=True,\
        help_text='Temporary field to hold imported data. Contents should probably migrate to Fernandos data below')

    date = models.CharField(max_length=100,null=True,blank=True)
    script = models.CharField(max_length=100,null=True,blank=True)
    script_fk = models.ForeignKey('Script',null=True,blank=True)
    language = models.CharField(max_length=100,null=True,blank=True)
    language_fk = models.ForeignKey('Language',null=True,blank=True)
    contains_pn = models.CharField(max_length=100,null=True,blank=True)
    contains_pn_bool = models.NullBooleanField(verbose_name='Contains personal names?')
    comment = models.CharField(max_length=100,null=True,blank=True)
    nf = models.CharField(max_length=100,null=True,blank=True,verbose_name='Name formulae')
    name_forms_present = models.ManyToManyField('NameForm',verbose_name='Name formulae M2M')
    # GeoDjango-specific: a geometry field (PointField) and
    # overriding the default manager with a GeoManager instance.
    point = models.PointField(null=True,blank=True)
    objects = models.GeoManager()   

    def __unicode__(self):
        try:
            site = u'%s' % self.site_fk.site_name #str(self.site_fk)
            id = str(self.id)
        except Exception:
            return 'No site name specified'
        return u'%s, site id: %s' % (site,id)

    def get_geojson(self):
        string = ''
        try:
            if self.point:
                string += '[' + str(self.point.x) + ',' + str(self.point.y) + ']'
                return string
        except Exception:
            pass
            return None
    
    def cname(self):
        return self.__class__.__name__

    def haystack_name(self):
        #return 'ogam'
        return 'inscriptions'

    #For elastic search spatial query
    def get_location(self):
        if self.point:
            return Point(self.point.x,self.point.y)
        return Point(0,0)

    def popup_content(self):
        try:
            str = "<table><thead>"
            str += "<tr><th colspan='2'><a target='_blank' href='/view/ogamsite_full/" + self.id.__str__() + "'>" + u'%s' % self.site_fk.site_name + "</a></th></tr></thead><tbody>"
            str += "<tr><th>Ancient name</th><td>"
            str += self.ancient_name.__str__()
            str += "</td></tr>"
            str += "<tr><th>Expanded text</th><td>"
            str += self.expanded_text.__str__()
            str += "</td></tr>"
            str += "<tr><th>Context</th><td>"
            str += self.get_context_macro_display().__str__() + ' ' +self.get_context_micro_display().__str__()
            str += "</td></tr>"        
            str += "</tbody></table>"
            str += "<button class='button tiny popup-extra' data-reveal-id='more-detail-modal' data-reveal-ajax='/view/ogamsite/"+ self.id.__str__() +"'>More</button>"
            return str
        except Exception as e:
            str = '<p>Some problem with Ogam site ID: ' + self.id.__str__() + '</p> '
            return str
    
    class Meta:
        verbose_name_plural = 'Ogam site'
        ordering = ('site',)

    def save(self, *args, **kwargs):
        if self.lat and self.lon:
            self.point = GEOSGeometry('POINT(' + str(self.lon ) + ' ' + str(self.lat) + ')')
        elif self.point:
            p = self.point
            self.lat = p.y
            self.lon = p.x
        super(OgamSite, self).save(*args, **kwargs)
		

class OgamInscription(models.Model):
    ogamsite_fk = models.ForeignKey('OgamSite',null=True,blank=True)
    toponym = models.ForeignKey('Toponyms',null=True,blank=True)
    name = models.TextField(null=True,blank=True) #Equiv to Word in previous Fernando data	
    name_clean = models.CharField(max_length=500,null=True,blank=True) #Equiv to Word in previous Fernando data
    expanded_text = models.CharField(max_length=100,null=True,blank=True) #Equiv to expansion in previous model
    is_ogam = models.NullBooleanField()
    reference = models.CharField(max_length=250,null=True,blank=True) #Equiv to Source in previous Fernando data
    script_fk = models.ForeignKey('Script',null=True,blank=True)
    language = models.CharField(max_length=50,null=True,blank=True,\
        help_text='Legacy field to be moved to drop down list')
    language_fk = models.ForeignKey('Language',null=True,blank=True,verbose_name='Language of name')
    language_of_inscription = models.ForeignKey('Language',null=True,blank=True,related_name='inscription_language')    
    etymology = models.CharField(max_length=50,null=True,blank=True,\
        help_text='Legacy field to be moved to drop down list')
    etymology_fk = models.CharField(max_length=2,choices=etymology_choices,null=True,blank=True)
    #comment = models.CharField(max_length=100,null=True,blank=True)
    comment = models.TextField(null=True,blank=True) #Equiv to Word in previous Fernando data		
    grammatical_description = models.CharField(max_length=100,null=True,blank=True)

    #Dating section
    chronology = models.CharField(max_length=100,null=True,blank=True,\
        help_text='Should this be a drop down list also? NJ')
    reason = models.CharField(max_length=100,null=True,blank=True,\
        help_text='Should this be a drop down list also? NJ')
    #Detail context section
    materials = models.CharField(max_length=500,null=True,blank=True)
    site_type = models.CharField(max_length=500,null=True,blank=True)#Type in fernandos original data

    source  = models.CharField(max_length=500,null=True,blank=True)
    context  = models.TextField(null=True,blank=True)
    leptonic  = models.TextField(max_length=1000,null=True,blank=True,verbose_name="Lepontic")
    pie_etymology  = models.TextField(max_length=1000,null=True,blank=True,verbose_name="PIE etymology")
    ie_etymology  = models.TextField(max_length=1000,null=True,blank=True,verbose_name="IE etymology")
    gaulish  = models.TextField(max_length=1000,null=True,blank=True)
    proto_celtic_etymology  = models.TextField(max_length=1000,null=True,blank=True,verbose_name="Proto-Celtic etymology")
    celtic_etymology  = models.TextField(max_length=1000,null=True,blank=True,verbose_name="Celtic etymology")
    celtic_cognates = models.TextField(max_length=1000,null=True,blank=True) 
    galatian  = models.TextField(max_length=1000,null=True,blank=True)
    morphology  = models.TextField(max_length=1000,null=True,blank=True)
    syntax  = models.TextField(max_length=1000,null=True,blank=True)
    semantic  = models.TextField(max_length=1000,null=True,blank=True)
    other_hispano_celtic  = models.TextField(max_length=1000,null=True,blank=True)
    other_hispano_celtic_2  = models.TextField(max_length=1000,null=True,blank=True) 
    phonology  = models.TextField(max_length=1000,null=True,blank=True)
    script = models.TextField(max_length=1000,null=True,blank=True)
    irish = models.TextField(max_length=1000,null=True,blank=True)
    welsh = models.TextField(max_length=1000,null=True,blank=True)   
    cornish = models.TextField(max_length=1000,null=True,blank=True)   
    breton = models.TextField(max_length=1000,null=True,blank=True)   
    cont_celtic = models.TextField(max_length=1000,null=True,blank=True)
    cont_celtic_2 = models.TextField(max_length=1000,null=True,blank=True)
    cumbric = models.TextField(max_length=1000,null=True,blank=True)
    brittonic = models.TextField(max_length=1000,null=True,blank=True)
    insular_celtic = models.TextField(max_length=1000,null=True,blank=True)
    pictish_celtic = models.TextField(max_length=1000,null=True,blank=True)
    pictish_celtic_2 = models.TextField(max_length=1000,null=True,blank=True)
    scottish_gaelic = models.TextField(max_length=1000,null=True,blank=True)
    scottish_gaelic_2 = models.TextField(max_length=1000,null=True,blank=True)   
    manx = models.TextField(max_length=1000,null=True,blank=True)
    goidelic = models.TextField(max_length=1000,null=True,blank=True)
    findspot = models.CharField(max_length=500,null=True,blank=True)
    mod_province = models.CharField(max_length=500,null=True,blank=True)
    
    dates = models.CharField(max_length=500,null=True,blank=True)

    matchstring = models.CharField(max_length=200,null=True,blank=True)
    
    def __unicode__(self):
        if self.name:
            return u'%s' % self.name
        return u'%s' % str(self.id) 


# Now renamed metalwork in front end
class Hoards(models.Model):
    site_name = models.CharField(max_length=1000,null=True,blank=True)
    #fk
    site_fk = models.ForeignKey(Site,null=True,blank=True)
    lat = models.FloatField(null=True,blank=True)
    lon = models.FloatField(null=True,blank=True)
    area = models.CharField(max_length=1000,null=True,blank=True)
    region = models.CharField(max_length=1000,null=True,blank=True)
    country = models.CharField(max_length=1000,null=True,blank=True)
    easting = models.FloatField(null=True,blank=True)
    northing = models.FloatField(null=True,blank=True)
    deposit_overview = models.TextField(max_length=1000,null=True,blank=True)
    deposit_context = models.TextField(max_length=1000,null=True,blank=True)
    no_of_objects = models.CharField(max_length=1000,null=True,blank=True)
    no_of_objects_cleaned = models.IntegerField(null=True,blank=True)#Clean with regex from no_of_objects text field    
    no_of_objects_clustered = models.CharField(max_length=1000,null=True,blank=True)
    no_of_objects_clustered_choice = models.CharField(choices=hoard_object_count,max_length=2,null=True,blank=True)
    find_type = models.CharField(max_length=1000,null=True,blank=True)
    find_type_cleaned = models.CharField(choices=hoard_find_type_choices,max_length=2,null=True,blank=True)
    material_type = models.CharField(max_length=1000,null=True,blank=True)
    #m2m
    material_type_fk = models.ManyToManyField(HoardMaterial,blank=True)
    summary_deposit_type = models.CharField(max_length=1000,null=True,blank=True)
    general_type = models.CharField(max_length=1000,null=True,blank=True)
    #m2m
    general_type_m2m = models.ManyToManyField(HoardType,blank=True)
    specific_object_type_m2m = models.ManyToManyField(HoardSpecificObject,blank=True)
    specific_object_description = models.TextField(max_length=1000,null=True,blank=True)
    arrangement_of_objects = models.TextField(max_length=1000,null=True,blank=True)
    object_condition = models.CharField(max_length=1000,null=True,blank=True)
    object_condition_summary = models.CharField(max_length=1000,null=True,blank=True)
    object_condition_summary_choice = models.CharField(max_length=32,choices=hoard_object_condition_choice,null=True,blank=True)
    dry_wet_context = models.CharField(max_length=1000,null=True,blank=True)
    dry_wet_context_choice = models.CharField(max_length=2,choices=hoard_context_choice,null=True,blank=True)
    metal_analysis_summary_1 = models.CharField(max_length=1000,null=True,blank=True)
    context_summary = models.CharField(max_length=1000,null=True,blank=True)
    context_summary_m2m = models.ManyToManyField(HoardContextSummary,blank=True)
    chronology_date_bracket_BC = models.CharField(max_length=1000,null=True,blank=True)
    chronology_start_date_BC = models.IntegerField(null=True,blank=True)
    chronoloy_end_date_BC = models.IntegerField(null=True,blank=True)
    regional_period_phase  = models.CharField(max_length=1000,null=True,blank=True)
    period_summary  = models.CharField(max_length=1000,null=True,blank=True)
    #fk
    period_summary_fk = models.ForeignKey(PeriodSummary,null=True,blank=True)
    c14_dates = models.CharField(max_length=1000,null=True,blank=True)
    refs = models.CharField(max_length=1000,null=True,blank=True)
    notes = models.TextField(max_length=1000,null=True,blank=True)
    # GeoDjango-specific: a geometry field (PointField) and
    # overriding the default manager with a GeoManager instance.
    point = models.PointField(null=True,blank=True)
    objects = models.GeoManager()	

    def __unicode__(self):
        if self.site_fk:
            return self.site_fk.site_name
        return u'None'

    def haystack_name(self):
        #return 'hoards'
        return 'metalwork'

    def get_geojson(self):
        string = ''
        try:
            if self.point:
                string += '[' + str(self.point.x) + ',' + str(self.point.y) + ']'
                return string
        except Exception:
            pass
            return None

    #For elastic search spatial query
    def get_location(self):
        if self.point:
            return Point(self.point.x,self.point.y)
        return Point(0,0)

    def popup_content(self):
        try:	
            str = "<table><thead>"
            str += "<tr><th colspan='2'><a target='_blank' href='/view/hoard_full/" + \
                self.id.__str__() + "'>" + u'%s' % self.site_fk.site_name + "</a></th></tr></thead><tbody>"
            str += "<tr><th>Find type</th><td>"
            str += self.get_find_type_cleaned_display()
            str += "</td></tr>"
            if self.material_type_fk.all().count() > 0:
                str += "<tr><th>Material(s)</th><td>"			
                for m in self.material_type_fk.all():
                    str += m.description + ', '
                str = str[0:-2]
                str += "</td></tr>"
            str += "<tr><th>No. of objects</th><td>"
            str += self.get_no_of_objects_clustered_choice_display()
            str += "</td></tr>"
            if self.specific_object_type_m2m.all().count() > 0:
                str += "<tr><th>Object type(s)</th><td>"
                for cn in self.specific_object_type_m2m.all():
                    str +=  cn.description + ', '
                str = str[0:-2]
                str += "</td></tr>"		
            if self.context_summary_m2m.all().count() > 0:
                str += "<tr><th>Context</th><td>"
                for cn in self.context_summary_m2m.all():
                     str +=  cn.description + ', '
                str = str[0:-2]
                str += "</td></tr>"
            str += "</tbody></table>"
            str += "<button class='button tiny popup-extra' data-reveal-id='more-detail-modal' data-reveal-ajax='/view/hoards/"+ self.id.__str__() +"'>More</button>"
            return str
        except Exception as e:
            str = '<p>Some problem with hoard ID: ' + self.id.__str__() + '</p> '
            return str

    class Meta:
        verbose_name = 'Metalwork'
        verbose_name_plural = 'Metalwork'
        #verbose_name_plural = 'Hoards'

    def save(self, *args, **kwargs):
        if self.lat and self.lon:
            self.point = GEOSGeometry('POINT(' + str(self.lon ) + ' ' + str(self.lat) + ')')
        elif self.point:
            p = self.point
            self.lat = p.y
            self.lon = p.x
        super(Hoards, self).save(*args, **kwargs)


		
class Toponyms(models.Model):
    #id = models.IntegerField(null=True, db_column='ID', blank=True) # Field name made lowercase.
    name = models.CharField(max_length=30, db_column='toponym', blank=True) # Field name made lowercase.
    source = models.CharField(max_length=30, db_column='source', blank=True) # Field name made lowercase.
    etymological_desc = models.ForeignKey('EtymologyDescription',null=True,blank=True)
    language = models.CharField(max_length=10, db_column='language', blank=True) # Field name made lowercase.
    language_fk = models.ForeignKey('Language',null=True, blank=True) # Field name made lowercase.	
    briga = models.CharField(max_length=1, db_column='briga', blank=True) # Field name made lowercase.
    dunon = models.CharField(max_length=1, db_column='dunon', blank=True) # Field name made lowercase.
    duron = models.CharField(max_length=1, db_column='duron', blank=True) # Field name made lowercase.
    ebur = models.CharField(max_length=1, db_column='ebur', blank=True) # Field name made lowercase.
    magos = models.CharField(max_length=1, db_column='magos', blank=True) # Field name made lowercase.
    nemeton = models.CharField(max_length=1, db_column='nemeton', blank=True) # Field name made lowercase.
    sego_field = models.CharField(max_length=1, db_column='sego', blank=True) # Field name made lowercase. Field renamed because it ended with '_'.
    notes = models.CharField(max_length=30, db_column='notes', blank=True) # Field name made lowercase.
    variants = models.CharField(max_length=60, db_column='variants', blank=True) # Field name made lowercase.
    object = models.CharField(max_length=10, db_column='obj', blank=True) # Field name made lowercase.
    object_fk = models.ForeignKey('SettlementType',null=True, blank=True)	
    text = models.CharField(max_length=20, db_column='toponym_text', blank=True) # Field name made lowercase.
    notes_2_m = models.CharField(max_length=50, db_column='notes_2', blank=True) # Field name made lowercase. Field renamed because it contained more than one '_' in a row.
    novios = models.CharField(max_length=1, db_column='novios', blank=True) # Field name made lowercase.
    cognate = models.CharField(max_length=50,null=True,blank=True)
    point = models.PointField(db_column='the_geom',null=True, blank=True)
    objects = models.GeoManager()
    class Meta:
        db_table = 'aema_db_toponyms'
        ordering = ('name',)
    def __unicode__(self):
        return u'%s' % (self.name)
	

    #For elastic search spatial query
    def get_location(self):
        if self.point:
            return Point(self.point.x,self.point.y)
        return Point(0,0)

    def get_geojson(self):
        string = ''
        try:
            if self.point:
                string += '[' + str(self.point.x) + ',' + str(self.point.y) + ']'
                return string
        except Exception:
            pass
            return None

    def cname(self):
        return self.__class__.__name__

    def haystack_name(self):
        return 'toponyms'

    def site_name_fake(self):
        return u'%s' % self.name

    def popup_content(self):
        str = "<table><thead>"
        str += "<tr><th colspan='2'><a target='_blank' href='/view/toponym_full/" + \
            self.id.__str__() + "'>" + self.name + "</a></th></tr></thead><tbody>"
        str += "<tr><th>Type</th><td>"
        if self.object_fk:
            str += self.object_fk.description
            str += "</td></tr>"
        if self.language:
            str += "<tr><th>Language</th><td>"
            str += self.language
            str += "</td></tr>"
        if self.cognate:
            str += "<tr><th>Definition(s)</th><td>"
            str += self.cognate
            str += "</td></tr>"
        if self.notes:
            str += "<tr><th>Notes</th><td>"
            str += self.notes
            str += "</td></tr>"
        if self.variants:
            str += "<tr><th>Variants</th><td>"
            str += self.variants
            str += "</td></tr>"
        if self.text:
            str += "<tr><th>Text</th><td>"
            str += self.text
            str += "</td></tr>"
        str += "</tbody></table>"
        return str

    # Now renamed metalwork in front end
class Miscellaneous(models.Model):
    site_name = models.CharField(max_length=1000,null=True,blank=True)
    #fk
    site_fk = models.ForeignKey(Site,null=True,blank=True)
    lat = models.FloatField(null=True,blank=True)
    lon = models.FloatField(null=True,blank=True)
    area = models.CharField(max_length=1000,null=True,blank=True)
    region = models.CharField(max_length=1000,null=True,blank=True)
    country = models.CharField(max_length=1000,null=True,blank=True)
    easting = models.FloatField(null=True,blank=True)
    northing = models.FloatField(null=True,blank=True)
    deposit_overview = models.TextField(max_length=1000,null=True,blank=True)
    deposit_context = models.TextField(max_length=1000,null=True,blank=True)
    no_of_objects = models.CharField(max_length=1000,null=True,blank=True)
    no_of_objects_cleaned = models.IntegerField(null=True,blank=True)#Clean with regex from no_of_objects text field    
    no_of_objects_clustered = models.CharField(max_length=1000,null=True,blank=True)
    no_of_objects_clustered_choice = models.CharField(choices=hoard_object_count,max_length=2,null=True,blank=True)
    find_type = models.CharField(max_length=1000,null=True,blank=True)
    find_type_cleaned = models.CharField(choices=hoard_find_type_choices,max_length=2,null=True,blank=True)
    material_type = models.CharField(max_length=1000,null=True,blank=True)
    #m2m
    material_type_fk = models.ManyToManyField(HoardMaterial,blank=True)
    summary_deposit_type = models.CharField(max_length=1000,null=True,blank=True)
    general_type = models.CharField(max_length=1000,null=True,blank=True)
    #m2m
    general_type_m2m = models.ManyToManyField(HoardType,blank=True)
    specific_object_type_m2m = models.ManyToManyField(HoardSpecificObject,blank=True)
    specific_object_description = models.TextField(max_length=1000,null=True,blank=True)
    arrangement_of_objects = models.TextField(max_length=1000,null=True,blank=True)
    object_condition = models.CharField(max_length=1000,null=True,blank=True)
    object_condition_summary = models.CharField(max_length=1000,null=True,blank=True)
    object_condition_summary_choice = models.CharField(max_length=32,choices=hoard_object_condition_choice,null=True,blank=True)
    dry_wet_context = models.CharField(max_length=1000,null=True,blank=True)
    dry_wet_context_choice = models.CharField(max_length=2,choices=hoard_context_choice,null=True,blank=True)
    material_analysis_summary = models.CharField(max_length=1000,null=True,blank=True)
    context_summary = models.CharField(max_length=1000,null=True,blank=True)
    context_summary_m2m = models.ManyToManyField(HoardContextSummary,blank=True)
    chronology_date_bracket_BC = models.CharField(max_length=1000,null=True,blank=True)
    chronology_start_date_BC = models.IntegerField(null=True,blank=True)
    chronoloy_end_date_BC = models.IntegerField(null=True,blank=True)
    regional_period_phase  = models.CharField(max_length=1000,null=True,blank=True)
    period_summary  = models.CharField(max_length=1000,null=True,blank=True)
    #fk
    period_summary_fk = models.ForeignKey(PeriodSummary,null=True,blank=True)
    c14_dates = models.CharField(max_length=1000,null=True,blank=True)
    refs = models.CharField(max_length=1000,null=True,blank=True)
    notes = models.TextField(max_length=1000,null=True,blank=True)
    # GeoDjango-specific: a geometry field (PointField) and
    # overriding the default manager with a GeoManager instance.
    point = models.PointField(null=True,blank=True)
    objects = models.GeoManager()   

    def __unicode__(self):
        if self.site_fk:
            return self.site_fk.site_name
        return u'None'

    def haystack_name(self):
        #return 'hoards'
        return 'miscellaneous'

    def get_geojson(self):
        string = ''
        try:
            if self.point:
                string += '[' + str(self.point.x) + ',' + str(self.point.y) + ']'
                return string
        except Exception:
            pass
            return None

    #For elastic search spatial query
    def get_location(self):
        if self.point:
            return Point(self.point.x,self.point.y)
        return Point(0,0)

    def popup_content(self):
        try:    
            str = "<table><thead>"
            str += "<tr><th colspan='2'><a target='_blank' href='/view/miscellaneous_full/" + \
                self.id.__str__() + "'>" + u'%s' % self.site_fk.site_name + "</a></th></tr></thead><tbody>"
            str += "<tr><th>Find type</th><td>"
            str += self.get_find_type_cleaned_display()
            str += "</td></tr>"
            if self.material_type_fk.all().count() > 0:
                str += "<tr><th>Material(s)</th><td>"           
                for m in self.material_type_fk.all():
                    str += m.description + ', '
                str = str[0:-2]
                str += "</td></tr>"
            str += "<tr><th>No. of objects</th><td>"
            str += self.get_no_of_objects_clustered_choice_display()
            str += "</td></tr>"
            if self.specific_object_type_m2m.all().count() > 0:
                str += "<tr><th>Object type(s)</th><td>"
                for cn in self.specific_object_type_m2m.all():
                    str +=  cn.description + ', '
                str = str[0:-2]
                str += "</td></tr>"     
            if self.context_summary_m2m.all().count() > 0:
                str += "<tr><th>Context</th><td>"
                for cn in self.context_summary_m2m.all():
                     str +=  cn.description + ', '
                str = str[0:-2]
                str += "</td></tr>"
            str += "</tbody></table>"
            str += "<button class='button tiny popup-extra' data-reveal-id='more-detail-modal' data-reveal-ajax='/view/miscellaneous/"+ self.id.__str__() +"'>More</button>"
            return str
        except Exception as e:
            str = '<p>Some problem with miscellaneous object ID: ' + self.id.__str__() + '</p> '
            return str

    class Meta:
        verbose_name = 'Miscellaneous'
        verbose_name_plural = 'Miscellany'
        #verbose_name_plural = 'Hoards'

    def save(self, *args, **kwargs):
        if self.lat and self.lon:
            self.point = GEOSGeometry('POINT(' + str(self.lon ) + ' ' + str(self.lat) + ')')
        elif self.point:
            p = self.point
            self.lat = p.y
            self.lon = p.x
        super(Miscellaneous, self).save(*args, **kwargs)
