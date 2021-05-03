from django.contrib.gis import admin
from django import forms
from django.contrib.admin import TabularInline, StackedInline, ModelAdmin
from .models import *
from .auxilliaryModels import *

from .forms import MflcForm


class LanguageAdmin(admin.OSMGeoAdmin):
    pass


class EtymologyInline(StackedInline):
    model = Etymology
    fieldsets = (
        ('General', {
            'fields': ('phonology', 'morphology', 'syntax', 'semantic'),
            'classes': ('collapse-open',)
        }),
        ('Mandatory', {
            'fields': (
            'type', 'description', 'comment', 'is_ogam', 'reference',
            'language'),
            'classes': ('collapse-open',)
        }),
        ('Core etymologies', {
            'fields': (
            'ie_etymology', 'proto_celtic_etymology', 'celtic_etymology',
            'celtic_cognates'),
            'classes': ('collapse-open',)
        }),
        ('Etymologies A', {
            'fields': (
            'cont_celtic', 'leptonic', 'other_hispano_celtic', 'gaulish'),
            'classes': ('collapse-open',)
        }),
        ('Etymologies B', {
            'fields': (
            'insular_celtic', 'brittonic', 'welsh', 'cornish', 'cumbric', \
            'pictish_celtic', 'breton', 'goidelic', 'irish', 'scottish_gaelic',
            'manx'),
            'classes': ('collapse-open',)
        }),
    )


class BurialDateInline(StackedInline):
    model = BurialDates
    extra = 1


class BurialIndividualDateInline(StackedInline):
    model = BurialIndividualDates
    extra = 1


class BurialImageInline(StackedInline):
    model = BurialImage


class StelaeImageInline(StackedInline):
    model = StelaeImage


class HoardImageInline(StackedInline):
    model = HoardImage


class MiscImageInline(StackedInline):
    model = MiscellaneousImage


class OgamImageInline(StackedInline):
    model = OgamImage

    class Media:
        js = ['/static/js/display_admin_images.js', ]


class GraveGoodInlineAdmin(StackedInline):
    model = GraveGood
    filter_horizontal = ('raw_materials_m2m',)
    exclude = ('type', 'raw_notes', 'functional_type', 'placement')
    raw_id_fields = ('functional_type_fk', 'placement_fk')
    extra = 1


class PotInlineAdmin(StackedInline):
    model = Pot
    exclude = ('specific_type', 'raw_notes', 'pot_placement', 'count', 'type')
    raw_id_fields = ('pot_type_fk', 'pot_placement_fk')
    extra = 1


class DatingInLine(StackedInline):
    model = Dating
    raw_id_fields = ('organic_material',)
    extra = 1


class ToponymAdmin(admin.OSMGeoAdmin):
    exclude = ('object',)


class OgamInscriptionInlineAdmin(StackedInline):
    form = MflcForm
    model = OgamInscription
    extra = 3
    # exclude = ('other_hispano_celtic_2','cont_celtic_2','pictish_celtic_2','scottish_gaelic_2','language')


class OgamInscriptionAdmin(admin.OSMGeoAdmin):
    raw_id_fields = ('ogamsite_fk',)
    list_display = ('id', 'name', 'name_clean', 'etymology', 'mod_province')
    model = OgamInscription
    search_fields = ('name', 'findspot')
    exclude = ('other_hispano_celtic_2', 'cont_celtic_2', 'pictish_celtic_2',
               'scottish_gaelic_2', 'language')
    inlines = [EtymologyInline, OgamImageInline]
    fieldsets = (
        ('General', {
            'fields': (
            'ogamsite_fk', 'name', 'name_clean', 'toponym', 'script_fk' \
                , 'language_fk', 'language_of_inscription', 'reference',
            'comment', 'chronology' \
                , 'materials'),
            'classes': ('collapse-open',)
        }),
        ('Relocated fields', {
            'fields': ('leptonic', 'pie_etymology', 'ie_etymology', 'gaulish', \
                       'proto_celtic_etymology', 'celtic_etymology',
                       'celtic_cognates', 'irish' \
                           , 'galatian', 'morphology', 'syntax', 'semantic',
                       'other_hispano_celtic' \
                           , 'phonology', 'script', 'welsh', 'cornish',
                       'breton', 'cont_celtic' \
                           , 'cumbric', 'brittonic', 'insular_celtic',
                       'pictish_celtic' \
                           , 'scottish_gaelic', 'manx', 'goidelic'),
            'classes': ('collapse-closed',)
        }),
    )

    class Media:
        geocodefield = 'point'
        js = ['/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', \
              '/static/js/define_tinymce_fields.js', \
              '/static/grappelli/tinymce_setup/tinymce_setup.js']


