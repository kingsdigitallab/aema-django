

# Create your models here.
# coding: utf-8

from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry,Point
from .choices import *
from aema_db.models import *


##### Auxilliary models:

#### Places:

class Site(models.Model):
    site_name = models.CharField(max_length=100)
    ancient_name = models.CharField(max_length=100,null=True,blank=True)
    area = models.CharField(max_length=100,null=True,blank=True)
    area_fk = models.ForeignKey('Area',null=True,blank=True)
    region = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        if self.area_fk:
            area = self.area_fk.area_name
            if self.area_fk.region_fk:
                region = self.area_fk.region_fk.region_name
                if self.area_fk.region_fk.country_fk:
                    country = self.area_fk.region_fk.country_fk.country_name
                else:
                    country = 'Country - blank description or absent'
            else:
                region = 'Region - blank description or absent'
                country = 'Country - blank description or absent'
        else:
            area = 'Area - blank description or absent'
            region = 'Region - blank description or absent'
            country = 'Country - blank description or absent'            
        return '%s, ID:%s (%s, %s, %s)' % (self.site_name,self.id,area,region,country)
                    
    class Meta:
        verbose_name_plural = 'Sites'
        ordering = ('site_name','id')
    
    
        
        
class Area(models.Model):
    area_name = models.CharField(max_length=100,null=True,blank=True)
    region = models.CharField(max_length=100,null=True,blank=True)
    region_fk = models.ForeignKey('Region',null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        if self.area_name:
            area = self.area_name
        else:
            area = 'Area not named'
        if self.region_fk:
            region = self.region_fk.region_name
            if self.region_fk.country_fk:
                country = self.region_fk.country_fk.country_name
            else:
                country = 'Country - blank description or absent'
        else:
            region = 'Region - blank description or absent'
            country = 'Country - blank description or absent'
        return '%s, ID:%s (%s, %s)' % (area,self.id,region,country)
    class Meta:
        ordering = ('area_name','id')
    @staticmethod
    def autocomplete_search_fields():
        return ("id_exact","area_fk__area_name__icontains",)    

        
        
class Region(models.Model):
    region_name = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    country_fk = models.ForeignKey('Country',null=True,blank=True)
    def __str__(self):
        if self.region_name:
            region = self.region_name
            if self.country_fk:
                country = self.country_fk.country_name
            else:
                country = 'Country - blank description or absent'
        else:
            region = 'Region - blank description or absent'
            country = 'Country - blank description or absent'
        
        return '%s, ID:%s (%s)' % (region,self.id,country)
    class Meta:
        ordering = ('region_name','id')        
    @staticmethod
    def autocomplete_search_fields():
        return ("id_exact","region_name__icontains",) 


 
class Country(models.Model):
    country_name = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        if self.country_name:
            country  = self.country_name
        else:
            country = 'Blank country name'    
        return '%s (%s)' % (country,self.id)
    class Meta:
        ordering = ('country_name','id')        
        verbose_name_plural = 'Countries'
        

### Archeaological classifications

# Linked to Burials by M2M
class SiteType(models.Model):
    site_type = models.CharField(max_length=100)
    def __str__(self):
        return self.site_type
    class Meta:
        ordering = ('site_type','id')

class SiteTypeSpecific(models.Model):
    description = models.CharField(max_length=100)
    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description','id')
    

class BurialIndividuals(models.Model):
    burial = models.ForeignKey('Burials')
    burial_type = models.CharField(max_length=2,choices=burial_type_choices,null=True,blank=True)
    gender = models.CharField(default='NI',max_length=2,choices=burial_gender_choice,null=True,blank=True)
    age = models.CharField(default='NI',max_length=2,choices=burial_age_assemblage,null=True,blank=True)
    usage =  models.CharField(max_length=2,choices=burial_usage_choice,null=True,blank=True)
    location_in_grave = models.CharField(max_length=200,null=True,blank=True)
    # New field for specific type imported from Burials
    site_type = models.ForeignKey('SiteTypeSpecific',null=True,blank=True,verbose_name='Grave type')

    position = models.CharField(max_length=2,choices=burial_position_choices,null=True,blank=True)
    position_fk = models.ForeignKey('BurialPosition',null=True,blank=True)
    orientation = models.CharField(max_length=2,choices=burial_orientation_choices,null=True,blank=True)
    head_position = models.CharField(max_length=2,choices=burial_direction_choices,null=True,blank=True)
    head_direction = models.CharField(max_length=2,choices=burial_direction_choices,null=True,blank=True)
    grave_good_m2m = models.ManyToManyField('GraveGood',blank=True)
    pot_m2m = models.ManyToManyField('Pot',blank=True)
    organic_material_fk = models.ForeignKey('OrganicMaterial',null=True,blank=True,verbose_name='Organic Material')
    date_ref = models.CharField(max_length=30,null=True,blank=True)    
    uncalibrated_date_bp = models.CharField(max_length=100,null=True,blank=True)
    uncalibrated_date_bc = models.CharField(max_length=100,null=True,blank=True)
    calibrated_date_bc_1_sigma = models.CharField(max_length=50,null=True,blank=True)
    calibrated_date_bc_2_sigma = models.CharField(max_length=50,null=True,blank=True)    
    general_chronology = models.CharField(max_length=50,null=True,blank=True)        
    general_chronology_fk = models.ForeignKey('GeneralChronology',null=True,blank=True)        
    raw_notes = models.TextField(null=True,blank=True)
    # New fields for enabling distance search as point won't allow joins via the django filter(s)
    point = models.PointField(null=True,blank=True)
    objects = models.GeoManager()
    
    def save(self, *args, **kwargs):
        if self.burial.point:
            self.point = GEOSGeometry('POINT(' + str(self.burial.point.x ) + ' ' + str(self.burial.point.y) + ')')
        #elif self.point:
        #    p = self.point
        #    self.lat = p.y
        #    self.lon = p.x
        super(BurialIndividuals, self).save(*args, **kwargs)

    def site_name_fake(self):
        return '%s' % self.burial.site_fk.site_name

    def haystack_name(self):
        return 'individuals'

    def point(self):
        try:
            return self.burial.point
        except Exception:
            return None

    def get_geojson(self):
        string = ''
        try:
            if self.burial.point:
                string += '[' + str(self.burial.point.x) + ',' + str(self.burial.point.y) + ']'
                return string
        except Exception:
            pass
            return None
        
    def __str__(self):
        #TO DO - crappy code quick fix
        if self.age is not None and self.gender is not None:
            return self.get_gender_display() + ', ' + self.get_age_display()
        else:
            return 'Full details not input'
    def get_location(self):
        if self.burial.point:
            return Point(self.burial.point.x,self.burial.point.y)
        return Point(0,0)
    class Meta:
        verbose_name_plural = ('Burial Individuals')

    def popup_content(self):
        str = "<table><thead>"
        if self.burial.site_fk:
            siteName = self.burial.site_fk.site_name
        else:
            siteName = 'Unnamed'
        str += "<tr><th colspan='2'><a target='_blank' href='/view/individual_full/" + \
            self.id.__str__() + "'>" + siteName + "</a></th></tr></thead><tbody>"
        str += "<tr><th>Type</th><td>"
        str += self.get_burial_type_display()
        str += "</td></tr>"
        str += "<tr><th>Gender</th><td>"
        str += self.get_gender_display()
        str += "</td></tr>"
        str += "<tr><th>Age</th><td>"
        str += self.get_age_display()
        str += "</td></tr>"
        if self.pot_m2m.all().count() > 0:
            str += "<tr><th>Pot</th><td>"
            for p in self.pot_m2m.all():
                str +=  p.description + ', '
            str = str[0:-2]
            str += "</td></tr>"
        if self.grave_good_m2m.all().count() > 0:
            str += "<tr><th>Grave goods</th><td>"
            for gd in self.grave_good_m2m.all():
                str +=  gd.functional_type_fk.description + ', '
            str = str[0:-2]
            str += "</td></tr>"
        str += "</tbody></table>"
        str += "<button class='button tiny popup-extra' data-reveal-id='more-detail-modal' data-reveal-ajax='/view/individuals/"+ self.id.__str__() +"'>More</button>"

        return str

# Linked to Burials by M2M
class Gender(models.Model):
    gender_name = models.CharField(max_length=30)
    def __str__(self):
        return self.gender_name
    class Meta:
        ordering = ('gender_name',)

class BurialPosition(models.Model):
    short_desc = models.CharField(max_length=2,null=True,blank=True)
    description = models.CharField(max_length=50)
    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',)




class OrganicMaterial(models.Model):
    material_class = models.CharField(max_length=100,null=True,blank=True,help_text='No need to fill this in - it will populate automatically')
    sub_class = models.ForeignKey('OrganicMaterialSubClass',null=True,blank=True)
    master = models.ForeignKey('OrganicMaterialMaster',default=3)
    def save(self, *args, **kwargs):
        self.material_class = self.master.master
        if self.sub_class:
            self.material_class = self.material_class  + ', %s' % self.sub_class
        super(OrganicMaterial, self).save()
    def __str__(self):
        if self.sub_class:
            return '%s, %s' % (self.master,self.sub_class)
        elif self.material_class:
            return self.material_class
        else:
            return '%s' % (self.id)
    def __str__(self):
        return self.material_class
                
    class Meta:
        ordering = ('material_class',)
        unique_together = ('master','sub_class')


class OrganicMaterialMaster(models.Model):
    master = models.CharField(max_length=30)
    def __str__(self):
        return self.master
    class Meta:
        ordering = ('master',)

        
class OrganicMaterialSubClass(models.Model):
    material_sub_class = models.CharField(max_length=50)
    def __str__(self):
        return self.material_sub_class
    class Meta:
        ordering = ('material_sub_class',)


class GraveGood(models.Model):
    type = models.ForeignKey('GraveGoodType',null=True,blank=True,help_text='Possibly redundant field to be removed after updates')
    functional_type = models.CharField(max_length='2',null=True,blank=True,choices=burial_grave_good_type_choices\
        ,help_text='Use the new fk field below')    
    functional_type_fk = models.ForeignKey('GraveGoodFunctionalType',default=1)
    condition = models.BooleanField(default=False,verbose_name='Fragmentary?')    
    placement = models.CharField(max_length='2',choices=burial_pot_and_good_placement_choices,null=True,blank=True)
    placement_fk = models.ForeignKey('GraveGoodPlacement',null=True,blank=True)
    description = models.CharField(max_length=100,null=True,blank=True)
    burial = models.ForeignKey('Burials')
    raw_materials_m2m = models.ManyToManyField('GraveGoodRawMaterialType',blank=True,verbose_name=\
         'Raw materials')
    raw_notes = models.TextField(null=True,blank=True)		 

    
    def site_name_fake(self):
        return self.burial.site_fk.site_name

    def get_location(self):
        if self.burial.point:
            return Point(self.burial.point.x,self.burial.point.y)
        return Point(0,0)

    def get_geojson(self):
        string = ''
        try:
            if self.burial.point:
                string += '[' + str(self.burial.point.x) + ',' + str(self.burial.point.y) + ']'
                return string
        except Exception:
            pass
            return None

    def haystack_name(self):
        return 'gravegoods'
    
    def __str__(self):
        if self.functional_type_fk is not None:
            type = self.functional_type_fk
        elif self.type is not None:
            type = self.type + '( Functional type not yet assigned)'
        else:
            type = 'No type'
        #if self.burial:
        #    site = self.burial.site_fk.site_name
        #    site_id = self.burial.id
        #    return u'%s, from %s (SITE ID:%s)' % (type,site,site_id)
        return '%s, (ID:%s)' % (type,str(self.id))
    class Meta:
        ordering = ('functional_type_fk','id')


class GraveGoodClass(models.Model):
    description = models.CharField(max_length=50)
    def __str__(self):
        return self.description
    class Meta:
        ordering = ('description','id',)
        
class GraveGoodType(models.Model):
    description = models.CharField(max_length=50)
    def __str__(self):
        return self.description
    class Meta:
        ordering = ('description','id',)

class GraveGoodFunctionalType(models.Model):
    short_desc = models.CharField(max_length=2,null=True,blank=True)
    description = models.CharField(max_length=50)
    def __str__(self):
        return self.description
    class Meta:
        ordering = ('description','id',)
    

class GraveGoodRawMaterialType(models.Model):
    description = models.CharField(max_length=50)
    def __str__(self):
        return self.description
    class Meta:
        ordering = ('description','id',)        
        
        
class GraveGoodPlacement(models.Model):
    short_desc = models.CharField(max_length=2,null=True,blank=True)
    description = models.CharField(max_length=50)
    def __str__(self):
        return self.description


class Dating(models.Model):
    burial = models.ForeignKey('Burials')
    general_chronology = models.CharField(max_length=50,null=True,blank=True)
    organic_material = models.ForeignKey('OrganicMaterial',null=True,blank=True)
    date_ref = models.CharField(max_length=20,null=True,blank=True)
    summary = models.CharField(max_length=100,null=True,blank=True)
    calibrated_date_bc_2_sigma = models.CharField(max_length=20,null=True,blank=True)
    uncalibrated_date_bp = models.CharField(max_length=20,null=True,blank=True)
    uncalibrated_date_bc = models.CharField(max_length=20,null=True,blank=True)
    duplicate_field = models.CharField(max_length=50,null=True,blank=True)
    approx_uncalibrated_date_bp = models.IntegerField(null=True,blank=True)
    error_margin = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return 'date for %s' % self.burial 

           
           
class Pot(models.Model):
    CN = (('CN','Container'),)
    amended_choices = burial_pot_and_good_placement_choices + CN

    description = models.CharField(max_length=100)
    count = models.IntegerField(null=True,blank=True,help_text='Redundant - to be replaced/moved')    
    pot_placement = models.CharField(max_length='2',choices=amended_choices,null=True,blank=True)
    pot_disposition = models.CharField(max_length='2',choices=burial_pot_position_choices,null=True,blank=True,\
        verbose_name = 'Pot position')
    pot_placement_fk = models.ForeignKey('GraveGoodPlacement',null=True,blank=True)
    condition = models.CharField(max_length=2,choices=burial_pot_condition_choices,default='CP');    
    type = models.ForeignKey('PotType',null=True,blank=True,help_text='Possibly redundant field to be removed\
        after data migrated to new field')
    specific_type = models.CharField(max_length='2',null=True,blank=True,choices=burial_pot_type_choices,verbose_name\
        ='Type')
    pot_type_fk = models.ForeignKey('SpecificPotType',null=True,blank=True)
    burial = models.ForeignKey('Burials',related_name='Burial')
    raw_notes = models.TextField(null=True,blank=True)	
    def __str__(self):
        if self.pot_type_fk:
            return '%s (ID:%s)' % (self.pot_type_fk.description,str(self.id))
        return '%s (ID:%s)' % (self.description,str(self.id))
        
    def site_name_fake(self):
        return self.burial.site_fk.site_name

    def haystack_name(self):
        return 'pots'        

    def get_location(self):
        if self.burial.point:
            return Point(self.burial.point.x,self.burial.point.y)
        return Point(0,0)
        
    def get_geojson(self):
        string = ''
        try:
            if self.burial.point:
                string += '[' + str(self.burial.point.x) + ',' + str(self.burial.point.y) + ']'
                return string
        except Exception:
            pass
            return None        

class SpecificPotType(models.Model):
    description = models.CharField(max_length=50)
    short_code = models.CharField(max_length=10)
    major_type = models.ForeignKey('MajorPotType',null=True,blank=True)
    def __str__(self):
        return self.description

class MajorPotType(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description

        
class PotType(models.Model):
    description = models.CharField(max_length=50)
    short_code = models.CharField(max_length=10)
    def __str__(self):
        return self.description
        

class Script(models.Model):
    description = models.CharField(max_length=50)
    sub_type = models.ForeignKey('ScriptSubType',null=True,blank=True)
    def __str__(self):
        st = ''
        try:
            if self.sub_type:
                st = self.sub_type.description
        except Exception:
            st = ''
        return '%s, %s' % (self.description,st)

class ScriptSubType(models.Model):
    description = models.CharField(max_length=50)
    def __str__(self):
        return self.description		

class Language(models.Model):
    description = models.CharField(max_length=50)
    def __str__(self):
        return self.description


class NameForm(models.Model):
    description = models.CharField(max_length=50)
    def __str__(self):
       return self.description

    class Meta:
        verbose_name = 'Name formula'
        verbose_name_plural = 'Name formulae'

    @staticmethod
    def autocomplete_search_fields():
        return ("id_exact","description__icontains",)

class HoardType(models.Model):        
    description = models.CharField(max_length=50)
    def __str__(self):
        return self.description

        
class PeriodSummary(models.Model):
    description = models.CharField(max_length=50)
    def __str__(self):
        return self.description
		
class HoardMaterial(models.Model):
    description = models.CharField(max_length=50)
    def __str__(self):
        return self.description

class StelaeStoneShape(models.Model):
    description = models.CharField(max_length=50)
    def __str__(self):
        return self.description

class RockFamily(models.Model):
    description =  models.CharField(max_length=50)
    def __str__(self):
        return self.description

class RockType(models.Model):
    family = models.ForeignKey(RockFamily)
    description =  models.CharField(max_length=50)
    def __str__(self):
        return self.description

class SpecificRockType(models.Model):
    type = models.ForeignKey(RockType)
    description =  models.CharField(max_length=50)
    def __str__(self):
        return '%s, %s, %s' % (self.description,self.type,self.type.family)
    def short_name(self):
        return self.description

class HoardSpecificObject(models.Model):
    description = models.CharField(max_length=50)
    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',)

class HoardContextSummary(models.Model):
    description = models.CharField(max_length=50)
    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',)

class OgamImage(models.Model):
    description = models.CharField(max_length=100)
    ogam_fk = models.ForeignKey('OgamInscription')
    type = models.CharField(max_length=2,choices=ogam_image_type)
    image =  models.ImageField(upload_to='static/media/uploads/Ogam/')
    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',)



class MiscellaneousImage(models.Model):
    description = models.CharField(max_length=100)
    miscellaneous = models.ForeignKey('Miscellaneous')
    type = models.CharField(max_length=2,choices=ogam_image_type)
    image =  models.ImageField(upload_to='static/media/uploads/Misc/')
    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',)


class BurialImage(models.Model):
    description = models.CharField(max_length=200)
    burial_fk = models.ForeignKey('Burials')
    type = models.ForeignKey('BurialImageType',null=True,blank=True)
    image = models.ImageField(upload_to='static/media/uploads/Burial/')
    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',)

class HoardImage(models.Model):
    description = models.CharField(max_length=200)
    hoard_fk = models.ForeignKey('Hoards')
    image = models.ImageField(upload_to='static/media/uploads/Hoards/')
    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',)




class StelaeImage(models.Model):
    description = models.CharField(max_length=200)
    burial_fk = models.ForeignKey('Stelae')
    type = models.ForeignKey('StelaeImageType',null=True,blank=True)
    image = models.ImageField(upload_to='static/media/uploads/Stelae/')
    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',)

class StelaeImageType(models.Model):
    description = models.CharField(max_length=50)
    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',)

class BurialImageType(models.Model):
    description = models.CharField(max_length=50)
    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',)




class StelaeTechnique(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',)




class StoredQuery(models.Model):
    geojson_rep = models.TextField()

    def __str__(self):
        return self.id

		
class Discovery(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',)    


class LocationSummary(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',)
		
class StelaeType(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',) 
		
class TypeOfLand(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',) 
		
class HumanFigure(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',) 


class Motif(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',)    

class GeneralChronology(models.Model):
    description = models.CharField(max_length=100)
    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',)    

	
		
class Etymology(models.Model):
    inscription = models.ForeignKey('OgamInscription',related_name='inscription')
    type = models.ForeignKey('EtymologyType',null=True,blank=True)
    description = models.ForeignKey('EtymologyDescription',null=True,blank=True)
    comment =  models.CharField(max_length=250,null=True,blank=True)
    ### relocated fields	
    is_ogam = models.NullBooleanField()
    reference = models.CharField(max_length=100,null=True,blank=True) #Equiv to Source in previous Fernando data
    language = models.ForeignKey('Language',null=True,blank=True)
    leptonic  = models.CharField(max_length=100,null=True,blank=True,verbose_name="Lepontic")
    pie_etymology  = models.CharField(max_length=100,null=True,blank=True,verbose_name="PIE etymology")
    ie_etymology  = models.CharField(max_length=100,null=True,blank=True,verbose_name="IE etymology")
    gaulish  = models.CharField(max_length=1000,null=True,blank=True)
    proto_celtic_etymology  = models.CharField(max_length=1000,null=True,blank=True,verbose_name="Proto-Celtic etymology")
    celtic_etymology  = models.TextField(max_length=1000,null=True,blank=True,verbose_name="Celtic etymology")
    celtic_cognates = models.CharField(max_length=1000,null=True,blank=True) 
    galatian  = models.CharField(max_length=1000,null=True,blank=True)
    syntax  = models.CharField(max_length=1000,null=True,blank=True)
    semantic  = models.CharField(max_length=1000,null=True,blank=True)
    other_hispano_celtic  = models.CharField(max_length=1000,null=True,blank=True)
    phonology  = models.CharField(max_length=1000,null=True,blank=True)
    irish = models.CharField(max_length=1000,null=True,blank=True)
    welsh = models.CharField(max_length=1000,null=True,blank=True)   
    cornish = models.CharField(max_length=1000,null=True,blank=True)   
    breton = models.CharField(max_length=1000,null=True,blank=True)   
    cont_celtic = models.CharField(max_length=1000,null=True,blank=True)
    cumbric = models.CharField(max_length=1000,null=True,blank=True)
    brittonic = models.CharField(max_length=1000,null=True,blank=True)
    insular_celtic = models.CharField(max_length=1000,null=True,blank=True)
    pictish_celtic = models.CharField(max_length=1000,null=True,blank=True)
    scottish_gaelic = models.CharField(max_length=1000,null=True,blank=True)
    manx = models.CharField(max_length=1000,null=True,blank=True)
    goidelic = models.CharField(max_length=1000,null=True,blank=True)
    morphology  = models.TextField(max_length=1000,null=True,blank=True)    
    def __str__(self):
        return '%s' % self.description.description
    class Meta:
        ordering = ('description',)
        verbose_name_plural = 'Etymologies'

class EtymologyDescription(models.Model):
    simple_form = models.CharField(max_length=50,null=True,blank=True)
    description = models.CharField(max_length=50,verbose_name='Form')
    long_description = models.CharField(max_length=200,null=True,blank=True,verbose_name='Extended form')
    en_cognate = models.CharField(max_length=200,null=True,blank=True,verbose_name='English definition')
    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',)

class EtymologyType(models.Model):
    description = models.CharField(max_length=50)
    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',)

class SettlementType(models.Model):
    description = models.CharField(max_length=50)
    def __str__(self):
        return '%s' % self.description
    class Meta:
        ordering = ('description',)

class BurialDates(models.Model):
    burial = models.ForeignKey('Burials')
    approx_uncalibrated_date_bp = models.IntegerField()
    error_margin = models.IntegerField()
    def __str__(self):
        return '%s +/- %s'% (str(self.approx_uncalibrated_date_bp),str(self.error_margin))
    class Meta:
        ordering = ('approx_uncalibrated_date_bp','error_margin')

class BurialIndividualDates(models.Model):
    individual = models.ForeignKey('BurialIndividuals')
    approx_uncalibrated_date_bp = models.IntegerField()
    error_margin = models.IntegerField()
    def __str__(self):
        return '%s +/- %s'% (str(self.approx_uncalibrated_date_bp),str(self.error_margin))
    class Meta:
        ordering = ('approx_uncalibrated_date_bp','error_margin')        

        
class Bibliography(models.Model):
    reference = models.CharField(max_length=300,null=True,blank=True)
    year = models.IntegerField(null=True,blank=True)
    years = models.CharField(max_length=300,null=True,blank=True)
    title = models.TextField(null=True,blank=True)
    editors = models.TextField(null=True,blank=True)
    place_of_publication = models.CharField(max_length=300,null=True,blank=True)
    publisher = models.CharField(max_length=300,null=True,blank=True)
    no_of_pages = models.CharField(max_length=300,null=True,blank=True)
    volume = models.CharField(max_length=200,null=True,blank=True)    
    page_numbers = models.CharField(max_length=200,null=True,blank=True)    

    def __str__(self):
        return '%s, %s' % (self.title, self.editors)    