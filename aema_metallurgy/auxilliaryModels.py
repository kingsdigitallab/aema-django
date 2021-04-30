# Create your models here.

from django.contrib.gis.db import models

# Models to contains aggregate values from Metallurgy
# that should be updated on save?

class PalstaveAverageValues(models.Model):
    average_sn = models.FloatField(null=True,blank=True)
    average_pb = models.FloatField(null=True,blank=True)
    def __unicode__(self):
        return ('Sn: %s, Pb: %s') % (self.average_sn,self.average_pb)
    

	