class BurialIndividualMain(admin.OSMGeoAdmin):
    filter_horizontal = ('grave_good_m2m', 'pot_m2m')
    raw_id_fields = (
    'organic_material_fk', 'position_fk', 'grave_good_m2m', 'pot_m2m',
    'burial')
    exclude = ('position', 'raw_notes')
    inlines = [BurialIndividualDateInline, ]


class BurialIndividualAdmin(StackedInline):
    filter_horizontal = ('grave_good_m2m', 'pot_m2m')
    model = BurialIndividuals
    extra = 1
    raw_id_fields = ('organic_material_fk', 'position_fk')
    exclude = ('position', 'raw_notes')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "grave_good_m2m":
            try:
                parent_id = int(request.META['PATH_INFO'].split('/')[4])
                kwargs["queryset"] = GraveGood.objects.filter(
                    burial_id=parent_id)
            except ValueError:
                #  By default return an empty queryset
                kwargs["queryset"] = GraveGood.objects.none()
            return super(BurialIndividualAdmin, self).formfield_for_manytomany(
                db_field, request, **kwargs)
        if db_field.name == "pot_m2m":
            try:
                parent_id = int(request.META['PATH_INFO'].split('/')[4])
                kwargs["queryset"] = Pot.objects.filter(burial_id=parent_id)
            except ValueError:
                kwargs["queryset"] = Pot.objects.none()
            return super(BurialIndividualAdmin, self).formfield_for_manytomany(
                db_field, request, **kwargs)


class BurialAdmin(admin.OSMGeoAdmin):
    list_display = ('id', 'site_fk', 'area_related', 'site_type', 'date_ref')
    search_fields = (
    'site_fk__site_name', 'date_ref', 'site_type_specific__description')
    filter_horizontal = ('site_type_m2m', 'site_type_specific', 'gender_m2m',
                         'grave_good_class_m2m')
    raw_id_fields = ('site_fk', 'organic_material_fk')

    def area_related(self, obj):
        try:
            return obj.site_fk.area_fk
        except Exception:
            return ''

    area_related.admin_order_field = 'site_fk__area_fk'
    fieldsets = (
        ('Location', {
            'fields': ('site_fk', 'lat', 'lon', 'point'),
            'classes': ('collapse-open',)
        }),
        ('Site details', {
            'fields': (
            'site_type_m2m', 'site_type_specific', 'cemetery', 'usage',
            'funerary_context', \
            'minimum_no_individuals', 'biblio_for_site'),
            'classes': ('collapse-closed',)
        }),
        ('Burial details', {
            'fields': (
            'burial_type', 'burial_summary', 'skeleton_summary', 'gender_m2m',
            'age',),
            'classes': ('collapse-closed',)
        }),
        ('Dating', {
            'fields': ('general_chronology', 'general_chronology_fk',
                       'organic_material_fk', 'date_ref', 'date_summary',
                       'calibrated_date_bc_2_sigma', 'uncalibrated_date_bp',
                       'uncalibrated_date_bc', \
                       'calibrated_date_bc_2_sigma_repeated_field'),
            'classes': ('collapse-closed',)
        }),
        ('Grave goods', {
            'fields': ('grave_good_short_summary', 'grave_good_class_m2m',
                       'no_of_grave_goods', 'pot_type', 'pot_type_summary'),
            'classes': ('collapse-closed',)
        }),
    )
    inlines = [BurialImageInline, PotInlineAdmin, GraveGoodInlineAdmin,
               BurialIndividualAdmin, DatingInLine, ]

    class Media:
        geocodefield = 'point'
        js = ['/geofield/%s/geocode.js' % (geocodefield), \
              '/static/js/proj4js/lib/proj4js-compressed.js', \
              '/static/js/burial_admin_customisations.js']


