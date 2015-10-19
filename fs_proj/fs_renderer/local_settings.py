"""
Local Settings for the renderer.
"""
from plugins import *

PLUGINS = {'childlist': ChildList, 'testplugin': TestPlugin}

# TESTING set to True adds a submission button, and head and body tags to the output 
# so that submission can be tested and the debug_toolbar will operate with it. 
TESTING = True 

# MODELS set to True will tell the Application class to use Django's models and ORM.
MODELS = False

# CUSTOM set to True will mean that the views.py will load the CustomApplication class
# from custom_logic.py rather than the Application class from fs_apps.py.
CUSTOM = False

# SECTION_MAPPING maps section numbers to primary table names
SECTION_MAPPING =  {0: 'volunteers', 1: 'volunteers', 2: 'volunteers',
                    3: 'volunteers', 4: 'volunteers'}

# DB_MAPPING is only needed if some model fields have different column names in the database.
DB_MAPPING = {'surgery': 'surgeries_id', 'surgeries': 'surgeries_id', 'diabetes': 'diabetes_diagnosed'}

# MODEL_MAPPING maps sections to primary Django models.
# MODEL_MAPPING = {0: Volunteer, 1: Volunteer, 2: Volunteer, 3: Volunteer, 4: Volunteer}
MODEL_MAPPING = {}

# MODEL_FORM_MAPPING maps Django Forms models to sections.  These are used for validation.
# MODEL_FORM_MAPPING = {0: VolunteerForm, 1: VolunteerForm, 2: VolunteerForm,
#                       3: VolunteerForm, 4: VolunteerForm}
MODEL_FORM_MAPPING = {}

# TABLE_MODEL_MAPPING allows secondary mapping between XML and models
# for multis with the multi attribute in the XML.
# TABLE_MODEL_MAPPING = {'volunteers': Volunteer, 'appointments': Appointment}
TABLE_MODEL_MAPPING = {}

# DATABASE to use if not using models
DATABASE = 'mysql+pymysql://david:david@localhost:3306/mydb'

# XML_FILE to load
XML_FILE = 'xmlfiles/FamHist.xml'
# XML_FILE = 'C:/Fenland/xmlfiles/RPAQtest3_v10.xml' # CHANGE 


# QUESTIONNAIRE set to True will use django-fsq questionnaire app models.
QUESTIONNAIRE = True
