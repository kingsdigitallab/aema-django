

burial_use_period_choice = (
    ('MP','Multi period'),
    ('SP','Single period'),
)

burial_type_choices = (
    ('CR','Cremation'),
    ('IH','Inhumation'),
    ('MX','Mixed')
)

burial_age_assemblage = (
    ('FT','Foetus'),
    ('NT','Neonate'),
    ('IF','Infant less than 3'),
    ('CH','Child 3 to 13'),
    ('SA','Sub adult 14 to 17'),
    ('AD','Adult 18 to 39'),
    ('OA','Old adult over 40'),
    ('NI','Not identified'),        
)


burial_gender_choice = (
    ('MA','Male'),
    ('MU','Male uncertain'),
    ('FE','Female'),
    ('FU','Female uncertain'),
    ('CH','Child'),
    ('NI','Not identified'),    
)

burial_usage_choice = (
    ('PU','Primary'),
    ('SU','Secondary'),
    ('NK','Not known'),    
)

burial_position_choices = (
    ('PR','Prone'),
    ('SU','Supine'),
    ('CL','Crouched left'),
    ('CR','Crouched right'),
    ('CO','Crouched'),
    ('EX','Extended'),
    ('FL','Flexed left'),
    ('FR','Flexed right'),
    ('FX','Flexed'),
    ('UR','Urned'),
    ('UU','Unurned'),
    ('RD','Redeposited'),
    ('DS','Disturbed'),
    ('DI','Disarticulated'),
)

burial_orientation_choices  = (
    ('NS','North to South'),
    ('EW','East to West'),
    ('NW','Northwest to Southeast'),
    ('NE','Northeast to Southwest'),
    ('ES','East southeast to West northwest'),
    ('WS','West southwest to East northeast'),
)


burial_direction_choices = (
    ('N','North'),
    ('S','South'),
    ('E','East'),
    ('W','West'),
    ('NW','Northwest'),
    ('NE','Northeast'),
    ('SW','Southwest'),
    ('SE','Southeast'),    
    ('EN','East northeast'),
    ('WN','West northwest'),
    ('ES','East southeast'),
    ('WS','West southwest'),        
)


burial_grave_good_type_choices = (
    ('AX','Axehead'),    
    ('AH','Arrowhead'),
    ('AW','Awl'),
    ('AT','Amulet'),    
    ('AM','Armlet'),
    ('AT','Animal bone burnt'),
    ('AB','Animal bone unburnt'),    
    ('BG','Beltring or toggle'),
    ('BT','Button'),
    ('BD','Bead'),    
    ('BR','Bracelet'),
    ('BC','Bracer'),
    ('BL','Blade'),    
    ('CO','Core'),    
    ('CU','Cushion stone'),            
    ('CP','Cup non ceramic'),
    ('CL','Cauldron'),    
    ('DG','Dagger'),        
    ('DC','Disc'),        
    ('DF','Dress fastener'),
    ('DK','Dirk'),    
    ('EG','Earring basket ornamnent'),
    ('FA','Fabricator'),    
    ('FL','Flake'),
    ('FN','Flint nodule'),    
    ('FB','Fibula'),
    ('FS','Fossil'),    
    ('FR','Fur'),
    ('GG','Gorget'),    
    ('HM','Hammerstone'),    
    ('HB','Halberd'),
    ('HN','Horn'),
    ('KN','Knife'),    
    ('LU','Lunulae'),
    ('LZ','Lozenge'),
    ('MC','Macehead'),    
    ('NK','Necklace'),            
    ('OT','Other'),        
    ('PB','Polished bone'),
    ('PQ','Quartz pebble'),
    ('PE','Pebble'),
    ('PI','Pin'),        
    ('PT','Pendant'),
    ('PO','Point'),    
    ('RA','Rock art'),    
    ('RG','Ring'),
    ('RU','Rubber'),
    ('RZ','Razor'),            
    ('SC','Scraper'),
    ('SP','Spoon'),
    ('SW','Sword'),        
    ('SH','Shell'),        
    ('SM','Smoother'),
    ('SL','Strike-a-light'),
    ('SP','Spearhead'),
    ('TX','Textile'),    
    ('QS','Quern - grinding stone'),
    ('UK','Unknown'),
    ('WH','Whetstone'),
    ('WS','Worked slate'),    
)

