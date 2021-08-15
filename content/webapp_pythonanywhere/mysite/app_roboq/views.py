from os import name
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.views import View
from time import sleep
import pandas as pd
import os
import shutil
from .models import *

# Create your views here.


class UploadExcel(View):

    template_name = 'app_roboq/upload_excel.html'

    def get(self, request):

        context = {
            'topnav_animate': 'svg-topnav-obj-roboq-rect'
        }

        return render(request, self.template_name, context)


    def post(self, request):

        import pandas as pd
        from dict2xml import dict2xml
        from django.core.files import File

        class IDSForm:

            '''

            '''

            def __init__(self, path, *args, **kwargs):
                self.path = path
                self.args = args
                self.kwargs = kwargs

            def open_ids_excel(self):
                '''
                aim: read all sheets from the template excel
                '''
                def read_into_df(self, sheet_list):
                    for sheet in sheet_list:
                        df = pd.read_excel(
                            self.path,
                            sheet_name=sheet,
                            dtype=str
                        ).fillna('')    # fillna() to replace nan with ''
                        self.kwargs[str('df-' + sheet)] = df
                sheet_list = ['us-filing-info', 'us-patent-cite', 'us-pub-appl-cite', 'us-foreign-document-cite', 'us-nplcit', 'us-ids-certification']
                read_into_df(self, sheet_list)

            def create_backbone(self):
                data = {
                    'us-ids': {},
                    'version-info': '1.0',
                    '_date-produced': '20050902',
                    '_dtd-version': 'v20_EFSWeb',
                    '_file': '',
                    '_lang': '',
                    '_status': ''
                }
                self.kwargs['base_data'] = {
                    'us-ids': data
                }

            def create_us_filing_info(self):
                '''
                create dict['us-filing-info']
                '''
                df = self.kwargs['df-us-filing-info']
                data = {
                    'us-application-identification-info':{
                        'doc-number': df['doc-number'][0],
                        'date': df['date'][0]
                    },
                    'us-first-named-inventor': {
                        'name': {
                            '_name-type': '',
                            '__text': df['us-first-named-inventor'][0]
                        },
                    },
                    'primary-examiner': {
                        'name': {
                            '_name-type': '',
                            '__text': df['primary-examiner'][0]
                        },
                        'electronic-signature': {
                            'basic-signature': {
                                'text-string': ''
                            },
                            '_date': '',
                            '_place-signed': ''
                        }
                    },
                    'file-reference-id': df['file-reference-id'][0],
                    'us-group-art-unit': df['us-group-art-unit'][0]
                }
                self.kwargs['base_data']['us-ids']['us-filing-info'] = data

            def create_certification(self):
                df = self.kwargs['df-us-ids-certification']
                if len(df) != 0:
                    data ={
                        'applicant-name': {
                            'name': {
                                '_name-type': '',
                                '__text': df['name'][0]
                            },
                            'registered-number': df['registered-number'][0]
                        },
                    }
                    self.kwargs['base_data']['us-ids']['us-ids-certification'] = data

            def create_patent_cite(self):
                sheet_list = ['us-patent-cite', 'us-pub-appl-cite', 'us-foreign-document-cite']
                for sheet in sheet_list:
                    df = self.kwargs[str('df-' + sheet)]
                    doc_reference = []
                    if len(df) != 0:
                        for row in range(len(df)):
                            if sheet == 'us-patent-cite':
                                id = 'dd: id_2'
                                num = str(row + 1)
                            elif sheet == 'us-pub-appl-cite':
                                id = 'dd: id_3'
                                num = str(row + 1)
                            else:
                                id = str(row + 1)
                                num = ''
                            instance = {
                                'doc-number': df['doc-number'][row],
                                'name': {
                                    '_name-type': '',
                                    '__text': df['name'][row]
                                },
                                'kind': df['kind'][row],
                                'date': df['date'][row],
                                'class': '',
                                'subclass': '',
                                'relevant-portion': df['relevant-portion'][row],
                                '_id': id,
                                '_num': num,
                                '_sequence': ''
                            }
                            if sheet == 'us-foreign-document-cite':
                                instance['country'] = df['country'][row]
                                if df['_translation-attached'][row] != '':
                                    instance['_translation-attached'] = 'yes'
                                else:
                                    instance['_translation-attached'] = 'no'
                            doc_reference.append(instance)
                        if sheet != 'us-foreign-document-cite':
                            data = {
                                'us-doc-reference': doc_reference
                            }
                        else:
                            data = {
                                'us-foreign-doc-reference': doc_reference
                            }
                        self.kwargs['base_data']['us-ids'][sheet] = data
            def create_non_patent_cite(self):
                df = self.kwargs[str('df-us-nplcit')]
                us_nplcit = []
                if len(df) != 0:
                    for row in range(len(df)):
                        instance = {
                            'text': df['text'][row],
                            '_file': '',
                            '_id': str(row + 1),
                            '_medium': '',
                            '_num': '',
                            '_sequence': '',
                            '_type': '',
                            '_url': '',
                        }
                        if df['_translation-attached'][row] != '':
                            instance['_translation-attached'] = 'yes'
                        else:
                            instance['_translation-attached'] = 'no'
                        us_nplcit.append(instance)
                    self.kwargs['base_data']['us-ids']['us-nplcit'] = us_nplcit

        file = request.FILES['file'].read()
        data = pd.read_excel(file)

        base_folder = str(os.path.dirname(os.path.realpath(__file__)))
        print('base_folder:' + base_folder)
        ids_xml_output = base_folder + 'output_xml/{}_output.xml'.format(request.POST['username'])
        form_data = IDSForm(path=file)
        form_data.open_ids_excel()
        form_data.create_backbone()
        form_data.create_us_filing_info()
        form_data.create_certification()
        form_data.create_patent_cite()
        form_data.create_non_patent_cite()
        xml_output = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_output = xml_output+ dict2xml(form_data.kwargs['base_data'], wrap='', indent='  ')

        dir_path = '/home/ipskios/mysite/media/xml/{}'.format(request.user)

        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))

        with open('mysite/app_roboq/output_xml/{}_output.xml'.format(request.POST['username']), 'w+') as xml_file:
            xml_file.write(xml_output)
            file = File(xml_file)
        file = open('mysite/app_roboq/output_xml/{}_output.xml'.format(request.POST['username']), 'rb')

        try:
            instance = UploadIDS.objects.get(char_username=str(request.user))
            instance.delete()
            UploadIDS.objects.create(
                char_username=request.POST['username'],
                doc_xml=File(file)
            )
        except:
            UploadIDS.objects.create(
                char_username=request.POST['username'],
                doc_xml=File(file)
            )

        close_window = '''
            <body onload="window.close()">
        '''

        return HttpResponse(close_window)


class DownloadExcel(View):

    def get(self, request):

        sleep(1)

        instance = UploadIDS.objects.get(char_username=str(request.user))
        instance.delete()

        dir_path = '/home/ipskios/mysite/media/xml/{}'.format(request.user)

        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))


        context = {
            'topnav_animate': 'svg-topnav-obj-roboq-rect'
        }

        return HttpResponseRedirect('/')