class OgamAdmin(admin.OSMGeoAdmin):
    list_display = (
    'id', 'site_fk', 'ancient_name', 'number', 'script_fk', 'language_fk')
    search_fields = ('site_fk__site_name', 'province', 'number', 'text')
    filter_horizontal = ('name_forms_present',)
    fieldsets = (
        ('Location', {
            'fields': (
            'site', 'site_fk', 'ancient_name', 'point', 'lat', 'lon',
            'coords'),
            'classes': ('collapse-open',)
        }),
        ('Details', {
            'fields': (
            'context', 'script_fk', 'language_fk', 'language', 'text',
            'expansion', 'contains_pn_bool', \
            'name_forms_present', 'nf', 'comment', 'date'),
            'classes': ('collapse-closed',)
        }),
    )

    class Media:
        geocodefield = 'point'
        js = ['/geofield/%s/geocode.js' % (geocodefield), \
              '/static/js/proj4js/lib/proj4js-compressed.js', \
              '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', \
              '/static/js/define_tinymce_fields.js', \
              '/static/grappelli/tinymce_setup/tinymce_setup.js']


class OgamSiteAdmin(admin.OSMGeoAdmin):
    list_display = ('id', 'ancient_name', 'number', 'language_fk', 'site_fk')
    search_fields = ('site_fk__site_name', 'province', 'number',)
    filter_horizontal = ('name_forms_present',)
    raw_id_fields = ('site_fk',)
    fieldsets = (
        ('Location', {
            'fields': (
            'site', 'province', 'site_fk', 'ancient_name', 'point', 'lat',
            'lon', 'coords'),
            'classes': ('collapse-open',)
        }),
        ('Details context', {
            'fields': ('full_text', 'expanded_text',  # 'meaning','etymology',\
                       'context_description', 'context_macro',
                       'context_macro_free_text', \
                       'context_micro', 'context_micro_free_text',
                       'context_secondary', 'context_secondary_text'),
            'classes': ('collapse-closed',)
        }),
    )

    inlines = [OgamInscriptionInlineAdmin, ]

    # class Media:
    #    geocodefield = 'point'
    #    js = ['/geofield/%s/geocode.js' % (geocodefield),\
    #    '/static/js/proj4js/lib/proj4js-compressed.js']  
    class Media:
        geocodefield = 'point'
        js = ['/geofield/%s/geocode.js' % (geocodefield), \
              '/static/js/proj4js/lib/proj4js-compressed.js', \
              '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', \
              '/static/js/define_tinymce_fields.js', \
              '/static/grappelli/tinymce_setup/tinymce_setup.js']


