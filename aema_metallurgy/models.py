from django.db import models
# Create your models here.

from django.contrib.gis.db import models

from auxilliaryModels import *

# Create your models here.
		
class Metallurgy(models.Model):
    point = models.PointField(null=True,blank=True)
    objects = models.GeoManager()
    #
    oxford_database_code = models.IntegerField(null=True,blank=True)
    sam_lab_code_serial_number = models.IntegerField(null=True,blank=True)
    find_place = models.CharField(max_length=50)
    archaeological_context = models.CharField(max_length=100,null=True,blank=True)
    modern_country = models.CharField(max_length=50)
    country_code = models.CharField(max_length=10)
    regional_code = models.IntegerField(null=True,blank=True)
    site_id_number	= models.IntegerField(null=True,blank=True)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    object_type_code = models.IntegerField(null=True,blank=True)
    object_description = models.CharField(max_length=100,null=True,blank=True)
    object_category = models.CharField(max_length=100,null=True,blank=True)
    sangmeister_period = models.IntegerField(null=True,blank=True)
    sangmeister_period_expanded	= models.CharField(max_length=100,null=True,blank=True)
    oxford_period_summary = models.CharField(max_length=2,null=True,blank=True)
    Sn = models.FloatField(null=True,blank=True)
    Pb = models.FloatField(null=True,blank=True)
    As	= models.FloatField(null=True,blank=True)
    Sb = models.FloatField(null=True,blank=True)
    Ag	= models.FloatField(null=True,blank=True)
    Ni	= models.FloatField(null=True,blank=True)
    Bi	= models.FloatField(null=True,blank=True)
    Au	= models.FloatField(null=True,blank=True)
    Zn	= models.FloatField(null=True,blank=True)
    Co = models.FloatField(null=True,blank=True)
    Fe = models.FloatField(null=True,blank=True)
    oxford_copper_group	= models.IntegerField(null=True,blank=True)
    oxford_alloy_group	= models.CharField(max_length=35,null=True,blank=True)
    Adjusted_As	= models.FloatField(null=True,blank=True)
    Adjusted_Sb	= models.FloatField(null=True,blank=True)
    Adjusted_Ag	= models.FloatField(null=True,blank=True)
    Adjusted_Ni	= models.FloatField(null=True,blank=True)
    Adjusted_Bi	= models.FloatField(null=True,blank=True)
    Adjusted_Co	= models.FloatField(null=True,blank=True)
    Adjusted_Fe	= models.FloatField(null=True,blank=True)
	
    def __unicode__(self):
        return u'%s, %s' % ( str(self.oxford_database_code) , self.find_place )

    class Meta:
        ordering = ('oxford_database_code','id')
        verbose_name = 'Metallurgy'
        verbose_name_plural = 'Metallurgy records'		

    def save(self, *args, **kwargs):
        super(Metallurgy, self).save()

