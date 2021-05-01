# Create your models here.

from django.contrib.gis.db import models

from django.contrib.gis.geos import GEOSGeometry,Point

from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from django.utils.text import normalize_newlines


class Core(models.Model):						
    name = models.CharField(max_length=100,	null=True,blank=True)
    # GeoDjango-specific: a geometry field (PointField) and
    # overriding the default manager with a GeoManager instance.
    point = models.PointField(null=True,blank=True)
    objects = models.GeoManager()
    prn = models.IntegerField(null=True,blank=True)					
    wat = models.CharField(max_length=255,	null=True,blank=True)					
    watprn = models.CharField(max_length=255,	null=True,blank=True)					
    ngr = models.CharField(max_length=11,	null=True,blank=True)					
    ngrqual = models.CharField(max_length=50,	null=True,blank=True)					
    map = models.CharField(max_length=13,	null=True,blank=True)					
    unitary = models.CharField(max_length=25,	null=True,blank=True)					
    community = models.CharField(max_length=50,	null=True,blank=True)					
    status_typ = models.CharField(max_length=20,	null=True,blank=True)					
    status = models.CharField(max_length=40	 ,null=True,blank=True)					
    reference = models.CharField(max_length=75,	null=True,blank=True)					
    grade = models.CharField(max_length=3	 ,null=True,blank=True)					
    category = models.CharField(max_length=2	, null=True,blank=True)					
    condition = models.CharField(max_length=50	,	 null=True,blank=True)				
    broadclass = models.CharField(max_length=60	, null=True,blank=True)					
    type = models.CharField(max_length=50	 ,null=True,blank=True)					
    period = models.CharField(max_length=255	, null=True,blank=True)					
    periodspec = models.CharField(max_length=50	, null=True,blank=True)					
    century = models.CharField(max_length=50	, null=True,blank=True)					
    form = models.CharField(max_length=25	 ,null=True,blank=True)					
    desc_1 = models.TextField(null=True,blank=True)						
    compiledon = models.CharField(max_length=40,	 null=True,blank=True)					
    project = models.CharField(max_length=15,	 null=True,blank=True)					
    origin = models.CharField(max_length=10	, null=True,blank=True)					
    east = models.FloatField(null=True,	blank=True)					
    nrth = models.FloatField(null=True,	blank=True)
    # Temp field
    no_of_houses = models.IntegerField(null=True,blank=True)
    type_m2m = models.ManyToManyField('Type',blank=True)
					
    class Meta:
        verbose_name = "Core data"
        verbose_name_plural = "Core data"
    def __unicode__(self):
        return u'%s' % self.name

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
            
    def site_name_fake(self):
        return u'%s' %  self.name

    def haystack_name(self):
        return 'settlements'

    def popup_content(self):
        str = "<table><thead>"
        str += "<tr><th colspan='2'><a target='_blank' href='/view/settlements_full/" + \
            self.id.__str__() + "'>" + self.name + "</a></th></tr></thead><tbody>"
        str += "<tr><th>Type</th><td>"
        str += self.type
        str += "</td></tr>"
        if self.unitary:
            str += "<tr><th>Unitary</th><td>"
            str += self.unitary
            str += "</td></tr>"
        if self.period:
            str += "<tr><th>Period</th><td>"
            str += self.period
            str += "</td></tr>"            
        str += "</tbody></table>"
        return str
	
