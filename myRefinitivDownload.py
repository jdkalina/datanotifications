from selenium import webdriver
import time
from datetime import datetime
import re
import glob
import pandas as pd


def myAccountLogin(webdriver_object, userid, pw):
    webdriver_object.get("https://login.cp.thomsonreuters.net/auth/idpssoinit?NameIDFormat=urn%3Aoasis%3Anames%3Atc%3ASAML%3A1.1%3Anameid-format%3AemailAddress&metaAlias=/reuters/idp&spEntityID=https%3A//saml.salesforce.com&binding=urn%3Aoasis%3Anames%3Atc%3ASAML%3A2.0%3Abindings%3AHTTP-POST&RelayState=MTRIntermediatePage%3Ftarget=/apex/home")
    
    #Page 2 inputs
    user_id_fld = webdriver_object.find_element_by_css_selector("input[id='AAA-AS-SI1-SE003']")
    pass_wd_fld = webdriver_object.find_element_by_css_selector("input[id='AAA-AS-SI1-SE006']")
    sign_in_btn = webdriver_object.find_element_by_css_selector("div[id='AAA-AS-SI1-SE014']")
    
    #Page 2 manipulate
    user_id_fld.send_keys(userid)
    pass_wd_fld.send_keys(pw)
    sign_in_btn.click()


def downloadDNs(webdriver_object):
    dl_dn_url = 'https://my.thomsonreuters.com/pages?name=weeklynotifications'
    webdriver_object.get(dl_dn_url)
    time.sleep(.5)
    xpath = "//*[@id='j_id0:j_id4:j_id175:j_id203:1:j_id219:j_id220:j_id241:0:j_id243']/a"
    link_cn = webdriver_object.find_element_by_xpath(xpath)
    link_cn.click()
    time.sleep(.5)
    

def readNotifications(download_dir_path = "C:\\Users\\u6037148\\Downloads", config_file = "C:\\venvs\\projects\\datanotifications\\config.xls"):
    """This function is used to read the downloaded excel documents into dataframes in pandas. Looks to dynamically find files based on day. Recommended to purge your download directory every month.
    This function will return a pandas dataframe and a summary of the before and after transformations.
    
    :download_dir_path: this defines the path to where your browser downloads files. Directories need to be defined with two '\' to account for regular expressions in Python.
    """
    today_day = str(datetime.today().day)
    dnfile = glob.glob(download_dir_path + "\\.*Content Change Notifications.*")
	if len(dnfile) > 1:
		dnfile= dnfile[0]
    df = pd.read_excel(dnfile)
    before_sort = df.shape[0]
    
    change_type = pd.read_excel(config_file,sheetname='Change Type')
    assoc_prod = pd.read_excel(config_file,sheetname='Associated Products')

    assoc_prod = assoc_prod[assoc_prod['include'] == "Y"]['Associated Products']
    change_type = change_type[change_type['include'] == "Y"]['Change Type']
    
    df['Boolean Product'] = False
    for prod in assoc_prod:
        for index,value in enumerate(df['Associated Products']):
            try: 
                test = bool(re.match(prod, value))
                if test:
                    df['Boolean Product'][index] = True
                else:
                    continue
            except:
                df['Boolean Product'][index] = False

    df['Boolean Change Type'] = False
    for chtype in change_type:
        for index,value in enumerate(df['Change Type']):
            try: 
                test = bool(re.match(chtype, value))
                if test:
                    df['Boolean Change Type'][index] = True
                else:
                    continue
            except:
                df['Boolean Change Type'][index] = False
    final_product = df[df['Boolean Product'] & df['Boolean Change Type']]
    print("Raw file has a total of " + str(before_sort) + " number of rows")
    print("Sorted file has a total of " + str(final_product.shape[0]) + " number of rows")
    return final_product
    
    
browser = webdriver.Chrome()    
myAccountLogin(browser, userid = "", pw = "")
downloadDNs(browser)
my_df = readNotifications()
my_df.to_csv("D:\\notifications\\ElektronDataNotifications.csv")
browser.quit()
