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
# allows python to use operating system dependent functions
import os

# launch url
url = "https://data.austintexas.gov/api/id/b8wk-ku9z.json?$query=select%20max(%60month%60)%20as%20__measure_date_alias__%20where%20%60total_unique_participants%60%20IS%20NOT%20NULL%20AND%20%60month%60%20%3E%3D%20%272016-10-01T00%3A00%3A00%27%20AND%20%60month%60%20%3C%3D%20%272021-09-30T23%3A59%3A59%27&$$read_from_nbe=true&$$version=2.1"

# create a new Chrome session called driver
driver = webdriver.Chrome()
# waits for up to 30 seconds for an element before throwing an exception
driver.implicitly_wait(30)
# navigates to the link and waits until page is fully loaded
driver.get(url)

# Selenium hands the page source to BeautifulSoup
soup = BeautifulSoup(driver.page_source, "lxml")

