#!/usr/bin/env python
import sys
import os
from mechanize import Browser, Request
import urllib
import cookielib
import argparse
from BeautifulSoup import BeautifulSoup
import xml.etree.ElementTree
from twilio.rest import TwilioRestClient

url = 'https://hrsa.cunyfirst.cuny.edu/oam/Portal_Login1.html'
jar = cookielib.LWPCookieJar()
br = Browser()
br.set_cookiejar(jar)
br.set_handle_robots(False)
br.open(url)
username = os.environ['CUNYID']
password = os.environ['CUNYPASS']
br.select_form(nr=0)
br["username"] = username
br["password"] = password
br.submit()

def w(ofile, browser):
    ofile = "%s.html" % ofile
    with open(ofile, 'w') as f:
        f.write(browser.response().get_data())


# br.set_debug_http(sys.stdout)
# br.set_debug_redirects(sys.stdout)
# br.set_debug_responses(sys.stdout)

#br.open("https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL?Page=SSR_SSENRL_GRADE&Action=A&TargetFrameName=None")
br.open("https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL")
w('now', br)

br.select_form(nr=0)
f = br.form
change_term_url = f.action
data = {}
for k,v in f.click_pairs():
    data[k] = v

data['ICAction'] = 'DERIVED_SSS_SCT_SSS_TERM_LINK'
# Do I need this section?
encData = urllib.urlencode(data)
req = Request(change_term_url, data=encData, headers={"Content-type": "application/x-www-form-urlencoded"})
br.open(req)
w('now1', br)

br.select_form(nr=0)
f = br.form
change_term_url = f.action
data = {}
for k,v in f.click_pairs():
    #print("Adding %s : %s" % (k,v))
    data[k] = v

data['ICAction'] = 'DERIVED_SSS_SCT_SSR_PB_GO'
data['ICAJAX'] = '1'
data['ICNAVTYPEDROPDOWN'] = '0'
data['ResponsetoDiffFrame'] = '-1'
data['SSR_DUMMY_RECV1$sels$1$$0'] = '1'
data['ICBcDomData'] = 'undefined'
data['SSR_DUMMY_RECV1$sels$0'] = '1'
##@#
encData = urllib.urlencode(data)
req = Request(change_term_url, data=encData, headers={"Content-type": "application/x-www-form-urlencoded"})
# br.set_debug_http(sys.stdout)
#br.set_debug_redirects(sys.stdout)
#br.set_debug_responses(sys.stdout)
br.open(req)

#d = br.response().get_data()
x = xml.etree.ElementTree.fromstring(br.response().get_data())[6]
soup = BeautifulSoup(x.text)
divs = soup.findAll('div')
d21 = divs[21]
#print(d21.text)
c = d21.contents[0]
children = c.findChildren()
grade_line = children[64]
new_grade = grade_line.text
#print("grade = %s" % new_grade)

changed = False

try:
    with open('grades.flag') as file:
        old_grade = file.read()
        if new_grade != old_grade:
            changed = True
except Exception as e:
    with open('grades.flag', 'w') as file:
        file.write(new_grade)
    

br.open('https://home.cunyfirst.cuny.edu/psp/cnyepprd/EMPLOYEE/EMPL/?cmd=logout')

if changed:
    accountSID = os.environ['TWILIO_SID']
    authToken = os.environ['TWILIO_TOKEN']
    from_number = os.environ['TWILIO_FROM_NUM']
    to_number = os.environ['TWILIO_TO_NUM']
    twilio = TwilioRestClient(accountSID, authToken)
    message = twilio.messages.create(body="Grades!", from_=from_number, to=to_number)
