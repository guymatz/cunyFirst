#!/usr/bin/env python

import sys
from mechanize import Browser, Item
import Cookie
import cookielib
import argparse
#from BeautifulSoup import BeautifulSoup

url='https://hrsa.cunyfirst.cuny.edu/oam/Portal_Login1.html'

parser = argparse.ArgumentParser(description='Check availability of CUNY classes in CUNYFirst')
parser.add_argument('--username', metavar='Username', type=str, required=True,
                   help='CUNY Username, e.g. Guy.Matz77')
parser.add_argument('--password', metavar='Password', type=str, required=True,
                   help='CUNY Password')
parser.add_argument('--college', metavar='College', type=str, required=True,
                   help='subject to search for, e.g. HTR')
parser.add_argument('--subject', metavar='Subject', type=str, required=True,
                   help='subject to search for, e.g. STAT')
parser.add_argument('--klass', metavar='Class#', type=str, required=True,
                   help='class # to search for, e.g. 31100')
parser.add_argument('--debug', action='store_true',
                   help='Print debug output and write responses to file')
args = parser.parse_args()

def writeout(ofile, browser):
  if args.debug:
    ofile = "%s.html" % ofile
    f = open(ofile, 'w')
    f.write(browser.response().get_data())
    f.close()
  else:
    return

def logout(browser):
  if args.debug: print("Logging out")
  browser.open('https://home.cunyfirst.cuny.edu/psp/cnyepprd/EMPLOYEE/EMPL/?cmd=logout')

def set_ICAction(browser):
  mods = browser.find_control('ICAction')
  mods.readonly = False
  browser['ICAction']='CLASS_SRCH_WRK2_INSTITUTION$42$'

jar = cookielib.LWPCookieJar()
br = Browser()
br.set_cookiejar(jar)
#proxy='127.0.0.1:8888'; br.set_proxies(proxies={'https':proxy, 'http':proxy})
br.set_handle_robots(False)
if args.debug: print("Getting Login page . . .")
br.open(url)
br.select_form(nr=0)
br["login"] = args.username
br["password"] = args.password
if args.debug: print("Logging in . . .")
br.submit()
writeout("past_login", br)

if args.debug: print("Getting search page . . .")
br.open("https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL")
writeout("on_search_form", br)

br.select_form(nr=0)

# How do I change this next semester?
mods = br.find_control('CLASS_SRCH_WRK2_STRM$45$')
item1 = Item(mods, {"contents": "1162", "value": "1162"})
item1.selected=True

mods = br.find_control('SSR_CLSRCH_WRK_SUBJECT_SRCH$0')
item2 = Item(mods, {"contents": args.subject, "value": args.subject})
item2.selected=True

# Next semester?
br['CLASS_SRCH_WRK2_STRM$45$']=['1162']
br['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$155$']=['9999']
br['CLASS_SRCH_WRK2_INSTITUTION$42$']=[args.college + '01']
br['SSR_CLSRCH_WRK_SSR_EXACT_MATCH1$1']=['E']
br.form['SSR_CLSRCH_WRK_CATALOG_NBR$1']=args.klass
br['SSR_CLSRCH_WRK_SUBJECT_SRCH$0']=[args.subject]
writeout("without_ICAction", br)

try:
  set_ICAction(br)
  mods = br.find_control('ICAction')
  mods.readonly = False
  br['ICAction']='CLASS_SRCH_WRK2_INSTITUTION$42$'
  writeout("with_ICAction", br)
except:
  print("set_ICAction did not work")
if args.debug: print("Submitting search page . . .")
br.submit()
writeout("past_search_form", br)

if args.debug: print("Submitting search page again . . !")
try:
  br.select_form(nr=0)
  mods = br.find_control('ICAction')
  mods.readonly = False
  br['ICAction']='CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH'
  br.form['SSR_CLSRCH_WRK_CATALOG_NBR$1'] = args.klass
  br['SSR_CLSRCH_WRK_SUBJECT_SRCH$0'] = [args.subject]
  br.submit()
  writeout("past_search_form_II", br)
except Exception as e:
  print("Failed submitting page again: ", e)
  logout(br)
  sys.exit()

content = br.response().get_data()
writeout("done", br)
logout(br)

if content.find('The search returns no results that match the criteria specified'):
  print("Boo!")
else:
  print("Yay!")

sys.exit(0)
