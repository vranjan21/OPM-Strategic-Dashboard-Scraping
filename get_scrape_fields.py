# make sure you install selenium and BeautifulSoup and pandas and lxml parser using
# python3 -m pip install -U selenium
# python3 -m pip install beautifulsoup4
# pip install pandas
# pip install lxml

# make sure you have the right version chrome driver in the /venv/bin

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
# regex
import re
import pandas as pd

#import date time package
from datetime import datetime

# imports csv
import csv

import os  # allows python to use operating system dependent functions
from selenium.webdriver.support.ui import WebDriverWait  # wait for the page to load
from selenium.webdriver.support import expected_conditions  # wait for the page to load

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# import json
import json

# import url
import urllib.request

# access the Measure JSON definition API endpoint
JSON_META_START_URL = "https://data.austintexas.gov/api/views/metadata/v1/"

# create a new chrome session called driver
driver = webdriver.Chrome()

# set driver to wait for up to 30 seconds for an element before throwing an exception
driver.implicitly_wait(30)

# can totally just navigate to a "waiting for json measure" page or something to populate the chrome window
# might be necessary if API calls take a really long time before it starts navigating somewhere

four_by_four_list = []

# open the list of measure 4x4s in read mode
with open('measures_four_by_four_list.csv', 'r') as read_obj:
    # pass the file object to csv.reader() to get the reader object
    csv_reader = csv.reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # link variable is a list that represents a link in each csv
        for link in row:
            # adds the link to the list of urls
            four_by_four_list.append(link)

measure_link_list = []

measure_value_list = []

measure_color_list = []

most_recent_reporting_year_list = []

reporting_frequency_list = []

page_update_date_list = []


for four_by_four in four_by_four_list:
    print(four_by_four)
    # internal testing only - adds the link of the measure to a list for the output
    measure_link = 'https://data.austintexas.gov/d/' + four_by_four
    measure_link_list.append(measure_link)

    measure_json_url = JSON_META_START_URL + four_by_four
    measure_meta = json.load(urllib.request.urlopen(measure_json_url))

    # get the measure page URL from the metadata
    scrape_url = measure_meta['dataUri']

    # navigate Selenium chrome driver to the measure page URL and waits until page is fully loaded
    driver.get(scrape_url)

 # wait until calculated measure result number is fully loaded
    try:
        WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "measure-result-big-number")))
    except TimeoutException:
        print("link not found ... breaking out")
        print()

    # Selenium hands the page source to BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "lxml")


# write the csv files
# note: to get apostrophes to display properly in excel have to encode as utf-8
with open('scrape_fields.csv', 'w', encoding='utf-8-sig') as myfile:

    # feeds the field names in through a Python Dictionary
    # also has a quote_all argument - formats everything in the csv with quotes debatable whether to keep this or not
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)


    # write each of the field columns  to csv
    index = 0
    list_length = len(four_by_four_list)

    wr.writerow(['4x4 (testing only)', 'Measure Link (testing only)', 'Most Recent Reporting Year',
                 'Reporting Frequency', 'Page Update Date'])
    while index < list_length:
        wr.writerow([four_by_four_list[index], measure_link_list[index], most_recent_reporting_year_list[index],
                     reporting_frequency_list[index], page_update_date_list[index]])
        index = index + 1