class StelaeAdmin(admin.OSMGeoAdmin):
    inlines = [StelaeImageInline, ]
    list_display = ('id', 'site_fk', 'area_related')

    def area_related(self, obj):
        try:
            return obj.site_fk.area_fk
        except Exception:
            return ''

    area_related.admin_order_field = 'site_fk__area_fk'
    raw_id_fields = ('site_fk', 'specific_stone_type', 'discovery')
    search_fields = ('site_fk__site_name', 'area', 'region')
    filter_horizontal = (
    'stone_shape_m2m', 'technique_m2m', 'location_summary', \
    'type_of_land', 'stelae_type', 'human_figure_m2m', 'motif')
    exclude = (
    'human_figure', 'human_figure_bool', 'lance_spear', 'lance_spear_bool',
    'sword', 'sword_bool', \
    'shield', 'shield_bool', 'bow_and_arrow_bool', 'bow_and_arrow',
    'wheeled_vehicle', \
    'wheeled_vehicle_bool', 'quadropeds_animals_bool', 'quadroped_bool',
    'mirror', \
    'mirror_bool', 'fibula', 'fibula_bool', 'comb', 'comb_bool', 'ornaments',
    'ornaments_bool', 'headdress', \
    'headdress_bool', 'helmet', 'helmet_bool', 'musical_instrument',
    'musical_instrument_bool', 'circles_cup_and_rings',
    'circles_cup_and_rings_bool')
    fieldsets = (
        ('Location', {
            'fields': (
            'site_name', 'location_description', 'site_fk', 'area', 'region',
            'lon', 'lat', 'point'),
            'classes': ('collapse-open',)
        }),
        ('Stelae details', {
            'fields': ('general_description', 'stone_shape', 'stone_shape_m2m',
                       'condition', 'technique_of_creation', 'technique_m2m',
                       'stone_type_and_description', \
                       'specific_stone_type', 'motif_overview', \
                       'no_of_motifs', 'summary_of_human_figure',
                       'musical_instrument_description', \
                       'spearhead_location', \
                       'helmet_type', 'sword_summary', 'shield_summary',
                       'shield_location', \
                       'bow_and_arrow_description', \
                       'quadroped_summary', 'vehicle_composition', \
                       'circle_etc_description', 'other_motifs', \
                       'unusual_motifs', 're_use', 're_use_bool',
                       'additional_features', 'additional_features_bool', \
                       'disposition_of_human_in_relation_to_other_motifs'),
            'classes': ('collapse-closed',)
        }),
        ('New fields', {
            'fields': ('discovery', 'location_summary', 'summary_location', \
                       'stelae_type', 'stelae_type_raw', 'type_of_land',
                       'type_of_land_raw', \
                       'human_figure_m2m', 'human_figure_m2m_raw', 'motif'),
            'classes': ('collapse-closed',)
        }),
        ('Chronology and Bibliography', {
            'fields': ('bibliography', 'chronology', 'chronology_fk',
                       'chronology_start_bc', 'chronology_end_bc'),
            'classes': ('collapse-closed',)
        }),
    )

    class Media:
        geocodefield = 'point'
        js = ['/geofield/%s/geocode.js' % (geocodefield), \
              '/static/js/proj4js/lib/proj4js-compressed.js']


class OgamFernandoRawAdmin(admin.OSMGeoAdmin):
    list_display = ('id', 'word', 'source', 'findspot')
    search_fields = ('word', 'source', 'findspot')


class AbrazoFernandoRawAdmin(admin.OSMGeoAdmin):
    filter_horizontal = ('etymologydescription', 'toponyms')
    # list_display = ('id','word','source',)
    search_fields = ('word', 'source', 'context')
    exclude = ('cont_celtic_2', 'pictish_celtic_2', 'scottish_gaelic_2',
               'other_hispano_celtic_2')
    fieldsets = [
        ('General',
         {'fields': ['word', 'toponyms', 'etymologydescription' \
             , 'nr', 'source', 'context', 'script']}),
        ('Linguistic',
         {'fields': ['phonology', 'morphology', 'syntax', 'semantic']}),
        ('Etymology',
         {'fields': ['pie_etymology', 'ie_etymology', 'proto_celtic_etymology',
                     'celtic_etymology', 'celtic_cognates']}),
        ('Language group 1',
         {'fields': ['cont_celtic', 'leptonic', 'other_hispano_celtic',
                     'gaulish', 'galatian']}),
        ('Language group 2',
         {'fields': ['insular_celtic', 'brittonic', 'welsh', 'cumbric',
                     'pictish_celtic', \
                     'breton', 'goidelic', 'irish', 'scottish_gaelic', 'manx',
                     'cornish']}),
        ('Reference and materials',
         {'fields': ['materials', 'type', 'dates', 'bibliography']}),
        ('Location',
         {'fields': ['findspot', 'mod_province', 'lon', 'lat', 'point']}),
    ]

    class Media:
        geocodefield = 'point'
        js = ['/geofield/%s/geocode.js' % (geocodefield), \
              '/static/js/proj4js/lib/proj4js-compressed.js']


class OrganicMaterialAdmin(admin.OSMGeoAdmin):
    fields = ('master', 'sub_class')
    model = OrganicMaterial


class BasicAdmin(ModelAdmin):
    pass


class SiteAdmin(ModelAdmin):
    list_display = ('id', 'site_name', 'area_fk', '__str__')
    search_fields = ('site_name',)
    raw_id_fields = ('area_fk',)
    exclude = ('region', 'country', 'area')


