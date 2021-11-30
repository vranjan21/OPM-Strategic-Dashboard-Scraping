# make sure you install selenium and BeautifulSoup and pandas and lxml parser using
# python3 -m pip install -U selenium
# python3 -m pip install beautifulsoup4
# pip install pandas
# pip install lxml

# make sure you have the right version chrome driver in the /venv/bin

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
# regex
import re
from regex import regex

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

from datetime import datetime

# import json
import json

# import url
import urllib.request

JSON_META_START_URL = "https://data.austintexas.gov/api/views/metadata/v1/"

# create a new chrome session called driver
driver = webdriver.Chrome(ChromeDriverManager().install())

# set driver to wait for up to 30 seconds for an element before throwing an exception
driver.implicitly_wait(30)

# can totally just navigate to a "waiting for json measure" page or something to populate the chrome window
# might be necessary if API calls take a really long time before it starts navigating somewhere

four_by_four_list = []
measure_link_list = []
story_link_list = []

# open the list of measure 4x4s in read mode
with open('api_fields.csv', 'r') as read_obj:
    # pass the file object to csv.reader() to get the reader object
    csv_reader = csv.reader(read_obj)

    # skip the first row of headers
    next(csv_reader)

    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # link variable is a list that represents a link in each csv
        four_by_four_list.append(row[0])
        measure_link_list.append(row[1])
        story_link_list.append(row[10])

print(four_by_four_list)
print(measure_link_list)
print(story_link_list)

measure_id_list = []

measure_name_list = []

measure_value_list = []

measure_status_list = []

measure_target_value_list = []

recent_reporting_year_list = []

reporting_frequency_list = []

page_update_date_list = []

measure_data_last_timestamp_list = []

MEASURE_ID_SEARCH = re.compile("^.*?(?=(_|-| ))")
FREQUENCY_MEASURE_SEARCH = re.compile("(?<=Reported:.)[^\n]*(?=Date)")
FREQUENCY_MEASURE_NO_UPDATE_SEARCH = re.compile("(?<=Reported:.)[^\n]*(?=Present)")
PAGE_UPDATE_DATE_SEARCH = re.compile("(?<=last updated:.)[^\n]*(?=Present)")

# iterates through url list
for four_by_four in four_by_four_list:
    print(four_by_four)
    # constructs the json URL for the two API calls
    measure_meta_one_url = "https://data.austintexas.gov/api/views/metadata/v1/" + four_by_four
    measure_meta_two_url = "https://data.austintexas.gov/api/measures_v1/" + four_by_four

    # get the raw JSON object from the first metadata url
    measure_meta_one = json.load(urllib.request.urlopen(measure_meta_one_url))

    # get the raw JSON object from the second metadata url
    measure_meta_two = json.load(urllib.request.urlopen(measure_meta_two_url))

    # get the date the measure was last updated
    measure_name_full = measure_meta_one['name']
    print(measure_name_full)

    # search for the measure name using the compiled regex search
    measure_id = re.search(MEASURE_ID_SEARCH, measure_name_full).group(0)

    # compile a regex expression to get the rest of the name
    measure_name_search = re.compile("(?<=" + measure_id + ").*")

    measure_name = re.search(measure_name_search, measure_name_full).group(0)[1:]

    print(measure_id)
    print(measure_name)

    # checks whether the target value exists
    if 'value' in measure_meta_two['metricConfig']['targets'][0]:
        target_value_index = -1

        # while the target value doesn't exist for the last element of the list,
        # de-iterate until there exists a target value
        while 'value' not in measure_meta_two['metricConfig']['targets'][target_value_index]:
            # if value exists, collect the value of the target
            target_value_index = target_value_index - 1

        # stores the very last existing
        measure_target_value = measure_meta_two['metricConfig']['targets'][target_value_index]['value']

    else:
        # if value does not exist, make the value "does not exist"
        measure_target_value = "Does not exist"

    print(measure_target_value)

    # get the date the measure was last updated
    last_timestamp_string = measure_meta_one['metadataUpdatedAt']
    last_timestamp_datetime = datetime.strptime(last_timestamp_string, '%Y-%m-%dT%H:%M:%S+0000')
    measure_data_last_timestamp = last_timestamp_datetime.strftime("%m/%d/%Y")

    print(measure_data_last_timestamp)

    # internal testing only - adds the link of the measure to a list for the output
    measure_link = 'https://data.austintexas.gov/d/' + four_by_four
    measure_link_list.append(measure_link)

index = 0
list_length = len(four_by_four_list)