burial_pot_and_good_placement_choices = (
    ('NH','Near head'),
    ('BB','Behind back'),
    ('ND','Near hands'),
    ('PE','Pelvis'),
    ('NF','Near feet'),
    ('NK','Neck'),
    ('FF','In front of face'),    
    ('WC','With cremation'),
)

burial_pot_position_choices = (
    ('UP','Upright'),
    ('IN','Inverted'),
    ('SO','On side'),    
)

burial_pot_type_choices = (
    ('UK','Unknown'),
    ('BB','Bell beaker'),
    ('BL','Beaker local or derived'),
    ('BU','Bucket urn'),    
    ('CU','Collared urn'),  
    ('CO','Cordoned urn'),
    ('EN','Encrusted urn'),      
    ('FV','Food vessel'),    
    ('GU','Globular urn'),  
    ('GW','Grooved ware'),
    ('LN','Late Neolithic'),    
    ('EB','Early Bronze age'),  
    ('MB','Middle Bronze age'),      
    ('MV','Miniature vessel'),
    ('LB','Late Bronze age'),    
    ('LI','Late Bronze Iron age'),  
    ('VU','Vase urn'),
)

burial_pot_condition_choices = (
    ('CP','Complete'),
    ('FR','Fragmentary'),
    ('SH','Small number of sherds'),
    ('UK','Unknown'),    
)


context_micro_choices = (
    ('BU','Burial'),
    ('CA','Cairn'),
    ('CV','Cave'),
    ('EC','Ecclesiastical'),
    ('LN','Landscape'),
    ('ST','Settlement'),
    ('SH','Settlement hillfort'),
    ('SB','Settlement broch'),
    ('SR','Settlement Roman'),
    ('SS','Standing stone'),
    ('SP','Standing stone possible'),
    ('UK','Unknown')
)

context_macro_choices = (
    ('CS','Coastal'),
    ('IS','Island'),
    ('LW','Lowland'),
    ('RV','Riverine'),
    ('UL','Upland'),
    ('UK','Unknown'),
)

etymology_choices = (
    ('IE','Indo European'),
    ('PC','Proto Celtic'),
    ('CM','Comparanda')
)

hoard_find_type_choices = (
    ('HO','Hoard'),
    ('PR','Pair'),
    ('SF','Single find'),
    ('TR','Triple'),
    ('UK','Unknown'),    
)


hoard_object_condition_choice = (
    ('BR','Broken'),
    ('CP','Complete'),
    ('MC','Mainly intact'),
    ('MF','Mostly fragmented'),
    ('MX','Mixed'),
    ('UK','Unknown'),        
)


hoard_context_choice =(
    ('DR','Dry'),
    ('WT','Wet'),
    ('TR','Transition'),
    ('UD','Dry Uncertain'),
    ('UW','Wet Uncertain'),
    ('UT','Transition Uncertain'),    
    ('UK','Unknown'),    
)


hoard_object_count = (
    ('UK','Unknown'),
    ('ON','1'),
    ('TW','2'),
    ('TH','3'),
    ('FO','4'),
    ('FV','5'),
    ('SX','6'),
    ('SV','7'),
    ('EI','8'),
    ('NI','9'),
    ('TN','10'),
    ('TP','10 plus'),
    ('ET','11 to 20'),
    ('TT','21 to 30'),
    ('TF','31 to 40'),
    ('FF','41 to 50'),
    ('FH','51 to 100'),
    ('HT','101 to 200'),
    ('TA','201 to 300'),
    ('TB','301 to 400'),
    ('FA','401 to 500'),
    ('FS','501 to 600'),
    ('SS','601 to 700'),
    ('SE','701 to 800'),
    ('EN','801 to 900'),
    ('NO','901 to 1000'),
    ('OT','1000 plus'),
    ('FT','1500 plus'),
    ('TZ','3500 plus')
)


ogam_image_type = (
    ('GN','General'),
    ('IN','Inscription'),
    ('DW','Drawing'),
)