class AreaAdmin(admin.OSMGeoAdmin):
    list_display = ('id', 'area_name', '__str__')
    search_fields = ('area_name',)
    raw_id_fields = ('region_fk',)
    exclude = ('region', 'country')


class RegionAdmin(admin.OSMGeoAdmin):
    list_display = ('id', 'region_name', '__str__')
    search_fields = ('region_name',)
    raw_id_fields = ('country_fk',)
    exclude = ('country',)


class CountryAdmin(admin.OSMGeoAdmin):
    list_display = ('id', 'country_name', '__str__')
    search_fields = ('country_name',)


class NameFormAdmin(admin.OSMGeoAdmin):
    pass


class GraveGoodRawMaterialAdmin(admin.OSMGeoAdmin):
    pass


class SpecificPotTypeAdmin(admin.OSMGeoAdmin):
    list_display = ('id', 'description', 'major_type')
    # pass#fields = ('description',)


class HoardsAdmin(admin.OSMGeoAdmin):
    filter_horizontal = (
    'material_type_fk', 'general_type_m2m', 'specific_object_type_m2m',
    'context_summary_m2m')
    list_display = (
    'id', 'site_fk', 'area_related', 'object_condition_summary_choice')

    def area_related(self, obj):
        try:
            return obj.site_fk.area_fk
        except Exception:
            return ''

    area_related.admin_order_field = 'site_fk__area_fk'
    search_fields = (
    'site_fk__site_name', 'area', 'region', 'object_condition_summary_choice')
    raw_id_fields = ('site_fk',)
    fieldsets = (
        ('Location', {
            'fields': ('site_fk', 'lat', 'lon', 'point',),
            'classes': ('collapse-open',)
        }),
        ('Details', {
            'fields': (
            'deposit_overview', 'deposit_context', 'no_of_objects_cleaned',
            'no_of_objects_clustered_choice' \
                , 'find_type_cleaned', 'material_type_fk', 'general_type_m2m',
            'specific_object_description' \
                , 'specific_object_type_m2m', 'arrangement_of_objects',
            'object_condition_summary_choice' \
                , 'dry_wet_context_choice', 'metal_analysis_summary_1',
            'context_summary', 'context_summary_m2m', 'notes'),
            'classes': ('collapse-closed',)
        }),
        ('Chronology and Bibliography', {
            'fields': (
            'chronology_date_bracket_BC', 'chronology_start_date_BC',
            'chronoloy_end_date_BC' \
                , 'regional_period_phase', 'period_summary_fk', 'c14_dates',
            'refs'),
            'classes': ('collapse-closed',)
        }),
    )
    inlines = [HoardImageInline, ]

    class Media:
        geocodefield = 'point'
        js = ['/geofield/%s/geocode.js' % (geocodefield), \
              '/static/js/proj4js/lib/proj4js-compressed.js']


class MiscellaneousAdmin(admin.OSMGeoAdmin):
    filter_horizontal = (
    'material_type_fk', 'general_type_m2m', 'specific_object_type_m2m',
    'context_summary_m2m')
    list_display = (
    'id', 'site_fk', 'area_related', 'object_condition_summary_choice')

    def area_related(self, obj):
        try:
            return obj.site_fk.area_fk
        except Exception:
            return ''

    area_related.admin_order_field = 'site_fk__area_fk'
    search_fields = (
    'site_fk__site_name', 'area', 'region', 'object_condition_summary_choice')
    raw_id_fields = ('site_fk',)
    fieldsets = (
        ('Location', {
            'fields': ('site_fk', 'lat', 'lon', 'point',),
            'classes': ('collapse-open',)
        }),
        ('Details', {
            'fields': (
            'deposit_overview', 'deposit_context', 'no_of_objects_cleaned',
            'no_of_objects_clustered_choice' \
                , 'find_type_cleaned', 'material_type_fk', 'general_type_m2m',
            'specific_object_description' \
                , 'specific_object_type_m2m', 'arrangement_of_objects',
            'object_condition_summary_choice' \
                , 'dry_wet_context_choice', 'material_analysis_summary',
            'context_summary', 'context_summary_m2m', 'notes'),
            'classes': ('collapse-closed',)
        }),
        ('Chronology and Bibliography', {
            'fields': (
            'chronology_date_bracket_BC', 'chronology_start_date_BC',
            'chronoloy_end_date_BC' \
                , 'regional_period_phase', 'period_summary_fk', 'c14_dates',
            'refs'),
            'classes': ('collapse-closed',)
        }),
    )
    inlines = [MiscImageInline, ]

    class Media:
        geocodefield = 'point'
        js = ['/geofield/%s/geocode.js' % (geocodefield), \
              '/static/js/proj4js/lib/proj4js-compressed.js']


