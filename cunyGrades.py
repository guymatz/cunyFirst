import sys
from mechanize import Browser, Request
import urllib
import Cookie
import cookielib
import argparse
#from BeautifulSoup import BeautifulSoup
from datetime import datetime

url='https://hrsa.cunyfirst.cuny.edu/oam/Portal_Login1.html'
jar = cookielib.LWPCookieJar()
br = Browser()
br.set_cookiejar(jar)
br.set_handle_robots(False)
br.open(url)
username = 'Guy.Matz77'
password = '*********'
br.select_form(nr=0)
br["login"] = username
br["password"] = password
br.submit()

def w(ofile, browser):
    ofile = "%s.html" % ofile
    with open(ofile, 'w') as f:
        f.write(browser.response().get_data())


br.set_debug_http(sys.stdout)
br.set_debug_redirects(sys.stdout)
br.set_debug_responses(sys.stdout)
        
br.open("https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL?Page=SSR_SSENRL_GRADE&Action=A&TargetFrameName=None")
w('now', br)

br.select_form(nr=0)
ICSID = br.form['ICSID']

change_term_url = 'https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL'

data={
    'ICAJAX': '1',
    'ICNAVTYPEDROPDOWN': '0',
    'ICType': 'Panel',
    'ICElementNum': '0',
    'ICStateNum': '2',
    'ICAction': 'DERIVED_SSS_SCT_SSS_TERM_LINK',
    'ICXPos': '0',
    'ICYPos': '0',
    'ResponsetoDiffFrame': '-1',
    'TargetFrameName': 'None',
    'FacetPath': 'None',
    'ICFocus': '',
    'ICSaveWarningFilter': '0',
    'ICChanged': '-1',
    'ICAutoSave': '0',
    'ICResubmit': '0',
    'ICActionPrompt': 'false',
    'ICBcDomData': 'undefined',
    'ICFind': '',
    'ICAddCount': '',
    'ICAPPCLSDATA': '',
    'DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$': '9999',
    'DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$': '9999',
    'ptus_defaultlocalnode': 'PSFT_CNYHCPRD',
    'ptus_dbname': 'CNYHCPRD',
    'ptus_portal': 'EMPLOYEE',
    'ptus_node': 'HRMS',
    'ptus_workcenterid': '',
    'ptus_componenturl': 'https://hrsa.cunyfirst.cuny.edu/psp/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL'
    }
data['ICSID'] = ICSID
data['ICAction']='DERIVED_SSS_SCT_SSR_PB_GO'
data['SSR_DUMMY_RECV1$sels$1$$0']='1'

encData = urllib.urlencode(data)
req = Request(change_term_url, data=encData, headers={"Content-type": "application/x-www-form-urlencoded"})
br.open(req)
w('now1', br)

##@# data['ICAction']='DERIVED_SSS_SCT_SSR_PB_GO'
##@# data['SSR_DUMMY_RECV1$sels$1$$0']='1'
##@# 
##@# encData = urllib.urlencode(data)
##@# req = Request(change_term_url, data=encData, headers={"Content-type": "application/x-www-form-urlencoded"})
##@# br.open(req)
##@# w('now2', br)
##@# 
##@# 
##@# br.open('https://home.cunyfirst.cuny.edu/psp/cnyepprd/EMPLOYEE/EMPL/?cmd=logout')
##@# 
