# -*- coding: utf-8 -*-
#!/usr/bin/python

from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

### Watch-out: installing Selenium requires Gekko and it may be easier to configure it with Chrome
geckk=r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'

'''Documentation & resources to help set-up & use selenium:  
    https://www.tutorialspoint.com/python_web_scraping/python_web_scraping_dynamic_websites.htm
    https://www.selenium.dev/documentation/en/webdriver/web_element/
    https://realpython.com/modern-web-automation-with-python-and-selenium/
    https://stackoverflow.com/questions/7861775/python-selenium-accessing-html-source
    https://stackoverflow.com/questions/51273995/selenium-python-dynamic-table
'''

### Set options for Selenium 
options = webdriver.FirefoxOptions()
options.headless = True
options.add_argument("disable-gpu")
options.add_argument("headless")
options.add_argument("no-default-browser-check")
options.add_argument("no-first-run")
options.add_argument("no-sandbox")
options.add_argument("marionette=True")
options.add_argument("--test-type")
options.set_preference('browser.download.manager.showWhenStarting', False)
options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
options.set_preference("browser.download.folderList",2)
options.set_preference("browser.download.manager.showWhenStarting",False)
options.set_preference("browser.download.dir","c:\\downloads")

profile = webdriver.FirefoxProfile()
profile.accept_untrusted_certs = True

driver = webdriver.Firefox(firefox_binary=geckk,options=options, firefox_profile=profile)

### Download
driver.get("https://datawrapper.dwcdn.net/tr5bJ/16/")
soup=BeautifulSoup(driver.page_source, 'html.parser')

### Get the data required (didn't manage to do differently than browsing across text)
data_cursor_start=soup.text.find('chartData: "')
data_cursor_stop=data_cursor_start+soup.text[data_cursor_start:].find('",')
zoom=str(soup.text)[data_cursor_start:data_cursor_stop]

### Create DataFrame
table_lines=zoom.split('\\n')
line_array=[]
for each_line in table_lines[1:]:
    line=each_line.split('\\t')
    line_array += line
line_matrix= [line_array[x:x+5] for x in range(0, len(line_array),5)]

df=pd.DataFrame(line_matrix, columns=['date', 'ncumul_hosp','ncumul_released','ncumul_deceased','ncumul_conf'])
df['date']=pd.to_datetime(df['date'],yearfirst=True)
df['abbreviation_canton_and_fl']='VD'
df['time']=np.NaN
df['ncumul_tested']=np.NaN
df['ncumul_ICU']=np.NaN
df['ncumul_vent']=np.NaN
df['source']='https://datawrapper.dwcdn.net/tr5bJ/16/'

### Format & Save CSV
new_order=['date','time','abbreviation_canton_and_fl','ncumul_tested','ncumul_conf',\
           'ncumul_hosp','ncumul_ICU','ncumul_vent','ncumul_released','ncumul_deceased','source']
df=df.T.reindex(new_order).T.set_index('date')

df.to_csv('COVID19_Fallzahlen_Kanton_VD_total.csv')
