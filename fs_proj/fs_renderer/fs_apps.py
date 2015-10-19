from copy import deepcopy
from itertools import chain
from xml_objectifier import objectifier
import datetime
import simplejson
import local_settings
from django import forms
from django.forms.models import model_to_dict


class Question(objectifier.Question):
    def __init__(self, question_object, app_object, section_object):
        self.plugin = ''
        super(Question, self).__init__(question_object, app_object, section_object)
        self.validator = self.set_validator()
        self.model = self.set_model()

    def set_validator(self):
        try:
            if 'CheckMaxLength' in self.restrictions.keys():
                self.maxlength = self.data_type['maxLength']
            if 'IsAnswered' in self.restrictions.keys():
                if self.restrictions['IsAnswered']['AllowError'] == 'false':
                    self.required = True
            if self.maxlength and self.required:
                return self.fields(self.data_type['type'])(maxlength=self.maxlength, required=True)
            elif self.maxlength and not self.required:
                return self.fields(self.data_type['type'])(maxlength=self.maxlength, required=False)
            elif not self.maxlength and self.required:
                return self.fields(self.data_type['type'])(required=True)
            elif not self.maxlength and not self.required:
                return self.fields(self.data_type['type'])(required=False)
        except: 
            pass


    def fields(self, field_type):
        return {'text': forms.CharField, 'string': forms.CharField, 'integer': forms.IntegerField,
                'real': forms.FloatField, 'date': forms.DateField,
                'dateTime': forms.DateTimeField, 'time': forms.TimeField,
                }[field_type]

    def set_rendering_hint(self, item):
        key = item.rhType.text
        self.rendering_hints[key] = ''
        for rhdata in item.rhData:
            self.rendering_hints[key] = self.rendering_hints[key] + ' ' + str(rhdata)
            if key == 'plugin':
                self.section.plugins.append(self)
                self.plugin = self.rendering_hints[key].strip()
                # self.app_object.plugins['questioon_plugins'].append(self.rendering_hints[key].strip())
                # self.section.plugins.append(self.rendering_hints[key].strip())
        self.rendering_hints[key] = self.rendering_hints[key].strip()

    def set_model(self):
        if self.variable in self.app_object.db_mapping.keys():
            variable = self.app_object.db_mapping[self.variable]
        else:
            variable = self.variable
        if self.app_object.models:
            section_model = self.app_object.model_mapping[int(self.section.position)]
            if variable in section_model._meta.get_all_field_names():
                self.model = section_model
            elif 'multi' in self.rendering_hints.keys():
                if variable in self.app_object.table_model_mapping[self.rendering_hints['multi']]._meta.get_all_field_names():
                    self.model = self.app_object.table_model_mapping[self.rendering_hints['multi']]
            else:
                self.model = None

    def get_template(self, selection):
        return {'radio': 'fs_renderer/radio.html',
                'dropdown': 'fs_renderer/select.html',
                'text': 'fs_renderer/text.html',
                'multiline': 'fs_renderer/textarea.html',
                'range': 'fs_renderer/range.html',
                'datalist': 'fs_renderer/datalist.html',
                'search': 'fs_renderer/search.html',
                'altradio': 'fs_renderer/alt_radio.html',
                'altdropdown': 'fs_renderer/alt_select.html',
                'alttext': 'fs_renderer/alt_text.html',
                'altmultiline': 'fs_renderer/alt_textarea.html',
                'altrange': 'fs_renderer/alt_range.html',
                'altdatalist': 'fs_renderer/alt_datalist.html',
                'altsearch': 'fs_renderer/alt_search.html',
                'altpassword': 'fs_renderer/text.html',}[selection]

    def set_template(self):
        if local_settings.QUESTIONNAIRE:
            qtype = 'alt' + self.rendering_hints['qtype']
            self.template = self.get_template(qtype)
        else:
            self.template = self.get_template(self.rendering_hints['qtype'])