admin.site.register(HoardMaterial, LanguageAdmin)
admin.site.register(HoardType, LanguageAdmin)
admin.site.register(BurialImageType, LanguageAdmin)

admin.site.register(HoardContextSummary)
admin.site.register(HoardSpecificObject, LanguageAdmin)
admin.site.register(Burials, BurialAdmin)
admin.site.register(Stelae, StelaeAdmin)
# admin.site.register(Ogam, OgamAdmin)
admin.site.register(OgamSite, OgamSiteAdmin)
admin.site.register(Hoards, HoardsAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(SpecificPotType, SpecificPotTypeAdmin)
admin.site.register(MajorPotType, NameFormAdmin)

admin.site.register(Site, SiteAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(NameForm, NameFormAdmin)
admin.site.register(GraveGoodRawMaterialType, GraveGoodRawMaterialAdmin)

admin.site.register(OrganicMaterial, OrganicMaterialAdmin)
admin.site.register(OrganicMaterialSubClass, admin.GeoModelAdmin)
admin.site.register(OrganicMaterialMaster, admin.GeoModelAdmin)
admin.site.register(SiteTypeSpecific, admin.GeoModelAdmin)
admin.site.register(StelaeStoneShape, admin.GeoModelAdmin)
admin.site.register(SpecificRockType, admin.GeoModelAdmin)
admin.site.register(GraveGoodFunctionalType, admin.GeoModelAdmin)
admin.site.register(BurialPosition, admin.GeoModelAdmin)
admin.site.register(Script, admin.GeoModelAdmin)
admin.site.register(ScriptSubType, admin.GeoModelAdmin)
admin.site.register(GraveGoodPlacement, admin.GeoModelAdmin,
                    exclude=('short_desc',))

admin.site.register(LocationSummary, admin.GeoModelAdmin)

admin.site.register(HumanFigure, admin.GeoModelAdmin)
admin.site.register(TypeOfLand, admin.GeoModelAdmin)
admin.site.register(StelaeType, admin.GeoModelAdmin)
admin.site.register(Motif, admin.GeoModelAdmin)
admin.site.register(StelaeTechnique, admin.GeoModelAdmin)

# Basic Admins to be modified
# admin.site.register(OgamFernandoRaw, OgamFernandoRawAdmin)
admin.site.register(AbrazoFernandoRaw, AbrazoFernandoRawAdmin)

# admin.site.register(AbrazoFernandoRaw, BasicAdmin)

admin.site.register(OgamInscription, OgamInscriptionAdmin)
admin.site.register(Discovery, admin.GeoModelAdmin)
admin.site.register(GeneralChronology, BasicAdmin)

admin.site.register(EtymologyDescription, BasicAdmin)
admin.site.register(EtymologyType, BasicAdmin)
admin.site.register(Toponyms, ToponymAdmin)
admin.site.register(SettlementType, BasicAdmin)
# admin.site.register(SpecificPotType,BasicAdmin)
# admin.site.register(Ab_to_Etym,BasicAdmin)
# admin.site.register(Ab_to_Topo,BasicAdmin)
admin.site.register(BurialIndividuals, BurialIndividualMain)

admin.site.register(Pot, BasicAdmin)
admin.site.register(PeriodSummary, BasicAdmin)
admin.site.register(GraveGood, BasicAdmin)

admin.site.register(Bibliography, BasicAdmin)

admin.site.register(Miscellaneous, MiscellaneousAdmin)

# admin.site.register(GraveGoodPlacement,BasicAdmin)
