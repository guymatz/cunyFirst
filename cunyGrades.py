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
login_url = 'https://hrsa.cunyfirst.cuny.edu/oam/Portal_Login1.html'
driver.get(login_url)
logging.debug("Gotlogin page")

user = os.environ['CUNY_USERNAME']
passwd = os.environ['CUNY_PASSWORD']

driver.find_element_by_id("CUNYfirstUsernameH").clear()
driver.find_element_by_id("CUNYfirstUsernameH").send_keys(user)
driver.find_element_by_id("CUNYfirstPassword").send_keys(passwd)
driver.find_element_by_id("submit").click()
logging.debug("Logged in")

main_page_url = "https://home.cunyfirst.cuny.edu/psp/cnyepprd/EMPLOYEE/EMPL/h/?tab=DEFAULT"
driver.get(main_page_url)

# Click Student Center
driver.find_element_by_link_text('Student Center').click()
logging.debug("Clicked Stident Center")

driver.switch_to.frame('ptifrmtgtframe')
driver.find_element_by_link_text('View Grades').click()
logging.debug("Clicked 'View Grades'")

time.sleep(10)

# Select semester
logging.debug("Changing Term . . . ")
# They got rid of the cahnge term button
#driver.find_element_by_link_text('change term').click()
#time.sleep(2)
driver.find_element_by_id('SSR_DUMMY_RECV1$sels$1$$0').click()
#driver.find_element_by_id('SSR_DUMMY_RECV1$sels$0$$0').click()
# click continue
driver.find_element_by_link_text('Continue').click()

grades = ''
file_grades = ''
first_run = False
try:
    with open('grades.txt') as file:
        file_grades = file.read()
except FileNotFoundError as fne:
    first_run = True

time.sleep(2)
for i in range(1,3):
    try:
        row = driver.find_element_by_id('trTERM_CLASSES$0_row%s' % i)
        cols = row.text.split('\n')
        grades = ",".join(cols)
    except Exception as nse:
        break

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
        message = twilio.messages.create(body="Grades!\n%s" % grades, from_=from_number, to=to_number)
    else:
        print("NOT sending to twilio")


# And log out
driver.get('https://home.cunyfirst.cuny.edu/psp/cnyepprd/EMPLOYEE/EMPL/?cmd=logout')

time.sleep(2)

driver.close()