class HouseData(models.Model):						
    site_name = models.CharField(max_length=50,null=True,blank=True) 				
    prn = models.ForeignKey('Core',null=True,blank=True)					
    house_number = models.IntegerField(null=True,blank=True) 			
    house_location_id = models.CharField(max_length=50	,	 null=True,blank=True) 			
    radiocarbon_earliest = models.IntegerField(null=True	,	 blank=True) 			
    radiocarbon_latest = models.IntegerField(null=True	,	 blank=True) 			
    approx_early_date = models.CharField(max_length=50	,	 null=True,blank=True) 			
    approx_late_date = models.CharField(max_length=50	,	 null=True,blank=True) 			
    percent_excavated = models.CharField(max_length=50	,	 null=True,blank=True) 			
    internal_diameter = models.CharField(max_length=50	,	 null=True,blank=True) 			
    area = models.CharField(max_length=50	,	 null=True,blank=True)				
    shape = models.CharField(max_length=50	,	 null=True,blank=True)				
    repair = models.NullBooleanField(	 null=True,blank=True)				
    rebuild_of = models.IntegerField(null=True	,	 blank=True) 			
    details = models.CharField(max_length=255,	null=True,blank=True)			
    in_situ_decay = models.NullBooleanField(	 null=True,blank=True) 			
    post_removal = models.NullBooleanField(	 null=True,blank=True) 			
    wall_materials = models.TextField( null=True,blank=True) 				
    stake = models.NullBooleanField( null=True,blank=True)					
    wall_gully = models.NullBooleanField(	 null=True,blank=True) 			
    wall_slot = models.NullBooleanField(	 null=True,blank=True) 			
    plank_timber = models.NullBooleanField(	 null=True,blank=True) 			
    stone_wall = models.NullBooleanField(	 null=True,blank=True) 			
    cob_or_clay = models.NullBooleanField(	 null=True,blank=True) 			
    wattle = models.NullBooleanField(	 null=True,blank=True) 	
    rubble_or_earth_core = models.NullBooleanField(null=True,blank=True) 			
    post = models.NullBooleanField(	 null=True,blank=True)					
    turf = models.NullBooleanField(	 null=True,blank=True)					
    width_of_outer_wall = models.CharField(max_length=50	,	 null=True,blank=True) 			
    internal_post_ring = models.NullBooleanField(	 null=True,blank=True) 			
    other_features = models.CharField(max_length=50	,	 null=True,blank=True) 			
    peripery_width = models.CharField(max_length=50	,	 null=True,blank=True) 			
    periphery_area = models.CharField(max_length=50	,	 null=True,blank=True) 			
    central_zone_area = models.CharField(max_length=50	,	 null=True,blank=True) 			
    hearth = models.NullBooleanField(	 null=True,blank=True)				
    hearth_details = models.TextField(	 null=True,blank=True) 				
    internal_partitions = models.NullBooleanField(	 null=True,blank=True) 			
    floor_details = models.CharField(max_length=50	,	 null=True,blank=True) 			
    wear = models.NullBooleanField(	 null=True,blank=True)				
    drain = models.NullBooleanField(	 null=True,blank=True)				
    occ_deposits = models.NullBooleanField(	 null=True,blank=True) 			
    pits = models.NullBooleanField(	 null=True,blank=True)				
    postholes = models.NullBooleanField(	 null=True,blank=True)				
    stakeholes = models.NullBooleanField(	 null=True,blank=True)				
    other_feat = models.NullBooleanField(	 null=True,blank=True) 			
    details_other = models.CharField(max_length=50	,	 null=True,blank=True)				
    door_orient = models.CharField(max_length=50	,	 null=True,blank=True) 			
    ext_width = models.CharField(max_length=50	,	 null=True,blank=True) 			
    int_width = models.CharField(max_length=50	,	 null=True,blank=True) 			
    porch = models.NullBooleanField(null=True,blank=True)					
    door_2_orient = models.CharField(max_length=50	,	 null=True,blank=True) 			
    door_2_ext = models.CharField(max_length=50	,	 null=True,blank=True) 			
    door_2_int = models.CharField(max_length=50	,	 null=True,blank=True) 			
    porch_2 = models.NullBooleanField(	 null=True,blank=True) 			
    extra_doors = models.CharField(max_length=50	,	 null=True,blank=True) 			
    drainage_gully = models.NullBooleanField(	 null=True,blank=True) 			
    external_hearth = models.NullBooleanField(	 null=True,blank=True) 			
    annexe_details = models.CharField(max_length=50	,	 null=True,blank=True) 			
    lithics_and_production = models.CharField(max_length=50	,	 null=True,blank=True) 			
    querns_morts_g_stones = models.CharField(max_length=50	,	  null=True,blank=True) # Field renamed to remove spaces. Field name made lowercase.
    other_ground_stone = models.CharField(max_length=50	,	 null=True,blank=True) 			
    burnt_stone = models.CharField(max_length=50	,	 null=True,blank=True) 			
    vessels = models.CharField(max_length=50	,	 null=True,blank=True)				
    fine_wares = models.CharField(max_length=50	,	 null=True,blank=True) 			
    briquetage = models.CharField(max_length=50	,	 null=True,blank=True)				
    coins = models.CharField(max_length=50	,	 null=True,blank=True)				
    tools = models.CharField(max_length=50	,	 null=True,blank=True)				
    pers_adornment = models.CharField(max_length=50	,	 null=True,blank=True) 			
    dec_fittings = models.CharField(max_length=50	,	 null=True,blank=True) 			
    struct_fitt = models.CharField(max_length=50	,	 null=True,blank=True) 			
    weapon = models.CharField(max_length=50	,	 null=True,blank=True)				
    textile_prod = models.CharField(max_length=50	,	 null=True,blank=True) 			
    other_craft_prod = models.CharField(max_length=50	,	 null=True,blank=True) 			
    other_metal = models.CharField(max_length=50	,	 null=True,blank=True) 			
    metal_working_fe = models.CharField(max_length=50	,	 null=True,blank=True) 			
    metal_work_non_fe = models.CharField(max_length=50	,	 null=True,blank=True) 			
    metal_work_unk = models.CharField(max_length=50	,	 null=True,blank=True) 			
    other_finds = models.CharField(max_length=50	,	 null=True,blank=True) 			
    cbm = models.CharField(max_length=50	,	 null=True,blank=True)				
    human_bone = models.CharField(max_length=50	,	 null=True,blank=True) 			
    spec_dep = models.NullBooleanField(	 null=True,blank=True) 			
    location = models.CharField(max_length=50,	 null=True,blank=True)					
    nature = models.CharField(max_length=50	 ,null=True,blank=True)					
    plant = models.NullBooleanField(null=True,blank=True)					
    a_bone = models.NullBooleanField(	 null=True,blank=True) 			
    h_bone = models.NullBooleanField(	 null=True,blank=True) 			
    metal = models.NullBooleanField( null=True,blank=True)					
    pottery = models.NullBooleanField(null=True,blank=True)					
    stone = models.NullBooleanField(null=True,blank=True)					
    other = models.NullBooleanField(null=True,blank=True)					
    pre_house_activity = models.TextField(null=True,blank=True)
    after_use = models.TextField(	 null=True,blank=True) 				
    notes = models.TextField(null=True,blank=True)						
    links = models.CharField(max_length=50	, null=True,blank=True)					
    mapinfo_id = models.IntegerField(null=True	,	 blank=True)				
    class Meta:
        verbose_name = "House data"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return u'House data - %s' % self.prn.name	
						
						
