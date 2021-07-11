from posixpath import basename
import pandas as pd
import pyautogui
import subprocess
import os
import time
from dict2xml import dict2xml

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
                    str(self.path + '/ids_excel_template.xlsx'),
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

    def xml_to_pdf(self):
        subprocess.Popen(
            ['xdg-open {}{}'.format(self.path, '/updated_IDS.pdf')],   #xdg-open opens file with the preferred application.
            shell=True
        )
        time.sleep(2)
        pyautogui.hotkey('alt', 'd')
        time.sleep(0.1)
        pyautogui.press('f')
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'shift', 's')
        time.sleep(0.1)
        pyautogui.press('down')
        time.sleep(0.1)
        pyautogui.press('down')
        time.sleep(0.1)
        pyautogui.press('down')
        time.sleep(0.1)
        pyautogui.press('down')
        time.sleep(0.1)
        pyautogui.press('down')
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.hotkey('alt', 'f4')
        time.sleep(0.1)

base_folder = str(os.path.dirname(os.path.realpath(__file__)))
# ids_excel = base_folder + '/ids_excel_template.xlsx'
ids_xml_output = base_folder + '/output_xml/output.xml'
ids_pdf_output = base_folder + '/output_pdf/output.xml'
form_data = IDSForm(path=base_folder)
form_data.open_ids_excel()
form_data.create_backbone()
form_data.create_us_filing_info()
form_data.create_certification()
form_data.create_patent_cite()
form_data.create_non_patent_cite()
xml_output = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml_output = xml_output+ dict2xml(form_data.kwargs['base_data'], wrap='', indent='  ')

with open(ids_xml_output, 'w') as xml_file:
    xml_file.write(xml_output)

form_data.xml_to_pdf()

os.remove(ids_xml_output)