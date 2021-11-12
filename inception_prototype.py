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

# iterates through the measure ID list
for measure_id in ['w7fi-einn', 'vyzh-pff9']:

    # construct the measure json url to access
    measure_json_url = JSON_META_START_URL + measure_id

    # get the raw JSON object
    measure_meta = json.load(urllib.request.urlopen(measure_json_url))

    # print the raw JSON object
    print("Raw meta:")
    print(measure_meta)
    print()

    # get the date the measure was last updated
    measure_updated_at = measure_meta['dataUpdatedAt']

    # print the date the measure was last updated
    print("Data Updated On: ")
    print(measure_updated_at)
    print()

    # get the measure page URLf from the metadata
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

    # finds and stores the HTML tag with the class "measure-result-big-number"
    measure_result = soup.find(class_="measure-result-big-number")

    # prints the raw HTML of the measure result
    print("Raw Measure Result:")
    print(measure_result)
    print()

    # stores the excerpt of the actual measure value string
    measure_result_value = str(measure_result.string)

    # prints the measure result
    print("measure result string: ")
    print(measure_result_value)
    print()