class EnviroData(models.Model):						
    old_id = models.IntegerField(null=True	,	 blank=True)				
    prn = models.ForeignKey('Core',null=True,blank=True)
    house_number = models.IntegerField(null=True	,	 blank=True) 			
    site_name = models.CharField(max_length=50	,	 null=True,blank=True) 			
    pollen = models.CharField(max_length=50	,	 null=True,blank=True)				
    pre_landscape = models.CharField(max_length=50	,	 null=True,blank=True) # Field renamed to remove dashes. Field name made lowercase.				
    early_landscape = models.CharField(max_length=50	,	 null=True,blank=True) 			
    late_landscape = models.CharField(max_length=50	,	 null=True,blank=True) 			
    barley = models.NullBooleanField(	 null=True,blank=True)				
    emmer = models.NullBooleanField(	 null=True,blank=True)				
    spelt = models.NullBooleanField(	 null=True,blank=True)				
    rye = models.NullBooleanField(	 null=True,blank=True)				
    oats = models.NullBooleanField(	 null=True,blank=True)				
    wheat_sp = models.NullBooleanField(	 null=True,blank=True) 			
    bread_wheat = models.NullBooleanField(	 null=True,blank=True) 			
    pulses = models.NullBooleanField(	 null=True,blank=True)				
    flax = models.NullBooleanField(	 null=True,blank=True)				
    fruit = models.NullBooleanField(	 null=True,blank=True)				
    nuts = models.NullBooleanField(	 null=True,blank=True)				
    other_wild = models.TextField(null=True,blank=True) 				
    sheep_or_goat = models.NullBooleanField(	 null=True,blank=True) 			
    percent_sheep_or_goat = models.IntegerField(null=True	,	 blank=True) 			
    cow = models.NullBooleanField(	 null=True,blank=True)				
    percentage_cow = models.IntegerField(null=True	,	 blank=True) 			
    pig = models.NullBooleanField(	 null=True,blank=True)				
    percentage_pig = models.IntegerField(null=True	,	 blank=True) 			
    horse = models.NullBooleanField(	 null=True,blank=True)				
    percentage_horse = models.IntegerField(null=True	,	 blank=True) 			
    other_specify = models.CharField(max_length=50	,	 null=True,blank=True) 			
    wild_small_mammals = models.NullBooleanField(	 null=True,blank=True) 			
    deer = models.NullBooleanField(	 null=True,blank=True)				
    other_large_mammals = models.NullBooleanField(	 null=True,blank=True) 			
    birds = models.NullBooleanField(	 null=True,blank=True)				
    fish = models.NullBooleanField(	 null=True,blank=True)				
    shell_fish = models.NullBooleanField(	 null=True,blank=True) 			
    type_of_exploitation = models.CharField(max_length=50	,	 null=True,blank=True) 			
    soil_chemical_analysis = models.NullBooleanField(	 null=True,blank=True) 			
    good_chronological_res = models.CharField(max_length=50	,	 null=True,blank=True) 			
    notes = models.TextField(	 null=True,blank=True)					
    class Meta:
        verbose_name = "Enviro data"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return u'Enviro data - %s' % self.prn.name						
						
						
