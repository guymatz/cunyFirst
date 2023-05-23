#!/usr/bin/env python
import sys
import os
import time
from twilio.rest import Client
import logging
from selenium import webdriver

if ('-d' in sys.argv):
    logging.basicConfig(level=logging.DEBUG)

# if we're on a TTY and not in a byobu environment
if os.isatty(sys.stdin.fileno()) and not os.environ.get('BYOBU_TTY'):
    driver = webdriver.Firefox()
else:
    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)

#login_url = 'https://hrsa.cunyfirst.cuny.edu/oam/Portal_Login1.html'
#login_url = 'https://ssologin.cuny.edu/cuny.html'
# This seems to be the best URL at the moment
login_url = 'https://home.cunyfirst.cuny.edu/psp/cnyepprd/EMPLOYEE/EMPL/h/?tab=DEFAULT'
driver.get(login_url)
logging.debug("Gotlogin page")

user = os.environ['CUNY_USERNAME']
passwd = os.environ['CUNY_PASSWORD']

driver.find_elements("id", "CUNYfirstUsernameH")[0].clear()
driver.find_elements("id", "CUNYfirstUsernameH")[0].send_keys(user)
driver.find_elements("id", "CUNYfirstPassword")[0].send_keys(passwd)
driver.find_elements("id", "submit")[0].click()
logging.debug("Logged in")

main_page_url = "https://home.cunyfirst.cuny.edu/psc/cnyihprd/EMPLOYEE/EMPL/c/NUI_FRAMEWORK.PT_LANDINGPAGE.GBL"
driver.get(main_page_url)

# Click Student Center
#driver.find_element_by_link_text('Student Center').click()
ss_url = "https://home.cunyfirst.cuny.edu/psc/cnyihprd/EMPLOYEE/EMPL/c/NUI_FRAMEWORK.PT_LANDINGPAGE.GBL?LP=CU_CS_SCC_STUDENT_HOMEPAGE_FL"
driver.get(ss_url)
logging.debug("Clicked Stident Center")

records_url = "https://cssa.cunyfirst.cuny.edu/psc/cnycsprd_7/EMPLOYEE/SA/c/SSR_STUDENT_ACAD_REC_FL.SSR_MD_ACAD_REC_FL.GBL?Action=U&MD=Y&GMenu=SSR_STUDENT_ACAD_REC_FL&GComp=SSR_ACADREC_NAV_FL&GPage=SCC_START_PAGE_FL&scname=CS_SSR_ACADEMIC_RECORDS_FL"
driver.get(records_url)

#driver.switch_to.frame('ptifrmtgtframe')
time.sleep(10)
driver.find_elements('link text', 'View Grades')[0].click()
logging.debug("Clicked 'View Grades'")

time.sleep(5)

# Select semester
try:
    term = driver.find_element('id', 'TERM_GRID$0_row_0')
    term.click()
except Exception as e:
    logging.debug("No need to change term?")

time.sleep(10)
grades = driver.find_element('css selector', 'tbody.ps_grid-body').text

file_grades = ''
first_run = False
try:
    with open('grades.txt') as file:
        file_grades = file.read()
except FileNotFoundError as fne:
    first_run = True

logging.debug("Got grades")

with open('grades.txt', 'w') as file:
    file.write(grades)

if (file_grades != grades) and not first_run:
    accountSID = os.environ['TWILIO_SID']
    authToken = os.environ['TWILIO_TOKEN']
    from_number = os.environ['TWILIO_FROM_NUM']
    to_number = os.environ['TWILIO_TO_NUM']
    print("Why Am I texting here")
    print("grades: %s" % grades)
    print("file_grades: %s" % file_grades)
    if os.environ.get('TWILIO_SEND'):
        twilio = Client(accountSID, authToken)
        message = twilio.messages.create(
            body="Grades!\n%s" % grades, from_=from_number, to=to_number)
    else:
        print("NOT sending to twilio")


# And log out
driver.get('https://home.cunyfirst.cuny.edu/psp/cnyepprd/EMPLOYEE/EMPL/?cmd=logout')

time.sleep(2)

driver.close()