class QuestionGroup(objectifier.QuestionGroup):
    def __init__(self, question_group_object, app_object, section_object):
        self.testing = local_settings.TESTING
        self.plugin = ''
        super(QuestionGroup, self).__init__(question_group_object, app_object, section_object)

    def set_rendering_hint(self, item):
        key = item.rhType.text
        self.rendering_hints[key] = ''
        for rhdata in item.rhData:
            self.rendering_hints[key] = self.rendering_hints[key] + ' ' + str(rhdata)
            if key == 'plugin':
                # self.plugins.append(self.rendering_hints[key].strip())
                self.section.plugins.append(self)
                self.plugin = self.rendering_hints[key].strip()
        self.rendering_hints[key] = self.rendering_hints[key].strip()

    def set_question(self, item):
        question = Question(item, self.app_object, self.section)
        self.question_group_objects.append(question)


class Section(objectifier.Section):
    def __init__(self, section_xml_object, app_object):
        self.testing = local_settings.TESTING
        self.plugins = []
        self.plugin = ''
        super(Section, self).__init__(section_xml_object, app_object)

    def set_rendering_hint(self, item):
        key = item.rhType.text
        self.rendering_hints[key] = ''
        for rhdata in item.rhData:
            self.rendering_hints[key] = self.rendering_hints[key] + ' ' + str(rhdata)
            if key == 'plugin':
                self.plugins.append(self)
                self.plugin = self.rendering_hints[key].strip()
                # self.app_object.plugins['section_plugins'].append(self.rendering_hints[key].strip())
        self.rendering_hints[key] = self.rendering_hints[key].strip()

    def set_question_group(self, item):
        """Creates Question Group instances."""
        question_group = QuestionGroup(item, self.app_object, self)
        self.question_groups.append(question_group)
        self.section_objects.append(question_group)

    def section_to_dict(self):
        data = {}
        multi = False
        for qg in self.section_objects:
            data_dict = {}
            for q in qg.question_group_objects:
                if isinstance(q, Question):
                    if 'multi' in q.rendering_hints.keys() or multi is True:
                        if multi is False:
                            multi = True
                            multi_name = q.rendering_hints['multi']
                            if multi_name not in data.keys():
                                data[multi_name] = []
                        data_dict['id'] = q.var_id
                        if isinstance(q.var_value, datetime.timedelta):
                            data_dict[q.variable[:-2]] = str(q.var_value)
                        else:
                            data_dict[q.variable[:-2]] = q.var_value
                        if 'endoftr' in q.rendering_hints.keys():
                            multi = False
                            data[multi_name].append(data_dict)
                            data_dict = {}
                    else:
                        if isinstance(q.var_value, datetime.timedelta):
                            data[q.variable] = str(q.var_value)
                        else:
                            data[q.variable] = q.var_value
        return data


class Application(objectifier.Application):
    def __init__(self, name, xml_path):
        self.models = local_settings.MODELS
        self.custom = local_settings.CUSTOM
        self.mapping = local_settings.SECTION_MAPPING
        self.db_mapping = local_settings.DB_MAPPING
        self.model_mapping = local_settings.MODEL_MAPPING
        self.model_form_mapping = local_settings.MODEL_FORM_MAPPING
        self.table_model_mapping = local_settings.TABLE_MODEL_MAPPING
        self.testing = local_settings.TESTING
        self.plugins = []
        super(Application, self).__init__(name, xml_path)


    def get_sections(self):
        """Instantiates Section objects for each section."""
        sections = {}
        for section in self.xml_object.section:
            sections[section.attrib['position']] = Section(section, self)
        return sections

    def set_rendering_hint(self, item):
        key = item.rhType.text
        self.rendering_hints[key] = ''
        for rhdata in item.rhData:
            self.rendering_hints[key] = self.rendering_hints[key] + ' ' + str(rhdata)
            if key == 'plugin':
                self.plugins.append(self.rendering_hints[key].strip())
        self.rendering_hints[key] = self.rendering_hints[key].strip()


    def get_table_name(self, section_number):
        return self.mapping[int(section_number)]

    def search(self, search_term, section_number):
        pass

    def get_section(self, section_number):
        return deepcopy(self.sections[str(section_number)])