class GeneralInfo(models.Model):						
    sitename = models.CharField(max_length=255	, null=True,blank=True)					
    prn = models.ForeignKey('Core',null=True,blank=True)					
    standard_of_data = models.IntegerField(null=True	,	 blank=True) 			
    earlier_activity = models.CharField(max_length=255	,	 null=True,blank=True) 			
    later_activity = models.CharField(max_length=255	,	 null=True,blank=True) 			
    phase = models.CharField(max_length=255,	 null=True,blank=True)					
    related_to = models.CharField(max_length=255	,	 null=True,blank=True) 			
    radiocarbon_dated = models.NullBooleanField(	 null=True,blank=True) 			
    dated_by_finds = models.NullBooleanField(	 null=True,blank=True) 			
    other_dating = models.CharField(max_length=255	,	 null=True,blank=True) 			
    dimensions_ha = models.CharField(max_length=255	,	 null=True,blank=True) 			
    altitude_m_od = models.FloatField(null=True	,	 blank=True) 			
    altitude_range = models.CharField(max_length=255	,	 null=True,blank=True) 			
    slope_class = models.CharField(max_length=50	,	 null=True,blank=True) 			
    site_position = models.CharField(max_length=255	,	 null=True,blank=True) 			
    topography = models.CharField(max_length=255,	 null=True,blank=True)					
    aspect = models.CharField(max_length=255,	 null=True,blank=True)					
    landuse_today = models.CharField(max_length=255	,	 null=True,blank=True) 			
    class Meta:
        verbose_name = "General Information"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return u'General info - %s' % self.prn.name			
						
						
