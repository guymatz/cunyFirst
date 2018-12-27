#!/usr/bin/env python
import sys
import os
import time
from twilio.rest import Client

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

#options = Options
#options.headless = True
#driver = webdriver.Firefox(options=options)
driver = webdriver.Firefox()
login_url = 'https://hrsa.cunyfirst.cuny.edu/oam/Portal_Login1.html'
driver.get(login_url)

driver.find_element_by_id("CUNYfirstUsernameH").clear()
driver.find_element_by_id("CUNYfirstUsernameH").send_keys('Guy.Matz77@login.cuny.edu')
driver.find_element_by_id("CUNYfirstPassword").send_keys('6VnNh0pwOh36')
driver.find_element_by_id("submit").click()

grades_url = "https://hrsa.cunyfirst.cuny.edu/psp/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL"

driver.get(grades_url)
driver.switch_to.frame('ptifrmtgtframe')
driver.find_element_by_id('DERIVED_SSS_SCT_SSS_TERM_LINK').click()

time.sleep(2)

# Select semester
driver.find_element_by_xpath('//*[@id="SSR_DUMMY_RECV1$sels$1$$0"]').click()
# click continue
driver.find_element_by_xpath('//*[@id="DERIVED_SSS_SCT_SSR_PB_GO"]').click()

grades = ''
file_grades = ''
with open('/tmp/grades.txt') as file:
    file_grades = file.read()

time.sleep(2)
for i in range(1,3):
    try:
        row = driver.find_element_by_id('trTERM_CLASSES$0_row%s' % i)
        cols = row.text.split('\n')
        grades = ",".join(cols)
    except Exception as nse:
        break

if (file_grades != grades):
    with open('/tmp/grades.txt', 'w') as file:
        file.write(grades)
    accountSID = os.environ['TWILIO_SID']
    authToken = os.environ['TWILIO_TOKEN']
    from_number = os.environ['TWILIO_FROM_NUM']
    to_number = os.environ['TWILIO_TO_NUM']
    print("Why Am I texting here")
    print("grades: %s" % grades)
    print("file_grades: %s" % file_grades)
    twilio = Client(accountSID, authToken)
    message = twilio.messages.create(body="Grades!\n%s" % grades, from_=from_number, to=to_number)
	

# Go to top frame
driver.switch_to.default_content()
# And log out
driver.find_element_by_xpath('//*[@id="pthdr2logout"]').click()

time.sleep(2)

driver.close()
