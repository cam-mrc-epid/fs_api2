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

# XML_FILE to load
XML_FILE = 'xmlfiles/FamHist.xml'
# XML_FILE = 'C:/Fenland/xmlfiles/RPAQtest3_v10.xml' # CHANGE 


# QUESTIONNAIRE set to True will use django-fsq questionnaire app models.
QUESTIONNAIRE = True