class SiteAttributes(models.Model):						
    prn = models.ForeignKey('Core',null=True,blank=True)				
    site_name = models.CharField(max_length=100	,	 null=True,blank=True) 			
    simple_site_type = models.CharField(max_length=255	,	 null=True,blank=True) 			
    settlement_sub_type = models.CharField(max_length=255	,	 null=True,blank=True) 			
    rcahmw_and_smith_site_classification = models.CharField(max_length=255	,	 null=True,blank=True) 			
    smith_sub_type = models.FloatField(null=True	,	 blank=True)
    hillfort_dims = models.FloatField(null=True,	 blank=True)					
    hillfort_shape = models.CharField(max_length=255	,	 null=True,blank=True) 			
    enclosure_type = models.CharField(max_length=255	,	 null=True,blank=True) 			
    ext_dimensions = models.FloatField(null=True	,	 blank=True) 			
    int_dimensions = models.FloatField(null=True	,	 blank=True) 			
    associated_fields = models.NullBooleanField(	 null=True,blank=True) 			
    curv_fields = models.NullBooleanField(	 null=True,blank=True)					
    terraced_fields = models.NullBooleanField(	 null=True,blank=True)					
    enclosure_materials = models.CharField(max_length=255	,	 null=True,blank=True) 			
    enclosure_feature_description = models.TextField(	 null=True,blank=True) 				
    no_enc_entrances = models.FloatField(null=True,	 blank=True)					
    enc_ent_orientation = models.CharField(max_length=50,	 null=True,blank=True)					
    enc_ent_type = models.CharField(max_length=255,	 null=True,blank=True)					
    enc_entrance_mat = models.CharField(max_length=255,	 null=True,blank=True)					
    ent_desc = models.TextField(null=True,blank=True)						
    annex_type = models.CharField(max_length=255,	 null=True,blank=True)					
    no_rhouses = models.IntegerField(null=True,	 blank=True)					
    no_longhuts = models.IntegerField(null=True,	 blank=True)					
    other = models.TextField(null=True,blank=True)						
    yard = models.CharField(max_length=1,	 null=True,blank=True)					
    special_dep_outside_houses = models.CharField(max_length=255	, null=True,blank=True)					
    hillfort_project_notes = models.TextField(	 null=True,blank=True) 				
    interp_comments = models.TextField(	 null=True,blank=True)					
    class Meta:
        verbose_name = "Site attributes"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return u'Attributes - %s' % self.prn.name
						
class RadioCarbonDates(models.Model):
    site_name = models.CharField(max_length=100	,	 null=True,blank=True) 			
    prn = models.ForeignKey('Core',null=True,blank=True)					
    house_number = models.IntegerField(null=True	,	 blank=True) 			
    lab_number = models.CharField(max_length=100	,	 null=True,blank=True) 			
    raw_date_bp = models.IntegerField(null=True	,	 blank=True) 			
    error = models.IntegerField(null=True	,	 blank=True) 			
    calibrated_date  = models.CharField(max_length=50	,	 null=True,blank=True) 			
    date_68_pc_low = models.IntegerField(null=True	,	 blank=True) 			
    date_68_pc_high = models.IntegerField(null=True	,	 blank=True) 			
    date_95_pc_low = models.IntegerField(null=True	,	 blank=True) 			
    date_95Pc_high = models.IntegerField(null=True	,	 blank=True) 			
    sample_location  = models.CharField(max_length=100	,	 null=True,blank=True) 			
    sample_material  = models.CharField(max_length=100	,	 null=True,blank=True) 		
    comment  = models.CharField(max_length=255	,	 null=True,blank=True) 			
    class Meta:
        verbose_name = "Radio Carbon Dates"
        verbose_name_plural = "Radio Carbon Dates"
    def __unicode__(self):
        return u'RC dates - %s' % self.prn.name
	