while index < list_length:
    print(four_by_four_list[index])
    # MEASURE PAGE:
    # scraping the measure page values
    # gets the next measure page link
    scrape_url = measure_link_list[index]

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

    # TO-DO: collect data from the measure page and store in the corresponding lists
    # TO-DO: Measure Value
    # TO-DO: Color of Measure Card - may be redundant, can just use the status of measure card
    # TO-DO: Status of Measure Card
    # TO-DO: Most Recent Reporting Year
    # TO-DO: add try and except clauses to all actions

    # locates and stores the text of the tag with the class "measure-result-big-number"
    measure_value = soup.find(class_="measure-result-big-number").text
    print(measure_value)

    # appends the measure value to the list
    measure_value_list.append(measure_value)

    # locates and stores the measure status (ex. On Track, Off Track, etc)
    try:
        measure_status = soup.find(class_="status-banner-text").text
    except AttributeError:
        # if this value doesn't exist, print that it Does not exist
        measure_status = "Does not exist"

    print(measure_status)

    # appends the measure status to the list
    measure_status_list.append(measure_status)

    # locates and stores the reporting year range
    # this is in the format of 1/1/20 - 12/31/20
    try:
        recent_reporting_year_range = soup.find(class_="reporting-period-latest").text
        # gets the last two characters/digits of the recent reporting year range
        # appends "20" to the start of the last two characters/digits
        # stores the value as recent_reporting_year
        #recent_reporting_year = "20" + recent_reporting_year_range[-2:]
        #if recent_reporting_year == '20ay':
        recent_reporting_year = datetime.now().year

    except AttributeError:
        # if this value doesn't exist, print that it Does not exist
        recent_reporting_year_range = "Does not exist"

    #print(recent_reporting_year)
    print(recent_reporting_year_range)
    # recent_reporting_year_list.append(recent_reporting_year)

    recent_reporting_year_list.append(recent_reporting_year_range)
    # TO-DO: Scrape Reporting Frequency
    # TO-DO: Scrape Page Update Date

    # STORY PAGE:
    # scraping the story page values
    # we do this separately because there are some stories that have multiple measures
    # gets the next story page link
    scrape_url = story_link_list[index]

    # if the link isn't a full URL
    if not scrape_url.startswith('http'):
        scrape_url = 'https://' + scrape_url

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

    # gets all the text of the story page as a single string
    story_text = soup.find(id="content").get_text().replace('\n', '')
    print(story_text)

    if FREQUENCY_MEASURE_SEARCH.search(story_text):
        # searches for and stores the reporting frequency in the story text
        reporting_frequency = re.search(FREQUENCY_MEASURE_SEARCH, story_text).group()
    elif FREQUENCY_MEASURE_NO_UPDATE_SEARCH.search(story_text):
        reporting_frequency = re.search(FREQUENCY_MEASURE_NO_UPDATE_SEARCH, story_text).group()
    else:
        reporting_frequency = "Does not exist"
    print(reporting_frequency)

    # appends the reporting frequency to the list of all reporting frequencies
    reporting_frequency_list.append(reporting_frequency)

    # searches for the page update date
    if PAGE_UPDATE_DATE_SEARCH.search(story_text):
        page_update_date = re.search(PAGE_UPDATE_DATE_SEARCH, story_text).group()
    else:
        page_update_date = "Does not exist"
    print(page_update_date)

    # appends the page update date to the list of all page updates
    page_update_date_list.append(page_update_date)





























































with open('all_data_fields.csv', 'w', encoding='utf-8-sig') as myfile:

    # feeds the field names in through a Python Dictionary
    # also has a quote_all argument - formats everything in the csv with quotes debatable whether to keep this or not
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

    # write each of the field columns to a csv file
    index = 0
    list_length = len(four_by_four_list)

    wr.writerow(['Measure ID',
                 'Measure Name',
                 'Story Link',
                 'Measure Value',
                 'Measure Status',
                 'Target Value',
                 'Reporting Frequency'
                 'Most Recent Reporting Year',
                 'Page Update Date'
                 'Metadata Update Date'
                ])
    while index < list_length:
        wr.writerow([measure_id_list[index],
                     measure_name_list[index],
                     story_link_list[index],
                     measure_value_list[index],
                     measure_status_list[index],
                     measure_target_value_list[index],
                     reporting_frequency_list[index],
                     recent_reporting_year_list[index],
                     page_update_date_list[index],
                     measure_data_last_timestamp_list[index]
                     ])
        index = index + 1

# end the Selenium browser session and closes the browser window
driver.quit()
