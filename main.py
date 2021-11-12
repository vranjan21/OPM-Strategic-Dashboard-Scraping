# make sure you install selenium and BeautifulSoup and pandas and lxml parser using
# python3 -m pip install -U selenium
# python3 -m pip install beautifulsoup4
# pip install pandas
# pip install lxml
# pip install regex

# make sure you have the right version chrome driver in the /venv/bin

from selenium import webdriver
from bs4 import BeautifulSoup
# regex
import re
from regex import regex
import pandas as pd
# allows python to use operating system dependent functions
import os

# wait for the page to load
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# allow date times to be converted
from datetime import datetime

# import sys for exceptions
import sys

# only works up to year 2010 or something like that

# launch url
url = "https://www.moodys.com/researchandratings/market-segment/u-s-public-finance/-/005003/0420B6?tb=0&po=1500&type=Rating_Action_rc"

# create a new Chrome session called driver
driver = webdriver.Chrome()
# waits for up to 30 seconds for an element before throwing an exception
driver.implicitly_wait(30)
# navigates to the link and waits until page is fully loaded
driver.get(url)

# Selenium hands the page source to BeautifulSoup
soup = BeautifulSoup(driver.page_source, "lxml")

# create an empty list
dataList = []

# create a counter for the end of link
x = 0

# compiles a regex expression object to match the name of the id
# . corresponds to any letter, * corresponds to any number of preceding letter
# could also use ^ at the front, which searches for anything that starts with the exp
# use https://medium.com/factory-mind/regex-tutorial-a-simple-cheatsheet-by-examples-649dc1c3f285
hrefName = re.compile("/research/Moodys.*")

# ensures that the research-module element (js table) fully loads
delay = 3
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'research-module')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

# gets the list of all the matching links in the page
linkList = soup.find_all("a", href=hrefName)

# different elements
rating_action = ""
rating_issuer = ""
rating_issuer_link = ""
rating_date = ""
rating_text = ""
rating_lead_analyst = ""
rating_lead_analyst_role = ""
rating_lead_analyst_group = ""
rating_additional_analyst = ""
rating_additional_analyst_role = ""
rating_additional_analyst_group = ""


ANALYST_LEADING_SEARCH = re.compile("(?<=each credit rating.\n\n\n)[^\n]*(?=\n)")
ANALYST_ADDITIONAL_SEARCH = re.compile("(?<=(553 1653|553-1653)\n\n\n)[^\n]*(?=\n)")


# iterate through links that match the link format
for link in linkList:
    driver.get("https://www.moodys.com" + link.get("href"))

    # Selenium hands of the source of the specific job page to a new Beautiful Soup object
    soup_level2 = BeautifulSoup(driver.page_source, "lxml")

    # identify and store rating action as a BeautifulSoup tag
    rating_action_tag = soup_level2.find("span", "mdcPageTitle")
    # stores the string inside the tag as rating_action
    rating_action = str(rating_action_tag.string)
    print(rating_action)

    # identify and store rating issuer via related issuers table
    rating_issuer_tag = soup_level2.find("span", "mdcRefEntityTitle")
    # gets only the human readable text ie the rating issuer
    rating_issuer = rating_issuer_tag.get_text().strip()
    print(rating_issuer)

    # identify and store href of the rating issuer
    rating_issuer_link = "https://www.moodys.com" + rating_issuer_tag.a.get("href")
    print(rating_issuer_link)

    # identify and store the rating date as a tag
    rating_date_tag = soup_level2.find("div", "mdcBodyHeader")
    # stores the string inside the tag as rating_date
    rating_date_string = str(rating_date_tag.string.strip())
    print(rating_date_string)
    rating_date = datetime.strptime(rating_date_string, '%d %b %Y')
    print(rating_date)

    # get tag for all the main content
    rating_text_tag = soup_level2.find("div", "mdcNoIframe")

    # stores the string inside the tag as rating_text
    rating_text = rating_text_tag.get_text()
    print(rating_text)

    # search for rating lead analyst
    # base the search on following the
    # "each credit rating." text
    rating_lead_analyst = re.search(ANALYST_LEADING_SEARCH, rating_text).group()
    print(rating_lead_analyst)

    # get tag for rating lead analyst role
    analyst_role_search = re.compile("(?<=" + rating_lead_analyst + "\n)[^\n]*(?=\n)")
    rating_lead_analyst_role = re.search(analyst_role_search, rating_text).group()
    print(rating_lead_analyst_role)

    # get tag for rating lead analyst group
    analyst_group_search = re.compile("(?<=" + rating_lead_analyst_role + "\n)[^\n]*(?=\n)")
    rating_lead_analyst_group = re.search(analyst_group_search, rating_text).group()
    print(rating_lead_analyst_group)

    # get tag for rating additional analyst
    # additional_analyst_search = regex.compile("(?<=" + rating_lead_analyst_group + "(.*\n)*\n\n)(\w| )*(?=\n)")
    additional_analyst_search = re.search(ANALYST_ADDITIONAL_SEARCH, rating_text).group()
    rating_additional_analyst = regex.search(additional_analyst_search, rating_text.strip()).group()
    print(rating_additional_analyst)

    # get tag for rating additional analyst role
    additional_analyst_role_search = re.compile("(?<=" + rating_additional_analyst + "\n)[^\n]*(?=\n)")
    rating_additional_analyst_role = re.search(additional_analyst_role_search, rating_text).group()
    print(rating_additional_analyst_role)

    # get tag for rating additional analyst group
    additional_analyst_group_search = re.compile("(?<=" + rating_additional_analyst_role + "\n)[^\n]*(?=\n)")
    rating_additional_analyst_group = re.search(additional_analyst_group_search, rating_text).group()
    print(rating_additional_analyst_group)



    # identify and store
    # identify first analyst by the "please see the ratings tab... credit rating." line
    # identify further analysts via breaks
    # allow for these to be empty if unidentified

    # append a row to the dataframe with all the elements

    # Beautiful Soup grabs the 1st HTML table on the page
    # table = soup_level2.find_all('table')[0]
    table = soup_level2.find("table")

    # Giving the HTML table to pandas to put into a dataframe object
    # uses the 0th row to make columns header... probably will need to look into this more in the future
    df = pd.read_html(str(table), header=0)

    # Store the first the dataframe in the previously created dataList
    dataList.append(df[0])

    # Ask Selenium to click the back button
    driver.execute_script("window.history.go(-1)")

    # increment the counter variable before starting the loop over
    x += 1

# add a try and catch it if it breaks and still store the dataframe

# end the Selenium browser session
driver.quit()

# combine all pandas dataframes in the list into one big dataframe
result = pd.concat(dataList, ignore_index=True)
# the guide uses the following but I don't think it's necessary to re-convert the dataframe to a panda
# result = pd.concat([pd.DataFrame(dataList[i]) for i in range(len(dataList))], ignore_index=True)

# convert pandas into a JSON
# orient records is the format of the json string, has no indexes
json_records = result.to_json(orient="records")

# convert pandas into a CSV
csv_records = result.to_csv()

# writing files
# get current working directory
path = os.getcwd()

# open, write, and close the file
f = open(path + "\\fhsu_payroll_data.json", "w")
f.write(json_records)
f.close()

f = open(path + "\\fhsu_payroll_data.csv", "w")
f.write(csv_records)
f.close()