class Finds(models.Model):						
    finds_assemblage_id = models.IntegerField(null=True	,	 blank=True) 			
    prn = models.ForeignKey('Core',null=True,blank=True)					
    site_name = models.CharField(max_length=255	,	 null=True,blank=True) 			
    watprn = models.CharField(max_length=255,	 null=True,blank=True)					
    quantity = models.CharField(max_length=255,	 null=True,blank=True)					
    ftype = models.CharField(max_length=255,	 null=True,blank=True)					
    fmaterial = models.CharField(max_length=255,	 null=True,blank=True)					
    datefound = models.CharField(max_length=255	, null=True,blank=True)					
    fnotes = models.CharField(max_length=255	, null=True,blank=True)					
    flocation = models.CharField(max_length=255	, null=True,blank=True)					
    accno = models.CharField(max_length=255	, null=True,blank=True)					
    bibliogref = models.CharField(max_length=255	, null=True,blank=True)					
    animal_bone = models.NullBooleanField(	 null=True,blank=True) 			
    human_bone = models.NullBooleanField(	 null=True,blank=True) 			
    pottery = models.NullBooleanField( null=True,blank=True)					
    fired_clay = models.NullBooleanField(	 null=True,blank=True) 			
    stone = models.NullBooleanField(	 null=True,blank=True)					
    burnt_stone_flint = models.NullBooleanField(	 null=True,blank=True) 			
    plant_macro = models.NullBooleanField(	 null=True,blank=True) 			
    charcoal = models.NullBooleanField(	 null=True,blank=True)					
    struck_worked_flint = models.NullBooleanField(	 null=True,blank=True) 			
    worked_stone = models.NullBooleanField(	 null=True,blank=True) 			
    vessels = models.NullBooleanField( null=True,blank=True)					
    finewares = models.NullBooleanField(	 null=True,blank=True)					
    briquetage = models.NullBooleanField(	 null=True,blank=True)					
    cbm = models.NullBooleanField(	 null=True,blank=True)				
    copper_alloy = models.NullBooleanField(	 null=True,blank=True)
    fe = models.NullBooleanField( null=True,blank=True)					
    pb = models.NullBooleanField( null=True,blank=True)					
    other_metal = models.NullBooleanField(	 null=True,blank=True) 			
    other_finds = models.NullBooleanField(	 null=True,blank=True) 			
    is_quantifiable_data_available = models.NullBooleanField(	 null=True,blank=True) 			
    coins = models.NullBooleanField(	 null=True,blank=True)					
    personal_adornment = models.NullBooleanField(	 null=True,blank=True) 			
    decorative_fittings = models.NullBooleanField(	 null=True,blank=True) 			
    tools = models.NullBooleanField(	 null=True,blank=True) 			
    weapons = models.NullBooleanField(	 null=True,blank=True) 			
    metal_objects = models.NullBooleanField(	 null=True,blank=True) 			
    craft_production = models.NullBooleanField(	 null=True,blank=True) 			
    textile_production = models.NullBooleanField(	 null=True,blank=True) 			
    craft_working = models.NullBooleanField(	 null=True,blank=True) 			
    fe_metalworking = models.NullBooleanField(	 null=True,blank=True) 			
    non_fe_metalworking = models.NullBooleanField(	 null=True,blank=True) 
    other_metalworking = models.NullBooleanField(	 null=True,blank=True) 			
    notes = models.TextField(null=True,blank=True)						
    class Meta:
        verbose_name = "Find"
        verbose_name_plural = "Find"
    def __unicode__(self):
        return u'Find - %s' % self.prn.name
						
class Sources(models.Model):						
    source_id = models.IntegerField(null=True,		 blank=True) 			
    prn = models.ForeignKey('Core',null=True,blank=True)				
    wat = models.CharField(max_length=255,	 null=True,blank=True)					
    watprn = models.CharField(max_length=255	, null=True,blank=True)					
    site_name = models.CharField(max_length=255	, null=True,blank=True) 			
    author = models.CharField(max_length=255,	 null=True,blank=True)					
    year = models.CharField(max_length=255,	 null=True,blank=True)					
    artcl_titl = models.CharField(max_length=255,	 null=True,blank=True)					
    title = models.CharField(max_length=255	, null=True,blank=True)					
    roundhouse_project_references = models.CharField(max_length=255,		 null=True,blank=True) 			
    other = models.CharField(max_length=255	, null=True,blank=True)					
    srcetype = models.CharField(max_length=255,	 null=True,blank=True)					
    collection = models.CharField(max_length=255,	 null=True,blank=True)					
    gw_bibref = models.CharField(max_length=255	, null=True,blank=True)					
    class Meta:
        verbose_name = "Source"
        verbose_name_plural = "Sources"
    def __unicode__(self):
        return u'Source - %s' % self.prn.name



        
class Type(models.Model):
    description = models.CharField(max_length=80)
    sub_type = models.ForeignKey('SubType',null=True,blank=True)
    def __unicode__(self):
        return u'%s' % self.description

class SubType(models.Model):
    description = models.CharField(max_length=80)
    def __unicode__(self):
        return u'%s' % self.description						
						
						
						
						
						
						
						
