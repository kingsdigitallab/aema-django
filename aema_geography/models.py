
from django.db import models
# Create your models here.
from django.contrib.gis.db import models

# This area of the database is for 
# collecting geographic extents from 
# previous projects


class RitualSitesIronAgeRoman(models.Model):
    # Spatial stuff
    point = models.PointField(null=True,blank=True)
    objects = models.GeoManager()
    # Regular stuff
    shape_id = models.IntegerField(null=True,blank=True)
    location = models.CharField(max_length=50,null=True,blank=True)
    count = models.IntegerField(null=True,blank=True)
    context = models.CharField(max_length=50,null=True,blank=True)
    contents = models.CharField(max_length=200,null=True,blank=True)
    description = models.CharField(max_length=150,null=True,blank=True)
    shape = models.CharField(max_length=30,null=True,blank=True)
    no_of_shr = models.CharField(max_length=30,null=True,blank=True)
    site_type = models.CharField(max_length=40,null=True,blank=True)
    species = models.CharField(max_length=60,null=True,blank=True)
    dating = models.CharField(max_length=50,null=True,blank=True)
    region = models.CharField(max_length=50,null=True,blank=True)
    def __unicode__(self):
        return self.description
    class Meta:
    	verbose_name = 'Ritual Sites - Iron Age/Roman'
      	verbose_name_plural = verbose_name

    def popup_content(self):
        str = '<p>'+self.location.__str__() +'</p><p>'+self.description.__str__() +'</p>'
        return str


class TribalRegalExtent(models.Model):
    # Spatial stuff
    polygon = models.MultiPolygonField(null=True,blank=True)
    objects = models.GeoManager()
    # Regular stuff
    description = models.CharField(max_length=50)

    def popup_content(self):
        return '<p>'+self.description+'</p>'


    class Meta:
    	verbose_name = 'Tribal and Royal influence'
    	verbose_name_plural = verbose_name


class Halsatt(models.Model):
    # Spatial stuff
    point = models.PointField(null=True,blank=True)
    objects = models.GeoManager()
    # Regular stuff
    location_desc = models.CharField(max_length=500,null=True,blank=True)
    description = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        verbose_name = 'Halsatt'
        verbose_name_plural = verbose_name



class GeojsonFile(models.Model):
    category = models.ForeignKey('GeojsonCategory',null=True,blank=True)
    short_description = models.CharField(max_length=100,null=True,blank=True)
    friendly_description = models.CharField(max_length=100,null=True,blank=True)
    file_path = models.CharField(max_length=500)
    def __unicode__(self):
        return self.friendly_description
    class Meta:
        ordering = ('friendly_description','category')

class GeojsonCategory(models.Model):
    short_description = models.CharField(max_length=100,null=True,blank=True)
    description = models.CharField(max_length=500,null=True,blank=True)
    major_category = models.ForeignKey('GeojsonMajorCategory',null=True,blank=True)
    def __unicode__(self):
        str = ''
        if self.major_category:
            str += self.major_category.description
        return u'%s (%s)' % (self.short_description,str)

class GeojsonMajorCategory(models.Model):
    description = models.CharField(max_length=30,null=True,blank=True)
    def __unicode__(self):
        return self.description




