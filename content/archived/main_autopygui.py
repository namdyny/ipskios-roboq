import time
from Xlib.X import EnableAccess
import pyautogui
import subprocess
import os
import pandas as pd
import numpy as np

def tab_sleep():
    '''
    function for tab-sleep shortcut
    '''
    pyautogui.press('tab')
    time.sleep(0.1)

def filling_top_info(data):
    '''
    function to fill in application_number, filing_date and first_named_inventor
    parameters:    
        data: pd.Dataframe with columns listed in col_list
    '''
    # move to 1, 1 pixel for safe robot action
    pyautogui.moveTo(1, 1)
    tab_sleep()
    # list of info for part 1
    col_list = ['application_number', 'filing_date', 'first_named_inventor']
    # filing in part 1
    for col in col_list:
        pyautogui.press(list(data[col][0]))
        tab_sleep()
    # made ready for part - US Patents
    for i in range(2):
        tab_sleep()

def filling_us_patent_info(data):
    '''
    function to fill in US patent and US application
    parameters:    
        data: pd.Dataframe with columns listed in col_list
    '''
    # both part - US Patents and US Patent Application Publications require 4 tabs
    for i in range(4):
        tab_sleep()
    
    for e, row in enumerate(range(len(data))):
        # both part - US Patents and US Patent Application Publications share the same column structure
        col_list = ['patent_number', 'kind_code', 'issue_date', 'applicant_name', 'content_related']
        for col in col_list:
            pyautogui.press(list(data[col][row]))
            tab_sleep()
        if e+1 != len(data):
            pyautogui.press('enter')
            for i in range(5):
                pyautogui.hotkey('shift', 'tab')
                time.sleep(0.1)

def filling_foreign_application(data):
    '''
    function to fill in foreign patent application
    parameters:    
        data: pd.Dataframe with columns listed in col_list
    '''
    # both part - US Patents and US Patent Application Publications require 4 tabs
    for i in range(5):
        tab_sleep()
    
    for e, row in enumerate(range(len(data))):
        # both part - US Patents and US Patent Application Publications share the same column structure
        col_list = ['patent_number', 'country_code', 'kind_code', 'issue_date', 'applicant_name', 'content_related']
        for col in col_list:
            pyautogui.press(list(data[col][row]))
            tab_sleep()
        if e+1 != len(data):
            pyautogui.press('enter')
            for i in range(6):
                pyautogui.hotkey('shift', 'tab')
                time.sleep(0.1)


base_ids_pdf = str(os.path.dirname(os.path.realpath(__file__)) + '/updated_IDS.pdf')
ids_excel = str(os.path.dirname(os.path.realpath(__file__)) + '/ids_excel_template.xlsx')

def open_file_default_app(path):
    '''
    aim: for opening up pdf files using acrobat
    '''    
    subprocess.Popen(
        ['xdg-open {}'.format(path)],   #xdg-open opens file with the preferred application.
        shell=True
    )
    time.sleep(2)   # time require for loadup
    pyautogui.moveTo(1, 1)  # move to 1, 1 pixel for safe robot action
    tab_sleep()

def open_ids_excel(path):
    '''
    aim: read all sheets from the template excel
    '''
    df_header_fields = pd.read_excel(
        path,
        sheet_name='header_fields',
        dtype=str
    ).fillna('')    # fillna() to replace nan with ''
    df_us_patents = pd.read_excel(
        path,
        sheet_name='us_patents',
        dtype=str
    ).fillna('')
    df_us_applications = pd.read_excel(
        path,
        sheet_name='us_applications',
        dtype=str
    ).fillna('')
    df_foreign_applications = pd.read_excel(
        path,
        sheet_name='foreign_applications',
        dtype=str
    ).fillna('')
    df_non_patents = pd.read_excel(
        path,
        sheet_name='non_patents',
        dtype=str
    ).fillna('')
    return df_header_fields, df_us_patents, df_us_applications, df_foreign_applications, df_non_patents

def fill_header_fields(df):
    col_list = df.keys()
    for col in col_list:
        if df[col][0] != '':
            pyautogui.press(list(df[col][0]))
            tab_sleep()
        else:
            tab_sleep()


open_file_default_app(base_ids_pdf)
df_header_fields, df_us_patents, df_us_applications, df_foreign_applications, df_non_patents = open_ids_excel(ids_excel)
fill_header_fields(df_header_fields)


# df_basic_info = pd.DataFrame(
#     data={
#         'application_number': ['87654321'],
#         'filing_date': ['2020-12-31'],
#         'first_named_inventor': ['ABCDEFG'],
#     }
# )
# filling_top_info(df_basic_info)

# df_us_granted = pd.DataFrame(
#     data={
#         'patent_number': ['12345678', '87654321'],
#         'kind_code': ['A1', 'A2'],
#         'issue_date': ['2021-01-01', '2021-06-01'],
#         'applicant_name': ['ABC ltd.', 'DEF Co., Ltd.'],
#         'content_related': ['page 1 column 10-11, claims 1-3', 'page 2, column 7-9, claims 4-6'],
#     }
# )
# filling_us_patent_info(data=df_us_granted)

# df_us_application = pd.DataFrame(
#     data={
#         'patent_number': ['12345678910', '10987654321'],
#         'kind_code': ['B1', 'B2'],
#         'issue_date': ['2021-07-01', '2021-07-02'],
#         'applicant_name': ['HIJ ltd.', 'KLM Co., Ltd.'],
#         'content_related': ['page 7 column 3-4, claims 8-9', 'page 5, column 7, claims 3-4'],
#     }
# )
# filling_us_patent_info(data=df_us_application)

# df_foreign_application = pd.DataFrame(
#     data={
#         'patent_number': ['12345678910A', '10987654321B'],
#         'country_code': ['CN', 'GB'],
#         'kind_code': ['B1', 'B2'],
#         'issue_date': ['2021-03-01', '2021-04-02'],
#         'applicant_name': ['XYZ ltd.', 'ZYX Co., Ltd.'],
#         'content_related': ['page 5 column 3-7, claims 8-11', 'page 6, column 5, claims 1-4'],
#     }
# )
# filling_foreign_application(df_foreign_application)