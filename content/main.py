import time
import pyautogui
import subprocess
import pandas as pd

'''
development notes:
    - require checking on page break
    - checking on T5 box
    - number of tabs and shift tabs
    - reusing filling_top_info()
'''

def tab_sleep():
    '''
    function for tab-sleep shortcut
    '''
    pyautogui.press('tab')
    time.sleep(0.1)

def open_updated_ids(path_uspto_ids):
    '''
    function to open USPTO IDS pdf file
    '''
    # open pdf with default application - Acrobat 9 (latest supportted version)
    subprocess.Popen(
        ['xdg-open {}'.format(path_uspto_ids)],
        shell=True # shell set to True, otherwise error
    )
    # normal time to open pdf
    time.sleep(2)

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

open_updated_ids(
    path_uspto_ids='/home/namdyny/Desktop/temp_git_repositories/ipskios-roboq/content/updated_IDS.pdf'
)

df_basic_info = pd.DataFrame(
    data={
        'application_number': ['87654321'],
        'filing_date': ['2020-12-31'],
        'first_named_inventor': ['ABCDEFG'],
    }
)
filling_top_info(df_basic_info)

df_us_granted = pd.DataFrame(
    data={
        'patent_number': ['12345678', '87654321'],
        'kind_code': ['A1', 'A2'],
        'issue_date': ['2021-01-01', '2021-06-01'],
        'applicant_name': ['ABC ltd.', 'DEF Co., Ltd.'],
        'content_related': ['page 1 column 10-11, claims 1-3', 'page 2, column 7-9, claims 4-6'],
    }
)
filling_us_patent_info(data=df_us_granted)

df_us_application = pd.DataFrame(
    data={
        'patent_number': ['12345678910', '10987654321'],
        'kind_code': ['B1', 'B2'],
        'issue_date': ['2021-07-01', '2021-07-02'],
        'applicant_name': ['HIJ ltd.', 'KLM Co., Ltd.'],
        'content_related': ['page 7 column 3-4, claims 8-9', 'page 5, column 7, claims 3-4'],
    }
)
filling_us_patent_info(data=df_us_application)

df_foreign_application = pd.DataFrame(
    data={
        'patent_number': ['12345678910A', '10987654321B'],
        'country_code': ['CN', 'GB'],
        'kind_code': ['B1', 'B2'],
        'issue_date': ['2021-03-01', '2021-04-02'],
        'applicant_name': ['XYZ ltd.', 'ZYX Co., Ltd.'],
        'content_related': ['page 5 column 3-7, claims 8-11', 'page 6, column 5, claims 1-4'],
    }
)
filling_foreign_application(df_foreign_application)