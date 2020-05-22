#!/usr/bin/env python
import sys
import os
import time
from twilio.rest import Client

from selenium import webdriver

# if we're on a TTY and not in a byobu environment
if os.isatty(sys.stdin.fileno()) and not os.environ.get('BYOBU_TTY'):
    driver = webdriver.Firefox()
else:
    options = webdriver.FirefoxOptions()
    options.set_headless()
    driver = webdriver.Firefox(firefox_options=options)
login_url = 'https://hrsa.cunyfirst.cuny.edu/oam/Portal_Login1.html'
driver.get(login_url)

u=os.environ['CUNY_USERNAME']
p=os.environ['CUNY_PASSWORD']

driver.find_element_by_id("CUNYfirstUsernameH").clear()
driver.find_element_by_id("CUNYfirstUsernameH").send_keys(u)
driver.find_element_by_id("CUNYfirstPassword").send_keys(p)
driver.find_element_by_id("submit").click()

main_page_url = "https://home.cunyfirst.cuny.edu/psp/cnyepprd/EMPLOYEE/EMPL/h/?tab=DEFAULT"
driver.get(main_page_url)

# Click Student Center
driver.find_element_by_link_text('Student Center').click()

driver.switch_to.frame('ptifrmtgtframe')
driver.find_element_by_link_text('View Grades').click()

time.sleep(4)

# Select semester
driver.find_element_by_link_text('change term').click()
time.sleep(2)
driver.find_element_by_id('SSR_DUMMY_RECV1$sels$1$$0').click()
# click continue
driver.find_element_by_link_text('Continue').click()

grades = ''
file_grades = ''
with open('grades.txt') as file:
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
    with open('grades.txt', 'w') as file:
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
	

# And log out
driver.get('https://home.cunyfirst.cuny.edu/psp/cnyepprd/EMPLOYEE/EMPL/?cmd=logout')

time.sleep(2)

driver.close()
