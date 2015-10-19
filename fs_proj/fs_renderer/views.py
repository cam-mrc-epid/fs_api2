import json
from django.http import HttpResponseNotFound
from django.views.generic import View
from django.shortcuts import render
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from custom_logic import CustomApplication
from django.views import generic
from questionnaire.models import Results, Users
import local_settings


if local_settings.CUSTOM:
    fenland_app = CustomApplication('fenland', local_settings.XML_FILE)
else:
    from fs_apps import Application
    fenland_app = Application('fenland', local_settings.XML_FILE)


class AltHTMLView(View):
    def get(self, request, section=None, question_group=None, question=None):
        result = {}
        if section is None:
            return HttpResponseNotFound('Page Not Found')
        section_obj = fenland_app.get_section(section)
        if request.GET:
            id_variable_value = request.GET['id']
            result['id_variable_value'] = id_variable_value
            # data = fenland_app.get_data(section, 'id', id_variable_value)
            # section_obj = DataPrep(section_obj, data)
            # section_obj = section_obj.data_prep()
            # data = FamHistQuestionnaire.objects.get(pk=id_variable_value)
            q_data = Results.objects.filter(user_id=id_variable_value).filter(questionnaire_id=section_obj.app_object.id)
            data={}
            for q in q_data:
                data[q.var_name] = q.var_value
        else:
            data = {}
            data['id'] = None
        if section_obj.plugins:
            for plugin_section in section_obj.plugins:
                plugin_section.plugin = local_settings.PLUGINS[plugin_section.plugin](data, plugin_section)
        if question_group is None:
            result['section'] = section_obj
            # result['data_id'] = data.id
            result['data'] = data
            return render(request, 'fs_renderer/alt_base2.html', result)
        question_group = section_obj.get_question_group(question_group)
        if question is None:
            result['question_group'] = question_group
            return render(request, 'fs_renderer/alt_question_group.html', result)
        question = question_group.get_question(question)
        result['question'] = question
        return render(request, 'fs_renderer/alt_question.html', result)

    def post(self, request, section=None, question_group=None, question=None):
        result = {}
        if section is None:
            return HttpResponseNotFound('Page Not Found')
        section_obj = fenland_app.get_section(section)
        myDict = dict(request.POST.iterlists())
        id_variable_value = request.GET['id']
        for k in myDict.keys():
            myDict[k] = myDict[k][0]
        if 'search' in myDict.keys():
            result['search_results'] = fenland_app.search(myDict['search'], section)
            data = {}
        else:
            for qg in section_obj.question_groups:
                for q in qg.question_group_objects:
                    try:
                        if q.variable in myDict.keys():
                            try:
                                q.validator.clean(myDict[q.variable])
                            except ValidationError as e:
                                section_obj.errors[q.variable] = unicode(e[0])
                    except:
                        pass
            q_data = Results.objects.filter(user_id=id_variable_value).filter(questionnaire_id=section_obj.app_object.id)
            user = Users.objects.get(user_id=id_variable_value)
            if not section_obj.errors:
                for q in q_data:
                    if q.var_name in myDict.keys():
                        q.var_value = myDict[q.var_name]
                        myDict.pop(q.var_name)
                        q.save()
                for q in myDict.keys():
                    Results.objects.create(user=user, questionnaire_id=section_obj.app_object.id, var_name=q, var_value=myDict[q])
            q_data = Results.objects.filter(user_id=id_variable_value).filter(questionnaire_id=section_obj.app_object.id)
            data={}
            for q in q_data:
                data[q.var_name] = q.var_value
            result['data'] = data
            result['section'] = section_obj
            if section_obj.plugins:
                for plugin_section in section_obj.plugins:
                    plugin_section.plugin = local_settings.PLUGINS[plugin_section.plugin](data, plugin_section)
            return render(request, 'fs_renderer/alt_base2.html', result)
        result['section'] = section_obj
        return render(request, 'fs_renderer/alt_base2.html', result)

