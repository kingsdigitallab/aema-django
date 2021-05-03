# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aema_db', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abrazofernandoraw',
            name='etymologydescription',
            field=models.ManyToManyField(verbose_name='Etymology description', to='aema_db.EtymologyDescription'),
        ),
        migrations.AlterField(
            model_name='burialimage',
            name='image',
            field=models.ImageField(upload_to='static/media/uploads/Burial/'),
        ),
        migrations.AlterField(
            model_name='burialindividuals',
            name='age',
            field=models.CharField(max_length=2, blank=True, null=True, default='NI', choices=[('FT', 'Foetus'), ('NT', 'Neonate'), ('IF', 'Infant less than 3'), ('CH', 'Child 3 to 13'), ('SA', 'Sub adult 14 to 17'), ('AD', 'Adult 18 to 39'), ('OA', 'Old adult over 40'), ('NI', 'Not identified')]),
        ),
        migrations.AlterField(
            model_name='burialindividuals',
            name='burial_type',
            field=models.CharField(max_length=2, blank=True, null=True, choices=[('CR', 'Cremation'), ('IH', 'Inhumation'), ('MX', 'Mixed')]),
        ),
        migrations.AlterField(
            model_name='burialindividuals',
            name='gender',
            field=models.CharField(max_length=2, blank=True, null=True, default='NI', choices=[('MA', 'Male'), ('MU', 'Male uncertain'), ('FE', 'Female'), ('FU', 'Female uncertain'), ('CH', 'Child'), ('NI', 'Not identified')]),
        ),
        migrations.AlterField(
            model_name='burialindividuals',
            name='head_direction',
            field=models.CharField(max_length=2, blank=True, null=True, choices=[('N', 'North'), ('S', 'South'), ('E', 'East'), ('W', 'West'), ('NW', 'Northwest'), ('NE', 'Northeast'), ('SW', 'Southwest'), ('SE', 'Southeast'), ('EN', 'East northeast'), ('WN', 'West northwest'), ('ES', 'East southeast'), ('WS', 'West southwest')]),
        ),
        migrations.AlterField(
            model_name='burialindividuals',
            name='head_position',
            field=models.CharField(max_length=2, blank=True, null=True, choices=[('N', 'North'), ('S', 'South'), ('E', 'East'), ('W', 'West'), ('NW', 'Northwest'), ('NE', 'Northeast'), ('SW', 'Southwest'), ('SE', 'Southeast'), ('EN', 'East northeast'), ('WN', 'West northwest'), ('ES', 'East southeast'), ('WS', 'West southwest')]),
        ),
        migrations.AlterField(
            model_name='burialindividuals',
            name='organic_material_fk',
            field=models.ForeignKey(verbose_name='Organic Material', blank=True, null=True, to='aema_db.OrganicMaterial'),
        ),
        migrations.AlterField(
            model_name='burialindividuals',
            name='orientation',
            field=models.CharField(max_length=2, blank=True, null=True, choices=[('NS', 'North to South'), ('EW', 'East to West'), ('NW', 'Northwest to Southeast'), ('NE', 'Northeast to Southwest'), ('ES', 'East southeast to West northwest'), ('WS', 'West southwest to East northeast')]),
        ),
        migrations.AlterField(
            model_name='burialindividuals',
            name='position',
            field=models.CharField(max_length=2, blank=True, null=True, choices=[('PR', 'Prone'), ('SU', 'Supine'), ('CL', 'Crouched left'), ('CR', 'Crouched right'), ('CO', 'Crouched'), ('EX', 'Extended'), ('FL', 'Flexed left'), ('FR', 'Flexed right'), ('FX', 'Flexed'), ('UR', 'Urned'), ('UU', 'Unurned'), ('RD', 'Redeposited'), ('DS', 'Disturbed'), ('DI', 'Disarticulated')]),
        ),
        migrations.AlterField(
            model_name='burialindividuals',
            name='site_type',
            field=models.ForeignKey(verbose_name='Grave type', blank=True, null=True, to='aema_db.SiteTypeSpecific'),
        ),
        migrations.AlterField(
            model_name='burialindividuals',
            name='usage',
            field=models.CharField(max_length=2, blank=True, null=True, choices=[('PU', 'Primary'), ('SU', 'Secondary'), ('NK', 'Not known')]),
        ),
        migrations.AlterField(
            model_name='burials',
            name='age',
            field=models.CharField(max_length=20, blank=True, null=True, help_text='Redundant - to be replaced/moved'),
        ),
        migrations.AlterField(
            model_name='burials',
            name='amber_bool',
            field=models.NullBooleanField(verbose_name='Amber', default=False),
        ),
        migrations.AlterField(
            model_name='burials',
            name='arrowhead_bool',
            field=models.NullBooleanField(verbose_name='Arrowhead', default=False),
        ),
        migrations.AlterField(
            model_name='burials',
            name='biblio_for_site',
            field=models.CharField(max_length=1000, blank=True, null=True, help_text='Redundant - to be replaced/moved'),
        ),
        migrations.AlterField(
            model_name='burials',
            name='bone_object_bool',
            field=models.NullBooleanField(verbose_name='Bone object', default=False),
        ),
        migrations.AlterField(
            model_name='burials',
            name='burial_type',
            field=models.CharField(max_length='2', blank=True, null=True, choices=[('CR', 'Cremation'), ('IH', 'Inhumation'), ('MX', 'Mixed')]),
        ),
        migrations.AlterField(
            model_name='burials',
            name='cu_cu_alloy_bool',
            field=models.NullBooleanField(verbose_name='Copper/Copper alloy', default=False),
        ),
        migrations.AlterField(
            model_name='burials',
            name='dagger_bool',
            field=models.NullBooleanField(verbose_name='Dagger', default=False),
        ),
        migrations.AlterField(
            model_name='burials',
            name='faience_bool',
            field=models.NullBooleanField(verbose_name='Faience', default=False),
        ),
        migrations.AlterField(
            model_name='burials',
            name='flint_or_stone_bool',
            field=models.NullBooleanField(verbose_name='Flint or Stone', default=False),
        ),
        migrations.AlterField(
            model_name='burials',
            name='gender_m2m',
            field=models.ManyToManyField(verbose_name='Gender assemblage', to='aema_db.Gender'),
        ),
        migrations.AlterField(
            model_name='burials',
            name='general_chronology',
            field=models.CharField(max_length=50, blank=True, null=True, help_text='Redundant field - use the one below'),
        ),
        migrations.AlterField(
            model_name='burials',
            name='general_chronology_fk',
            field=models.ForeignKey(verbose_name='General chronology', blank=True, null=True, to='aema_db.GeneralChronology'),
        ),
        migrations.AlterField(
            model_name='burials',
            name='gold_silver_bool',
            field=models.NullBooleanField(verbose_name='Gold and Silver', default=False),
        ),
        migrations.AlterField(
            model_name='burials',
            name='grave_good_class_m2m',
            field=models.ManyToManyField(verbose_name='Grave good classes', to='aema_db.GraveGoodClass'),
        ),
        migrations.AlterField(
            model_name='burials',
            name='jet_lignite_shale_bool',
            field=models.NullBooleanField(verbose_name='Jet/Lignite/Shale', default=False),
        ),
        migrations.AlterField(
            model_name='burials',
            name='jewellery_bool',
            field=models.NullBooleanField(verbose_name='Jewellery', default=False),
        ),
        migrations.AlterField(
            model_name='burials',
            name='no_of_grave_goods',
            field=models.IntegerField(blank=True, null=True, help_text='Redundant - to be replaced/moved'),
        ),
        migrations.AlterField(
            model_name='burials',
            name='organic_material_fk',
            field=models.ForeignKey(verbose_name='Organic Material', blank=True, null=True, to='aema_db.OrganicMaterial'),
        ),
        migrations.AlterField(
            model_name='burials',
            name='pot_bool',
            field=models.NullBooleanField(verbose_name='Pot', default=False),
        ),
        migrations.AlterField(
            model_name='burials',
            name='site_fk',
            field=models.ForeignKey(verbose_name='Location summary', blank=True, null=True, help_text='Currently displaying ID as there needs to be some checking and rationalisation of site name records (according to the original values below)', to='aema_db.Site'),
        ),
        migrations.AlterField(
            model_name='burials',
            name='site_type_m2m',
            field=models.ManyToManyField(verbose_name='Site type(s)', to='aema_db.SiteType'),
        ),
        migrations.AlterField(
            model_name='burials',
            name='site_type_specific',
            field=models.ManyToManyField(verbose_name='Specific site type(s)', to='aema_db.SiteTypeSpecific'),
        ),
        migrations.AlterField(
            model_name='burials',
            name='usage',
            field=models.CharField(max_length='2', blank=True, null=True, choices=[('MP', 'Multi period'), ('SP', 'Single period')]),
        ),
        migrations.AlterField(
            model_name='burials',
            name='weapons_bool',
            field=models.NullBooleanField(verbose_name='Weapons', default=False),
        ),
        migrations.AlterField(
            model_name='burials',
            name='wristguard_bool',
            field=models.NullBooleanField(verbose_name='Wristguard', default=False),
        ),
        migrations.AlterField(
            model_name='etymology',
            name='celtic_etymology',
            field=models.TextField(verbose_name='Celtic etymology', max_length=1000, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='etymology',
            name='ie_etymology',
            field=models.CharField(verbose_name='IE etymology', max_length=100, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='etymology',
            name='leptonic',
            field=models.CharField(verbose_name='Lepontic', max_length=100, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='etymology',
            name='pie_etymology',
            field=models.CharField(verbose_name='PIE etymology', max_length=100, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='etymology',
            name='proto_celtic_etymology',
            field=models.CharField(verbose_name='Proto-Celtic etymology', max_length=1000, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='etymologydescription',
            name='description',
            field=models.CharField(verbose_name='Form', max_length=50),
        ),
        migrations.AlterField(
            model_name='etymologydescription',
            name='en_cognate',
            field=models.CharField(verbose_name='English definition', max_length=200, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='etymologydescription',
            name='long_description',
            field=models.CharField(verbose_name='Extended form', max_length=200, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gravegood',
            name='condition',
            field=models.BooleanField(verbose_name='Fragmentary?', default=False),
        ),
        migrations.AlterField(
            model_name='gravegood',
            name='functional_type',
            field=models.CharField(max_length='2', blank=True, null=True, choices=[('AX', 'Axehead'), ('AH', 'Arrowhead'), ('AW', 'Awl'), ('AT', 'Amulet'), ('AM', 'Armlet'), ('AT', 'Animal bone burnt'), ('AB', 'Animal bone unburnt'), ('BG', 'Beltring or toggle'), ('BT', 'Button'), ('BD', 'Bead'), ('BR', 'Bracelet'), ('BC', 'Bracer'), ('BL', 'Blade'), ('CO', 'Core'), ('CU', 'Cushion stone'), ('CP', 'Cup non ceramic'), ('CL', 'Cauldron'), ('DG', 'Dagger'), ('DC', 'Disc'), ('DF', 'Dress fastener'), ('DK', 'Dirk'), ('EG', 'Earring basket ornamnent'), ('FA', 'Fabricator'), ('FL', 'Flake'), ('FN', 'Flint nodule'), ('FB', 'Fibula'), ('FS', 'Fossil'), ('FR', 'Fur'), ('GG', 'Gorget'), ('HM', 'Hammerstone'), ('HB', 'Halberd'), ('HN', 'Horn'), ('KN', 'Knife'), ('LU', 'Lunulae'), ('LZ', 'Lozenge'), ('MC', 'Macehead'), ('NK', 'Necklace'), ('OT', 'Other'), ('PB', 'Polished bone'), ('PQ', 'Quartz pebble'), ('PE', 'Pebble'), ('PI', 'Pin'), ('PT', 'Pendant'), ('PO', 'Point'), ('RA', 'Rock art'), ('RG', 'Ring'), ('RU', 'Rubber'), ('RZ', 'Razor'), ('SC', 'Scraper'), ('SP', 'Spoon'), ('SW', 'Sword'), ('SH', 'Shell'), ('SM', 'Smoother'), ('SL', 'Strike-a-light'), ('SP', 'Spearhead'), ('TX', 'Textile'), ('QS', 'Quern - grinding stone'), ('UK', 'Unknown'), ('WH', 'Whetstone'), ('WS', 'Worked slate')], help_text='Use the new fk field below'),
        ),
        migrations.AlterField(
            model_name='gravegood',
            name='placement',
            field=models.CharField(max_length='2', blank=True, null=True, choices=[('NH', 'Near head'), ('BB', 'Behind back'), ('ND', 'Near hands'), ('PE', 'Pelvis'), ('NF', 'Near feet'), ('NK', 'Neck'), ('FF', 'In front of face'), ('WC', 'With cremation')]),
        ),
        migrations.AlterField(
            model_name='gravegood',
            name='raw_materials_m2m',
            field=models.ManyToManyField(verbose_name='Raw materials', blank=True, to='aema_db.GraveGoodRawMaterialType'),
        ),
        migrations.AlterField(
            model_name='gravegood',
            name='type',
            field=models.ForeignKey(blank=True, null=True, help_text='Possibly redundant field to be removed after updates', to='aema_db.GraveGoodType'),
        ),
        migrations.AlterField(
            model_name='hoardimage',
            name='image',
            field=models.ImageField(upload_to='static/media/uploads/Hoards/'),
        ),
        migrations.AlterField(
            model_name='hoards',
            name='dry_wet_context_choice',
            field=models.CharField(max_length=2, blank=True, null=True, choices=[('DR', 'Dry'), ('WT', 'Wet'), ('TR', 'Transition'), ('UD', 'Dry Uncertain'), ('UW', 'Wet Uncertain'), ('UT', 'Transition Uncertain'), ('UK', 'Unknown')]),
        ),
        migrations.AlterField(
            model_name='hoards',
            name='find_type_cleaned',
            field=models.CharField(max_length=2, blank=True, null=True, choices=[('HO', 'Hoard'), ('PR', 'Pair'), ('SF', 'Single find'), ('TR', 'Triple'), ('UK', 'Unknown')]),
        ),
        migrations.AlterField(
            model_name='hoards',
            name='no_of_objects_clustered_choice',
            field=models.CharField(max_length=2, blank=True, null=True, choices=[('UK', 'Unknown'), ('ON', '1'), ('TW', '2'), ('TH', '3'), ('FO', '4'), ('FV', '5'), ('SX', '6'), ('SV', '7'), ('EI', '8'), ('NI', '9'), ('TN', '10'), ('TP', '10 plus'), ('ET', '11 to 20'), ('TT', '21 to 30'), ('TF', '31 to 40'), ('FF', '41 to 50'), ('FH', '51 to 100'), ('HT', '101 to 200'), ('TA', '201 to 300'), ('TB', '301 to 400'), ('FA', '401 to 500'), ('FS', '501 to 600'), ('SS', '601 to 700'), ('SE', '701 to 800'), ('EN', '801 to 900'), ('NO', '901 to 1000'), ('OT', '1000 plus'), ('FT', '1500 plus'), ('TZ', '3500 plus')]),
        ),
        migrations.AlterField(
            model_name='hoards',
            name='object_condition_summary_choice',
            field=models.CharField(max_length=32, blank=True, null=True, choices=[('BR', 'Broken'), ('CP', 'Complete'), ('MC', 'Mainly intact'), ('MF', 'Mostly fragmented'), ('MX', 'Mixed'), ('UK', 'Unknown')]),
        ),
        migrations.AlterField(
            model_name='miscellaneous',
            name='dry_wet_context_choice',
            field=models.CharField(max_length=2, blank=True, null=True, choices=[('DR', 'Dry'), ('WT', 'Wet'), ('TR', 'Transition'), ('UD', 'Dry Uncertain'), ('UW', 'Wet Uncertain'), ('UT', 'Transition Uncertain'), ('UK', 'Unknown')]),
        ),
        migrations.AlterField(
            model_name='miscellaneous',
            name='find_type_cleaned',
            field=models.CharField(max_length=2, blank=True, null=True, choices=[('HO', 'Hoard'), ('PR', 'Pair'), ('SF', 'Single find'), ('TR', 'Triple'), ('UK', 'Unknown')]),
        ),
        migrations.AlterField(
            model_name='miscellaneous',
            name='no_of_objects_clustered_choice',
            field=models.CharField(max_length=2, blank=True, null=True, choices=[('UK', 'Unknown'), ('ON', '1'), ('TW', '2'), ('TH', '3'), ('FO', '4'), ('FV', '5'), ('SX', '6'), ('SV', '7'), ('EI', '8'), ('NI', '9'), ('TN', '10'), ('TP', '10 plus'), ('ET', '11 to 20'), ('TT', '21 to 30'), ('TF', '31 to 40'), ('FF', '41 to 50'), ('FH', '51 to 100'), ('HT', '101 to 200'), ('TA', '201 to 300'), ('TB', '301 to 400'), ('FA', '401 to 500'), ('FS', '501 to 600'), ('SS', '601 to 700'), ('SE', '701 to 800'), ('EN', '801 to 900'), ('NO', '901 to 1000'), ('OT', '1000 plus'), ('FT', '1500 plus'), ('TZ', '3500 plus')]),
        ),
        migrations.AlterField(
            model_name='miscellaneous',
            name='object_condition_summary_choice',
            field=models.CharField(max_length=32, blank=True, null=True, choices=[('BR', 'Broken'), ('CP', 'Complete'), ('MC', 'Mainly intact'), ('MF', 'Mostly fragmented'), ('MX', 'Mixed'), ('UK', 'Unknown')]),
        ),
        migrations.AlterField(
            model_name='miscellaneousimage',
            name='image',
            field=models.ImageField(upload_to='static/media/uploads/Misc/'),
        ),
        migrations.AlterField(
            model_name='miscellaneousimage',
            name='type',
            field=models.CharField(max_length=2, choices=[('GN', 'General'), ('IN', 'Inscription'), ('DW', 'Drawing')]),
        ),
        migrations.AlterField(
            model_name='ogam',
            name='contains_pn_bool',
            field=models.NullBooleanField(verbose_name='Contains personal names?'),
        ),
        migrations.AlterField(
            model_name='ogam',
            name='coords',
            field=models.CharField(max_length=200, blank=True, null=True, help_text='Irish Transverse Mercator, please use Map or WGS84 Lat/Lon from here on'),
        ),
        migrations.AlterField(
            model_name='ogam',
            name='name_forms_present',
            field=models.ManyToManyField(verbose_name='Name formulae M2M', to='aema_db.NameForm'),
        ),
        migrations.AlterField(
            model_name='ogam',
            name='nf',
            field=models.CharField(verbose_name='Name formulae', max_length=100, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ogam',
            name='rmp',
            field=models.CharField(verbose_name='Record of Monument and Place', max_length=100, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ogamimage',
            name='image',
            field=models.ImageField(upload_to='static/media/uploads/Ogam/'),
        ),
        migrations.AlterField(
            model_name='ogamimage',
            name='type',
            field=models.CharField(max_length=2, choices=[('GN', 'General'), ('IN', 'Inscription'), ('DW', 'Drawing')]),
        ),
        migrations.AlterField(
            model_name='ogaminscription',
            name='celtic_etymology',
            field=models.TextField(verbose_name='Celtic etymology', max_length=1000, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ogaminscription',
            name='chronology',
            field=models.CharField(max_length=100, blank=True, null=True, help_text='Should this be a drop down list also? NJ'),
        ),
        migrations.AlterField(
            model_name='ogaminscription',
            name='etymology',
            field=models.CharField(max_length=50, blank=True, null=True, help_text='Legacy field to be moved to drop down list'),
        ),
        migrations.AlterField(
            model_name='ogaminscription',
            name='etymology_fk',
            field=models.CharField(max_length=2, blank=True, null=True, choices=[('IE', 'Indo European'), ('PC', 'Proto Celtic'), ('CM', 'Comparanda')]),
        ),
        migrations.AlterField(
            model_name='ogaminscription',
            name='ie_etymology',
            field=models.TextField(verbose_name='IE etymology', max_length=1000, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ogaminscription',
            name='language',
            field=models.CharField(max_length=50, blank=True, null=True, help_text='Legacy field to be moved to drop down list'),
        ),
        migrations.AlterField(
            model_name='ogaminscription',
            name='language_fk',
            field=models.ForeignKey(verbose_name='Language of name', blank=True, null=True, to='aema_db.Language'),
        ),
        migrations.AlterField(
            model_name='ogaminscription',
            name='leptonic',
            field=models.TextField(verbose_name='Lepontic', max_length=1000, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ogaminscription',
            name='pie_etymology',
            field=models.TextField(verbose_name='PIE etymology', max_length=1000, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ogaminscription',
            name='proto_celtic_etymology',
            field=models.TextField(verbose_name='Proto-Celtic etymology', max_length=1000, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ogaminscription',
            name='reason',
            field=models.CharField(max_length=100, blank=True, null=True, help_text='Should this be a drop down list also? NJ'),
        ),
        migrations.AlterField(
            model_name='ogamsite',
            name='contains_pn_bool',
            field=models.NullBooleanField(verbose_name='Contains personal names?'),
        ),
        migrations.AlterField(
            model_name='ogamsite',
            name='context_macro',
            field=models.CharField(max_length=2, blank=True, null=True, choices=[('CS', 'Coastal'), ('IS', 'Island'), ('LW', 'Lowland'), ('RV', 'Riverine'), ('UL', 'Upland'), ('UK', 'Unknown')]),
        ),
        migrations.AlterField(
            model_name='ogamsite',
            name='context_macro_free_text',
            field=models.CharField(max_length=50, blank=True, null=True, help_text='to be moved into drop down list'),
        ),
        migrations.AlterField(
            model_name='ogamsite',
            name='context_micro',
            field=models.CharField(max_length=2, blank=True, null=True, choices=[('BU', 'Burial'), ('CA', 'Cairn'), ('CV', 'Cave'), ('EC', 'Ecclesiastical'), ('LN', 'Landscape'), ('ST', 'Settlement'), ('SH', 'Settlement hillfort'), ('SB', 'Settlement broch'), ('SR', 'Settlement Roman'), ('SS', 'Standing stone'), ('SP', 'Standing stone possible'), ('UK', 'Unknown')]),
        ),
        migrations.AlterField(
            model_name='ogamsite',
            name='context_micro_free_text',
            field=models.CharField(max_length=50, blank=True, null=True, help_text='To be moved into drop down list'),
        ),
        migrations.AlterField(
            model_name='ogamsite',
            name='context_secondary_text',
            field=models.CharField(max_length=10, blank=True, null=True, help_text='To be moved into tick box'),
        ),
        migrations.AlterField(
            model_name='ogamsite',
            name='coords',
            field=models.CharField(max_length=200, blank=True, null=True, help_text='Irish Transverse Mercator,         please use Map or WGS84 Lat/Lon from here on'),
        ),
        migrations.AlterField(
            model_name='ogamsite',
            name='etymology',
            field=models.TextField(blank=True, null=True, help_text='Temporary field to hold imported data. Contents should probably migrate to Fernandos data below'),
        ),
        migrations.AlterField(
            model_name='ogamsite',
            name='meaning',
            field=models.TextField(blank=True, null=True, help_text='Temporary field to hold imported data. Contents should probably migrate to Fernandos data below'),
        ),
        migrations.AlterField(
            model_name='ogamsite',
            name='name_forms_present',
            field=models.ManyToManyField(verbose_name='Name formulae M2M', to='aema_db.NameForm'),
        ),
        migrations.AlterField(
            model_name='ogamsite',
            name='nf',
            field=models.CharField(verbose_name='Name formulae', max_length=100, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ogamsite',
            name='rmp',
            field=models.CharField(verbose_name='Record of Monument and Place', max_length=100, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='organicmaterial',
            name='material_class',
            field=models.CharField(max_length=100, blank=True, null=True, help_text='No need to fill this in - it will populate automatically'),
        ),
        migrations.AlterField(
            model_name='pot',
            name='condition',
            field=models.CharField(max_length=2, default='CP', choices=[('CP', 'Complete'), ('FR', 'Fragmentary'), ('SH', 'Small number of sherds'), ('UK', 'Unknown')]),
        ),
        migrations.AlterField(
            model_name='pot',
            name='count',
            field=models.IntegerField(blank=True, null=True, help_text='Redundant - to be replaced/moved'),
        ),
        migrations.AlterField(
            model_name='pot',
            name='pot_disposition',
            field=models.CharField(verbose_name='Pot position', max_length='2', blank=True, null=True, choices=[('UP', 'Upright'), ('IN', 'Inverted'), ('SO', 'On side')]),
        ),
        migrations.AlterField(
            model_name='pot',
            name='pot_placement',
            field=models.CharField(max_length='2', blank=True, null=True, choices=[('NH', 'Near head'), ('BB', 'Behind back'), ('ND', 'Near hands'), ('PE', 'Pelvis'), ('NF', 'Near feet'), ('NK', 'Neck'), ('FF', 'In front of face'), ('WC', 'With cremation'), ('CN', 'Container')]),
        ),
        migrations.AlterField(
            model_name='pot',
            name='specific_type',
            field=models.CharField(verbose_name='Type', max_length='2', blank=True, null=True, choices=[('UK', 'Unknown'), ('BB', 'Bell beaker'), ('BL', 'Beaker local or derived'), ('BU', 'Bucket urn'), ('CU', 'Collared urn'), ('CO', 'Cordoned urn'), ('EN', 'Encrusted urn'), ('FV', 'Food vessel'), ('GU', 'Globular urn'), ('GW', 'Grooved ware'), ('LN', 'Late Neolithic'), ('EB', 'Early Bronze age'), ('MB', 'Middle Bronze age'), ('MV', 'Miniature vessel'), ('LB', 'Late Bronze age'), ('LI', 'Late Bronze Iron age'), ('VU', 'Vase urn')]),
        ),
        migrations.AlterField(
            model_name='pot',
            name='type',
            field=models.ForeignKey(blank=True, null=True, help_text='Possibly redundant field to be removed        after data migrated to new field', to='aema_db.PotType'),
        ),
        migrations.AlterField(
            model_name='stelaeimage',
            name='image',
            field=models.ImageField(upload_to='static/media/uploads/Stelae/'),
        ),
        migrations.AlterField(
            model_name='toponyms',
            name='briga',
            field=models.CharField(max_length=1, blank=True, db_column='briga'),
        ),
        migrations.AlterField(
            model_name='toponyms',
            name='dunon',
            field=models.CharField(max_length=1, blank=True, db_column='dunon'),
        ),
        migrations.AlterField(
            model_name='toponyms',
            name='duron',
            field=models.CharField(max_length=1, blank=True, db_column='duron'),
        ),
        migrations.AlterField(
            model_name='toponyms',
            name='ebur',
            field=models.CharField(max_length=1, blank=True, db_column='ebur'),
        ),
        migrations.AlterField(
            model_name='toponyms',
            name='language',
            field=models.CharField(max_length=10, blank=True, db_column='language'),
        ),
        migrations.AlterField(
            model_name='toponyms',
            name='magos',
            field=models.CharField(max_length=1, blank=True, db_column='magos'),
        ),
        migrations.AlterField(
            model_name='toponyms',
            name='name',
            field=models.CharField(max_length=30, blank=True, db_column='toponym'),
        ),
        migrations.AlterField(
            model_name='toponyms',
            name='nemeton',
            field=models.CharField(max_length=1, blank=True, db_column='nemeton'),
        ),
        migrations.AlterField(
            model_name='toponyms',
            name='notes',
            field=models.CharField(max_length=30, blank=True, db_column='notes'),
        ),
        migrations.AlterField(
            model_name='toponyms',
            name='notes_2_m',
            field=models.CharField(max_length=50, blank=True, db_column='notes_2'),
        ),
        migrations.AlterField(
            model_name='toponyms',
            name='novios',
            field=models.CharField(max_length=1, blank=True, db_column='novios'),
        ),
        migrations.AlterField(
            model_name='toponyms',
            name='object',
            field=models.CharField(max_length=10, blank=True, db_column='obj'),
        ),
        migrations.AlterField(
            model_name='toponyms',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, db_column='the_geom', srid=4326),
        ),
        migrations.AlterField(
            model_name='toponyms',
            name='sego_field',
            field=models.CharField(max_length=1, blank=True, db_column='sego'),
        ),
        migrations.AlterField(
            model_name='toponyms',
            name='source',
            field=models.CharField(max_length=30, blank=True, db_column='source'),
        ),
        migrations.AlterField(
            model_name='toponyms',
            name='text',
            field=models.CharField(max_length=20, blank=True, db_column='toponym_text'),
        ),
        migrations.AlterField(
            model_name='toponyms',
            name='variants',
            field=models.CharField(max_length=60, blank=True, db_column='variants'),
        ),
    ]
