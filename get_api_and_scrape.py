# make sure you install selenium and BeautifulSoup and pandas and lxml parser using
# python3 -m pip install -U selenium
# python3 -m pip install beautifulsoup4
# pip install pandas
# pip install lxml

# api field imports
# imports csv
import csv

# import url
import urllib.request

# import json
import json

# import regex
import re

# import date-time package
from datetime import datetime

# scrape field imports
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

from selenium.webdriver.support.ui import WebDriverWait  # wait for the page to load
from selenium.webdriver.support import expected_conditions  # wait for the page to load

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import traceback

import lxml

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# opens the measures_four_by_four_list.csv file
def get_api_and_scrape(open_file_location, save_folder_location):

    # create a blank list to store the four by fours
    four_by_four_list = []

    # create a blank list to store the story page links
    measure_story_link_list = []

    # create a new chrome session called driver
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # set driver to wait for up to 30 seconds for an element before throwing an exception
    driver.implicitly_wait(30)

    # open the list of measure 4x4s in read mode
    with open(open_file_location, 'r') as read_obj:
        # pass the file object to csv.reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            # append the first item in the row at index 0 which is the 4x4 to the four_by_four_list
            four_by_four_list.append(row[0])
            # append the second item in the row at index 1 which is the story link to the measure_story_link_list
            measure_story_link_list.append(row[1])

    # API Fields
    # testing only - create a blank list to store measure links
    measure_link_list = []

    # create a blank list to store measure IDs
    measure_id_list = []

    # create a blank list to store measure names
    measure_name_list = []

    # create a blank list to store measure target values
    measure_target_value_list = []

    # create a blank list to store measure timestamps
    measure_data_last_timestamp_list = []

    # Scrape Fields
    measure_value_list = []

    measure_status_list = []

    recent_reporting_year_list = []

    reporting_frequency_list = []

    page_update_date_list = []

    # compiles the regex expression to search for the measure ID
    MEASURE_ID_SEARCH = re.compile("^.*?(?=(_|-| ))")

    # compiles the regex expression to search for frequency measures and page update dates
    FREQUENCY_MEASURE_SEARCH = re.compile("(?<=Reported:.)[^\n]*(?=Date)")
    FREQUENCY_MEASURE_NO_UPDATE_SEARCH = re.compile("(?<=Reported:.)[^\n]*(?=Present)")
    PAGE_UPDATE_DATE_SEARCH = re.compile("(?<=last updated:.)[^\n]*(?=Present)")

    # main loop index value
    index = 0

    # length of the list of measures to iterate
    list_length = len(four_by_four_list)

    # write the csv files
    # note: to get apostrophes to display properly in excel have to encode as utf-8
    # have to add a newline = '' because of Windows compatibility issues
    filename = save_folder_location + '/get_api_and_scrape_log_' + datetime.now().strftime("%Y%m%d-%H%M%S") + '.csv'
    with open(filename, 'w', newline='', encoding='utf-8-sig') as myfile:

        # feeds the field names in through a Python Dictionary
        # also has a quote_all argument - formats everything in the csv with quotes debatable whether to keep this or not
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

        wr.writerow([
            '4x4 (testing only)',
            'Link to Measure',
            'Link to Story',
            'Measure ID',
            'Measure Name',
            'Measure Value',
            'Target Value',
            'Measure Status',
            'Most Recent Reporting Year',
            'Reporting Frequency',
            'Page Update Date',
            'Metadata Update Date'
        ])

        # iterates through url list
        while index < list_length:
            try:
                # set the four by four that will be evaluated
                four_by_four = four_by_four_list[index]
                print('Scraping ' + str(index + 1) + ' of ' + str(list_length) + ' measures')
                print('Four by Four:')
                print(four_by_four)
                # constructs the json URL for the two API calls
                measure_meta_one_url = "https://data.austintexas.gov/api/views/metadata/v1/" + four_by_four
                measure_meta_two_url = "https://data.austintexas.gov/api/measures_v1/" + four_by_four

                # get the raw JSON object from the first metadata url
                measure_meta_one = json.load(urllib.request.urlopen(measure_meta_one_url))

                # get the raw JSON object from the second metadata url
                measure_meta_two = json.load(urllib.request.urlopen(measure_meta_two_url))

                # get the measure name
                measure_name_full = measure_meta_one['name']
                print('Full Measure Name:')
                print(measure_name_full)

                # search for the measure name using the compiled regex search
                measure_id = re.search(MEASURE_ID_SEARCH, measure_name_full).group(0)

                # compile a regex expression to get the rest of the name
                measure_name_search = re.compile("(?<=" + measure_id + ").*")

                measure_name = re.search(measure_name_search, measure_name_full).group(0)[1:]
                print('Measure ID:')
                print(measure_id)
                print('Measure Name:')
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
                print('Measure Target Value:')
                print(measure_target_value)

                # get the date the measure was last updated
                last_timestamp_string = measure_meta_one['metadataUpdatedAt']
                last_timestamp_datetime = datetime.strptime(last_timestamp_string, '%Y-%m-%dT%H:%M:%S+0000')
                measure_data_last_timestamp = last_timestamp_datetime.strftime("%m/%d/%Y")

                print('Metadata Updated:')
                print(measure_data_last_timestamp)

                # internal testing only - adds the link of the measure to a list for the output
                measure_link = 'https://data.austintexas.gov/d/' + four_by_four
                measure_link_list.append(measure_link)

                # append the measure ID to the list of measure IDs
                measure_id_list.append(measure_id)
                # append the name of the measure to the list of measure names
                measure_name_list.append(measure_name)
                # append the target value to the list of targets
                measure_target_value_list.append(measure_target_value)
                # append the timestamp to the list of timestamps
                measure_data_last_timestamp_list.append(measure_data_last_timestamp)

                scrape_url = measure_link_list[index]

                # navigate Selenium chrome driver to the measure page URL and waits until page is fully loaded
                driver.get(scrape_url)

                # wait until calculated measure result number is fully loaded
                try:
                    WebDriverWait(driver, 30).until(
                        expected_conditions.visibility_of_element_located((By.CLASS_NAME, "measure-result-big-number")))
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
                print('Measure Value:')
                print(measure_value)

                # appends the measure value to the list
                measure_value_list.append(measure_value)

                # locates and stores the measure status (ex. On Track, Off Track, etc)
                try:
                    measure_status = soup.find(class_="status-banner-text").text
                except AttributeError:
                    # if this value doesn't exist, print that it Does not exist
                    measure_status = "Does not exist"

                print('Measure Status:')
                print(measure_status)

                # appends the measure status to the list
                measure_status_list.append(measure_status)

                # locates and stores the reporting year range
                # this is in the format of 1/1/20 - 12/31/20
                try:
                    recent_reporting_year_range = soup.find(class_="reporting-period-latest").text

                except AttributeError:
                    # if this value doesn't exist, print that it Does not exist
                    recent_reporting_year_range = "Does not exist"

                print('Recent Reporting Year Range:')
                print(recent_reporting_year_range)
                # recent_reporting_year_list.append(recent_reporting_year)

                recent_reporting_year_list.append(recent_reporting_year_range)
                # TO-DO: Scrape Reporting Frequency
                # TO-DO: Scrape Page Update Date

                # STORY PAGE:
                # scraping the story page values
                # we do this separately because there are some stories that have multiple measures
                # gets the next story page link
                scrape_url = measure_story_link_list[index]

                # if the link isn't a full URL
                if not scrape_url.startswith('http'):
                    scrape_url = 'https://' + scrape_url

                # navigate Selenium chrome driver to the measure page URL and waits until page is fully loaded
                driver.get(scrape_url)

                # wait until calculated measure result number is fully loaded
                try:
                    WebDriverWait(driver, 30).until(
                        expected_conditions.visibility_of_element_located((By.CLASS_NAME, "measure-result-big-number")))
                except TimeoutException:
                    print("link not found ... breaking out")
                    print()

                # Selenium hands the page source to BeautifulSoup
                soup = BeautifulSoup(driver.page_source, "lxml")

                # gets all the text of the story page as a single string
                story_text = soup.find(id="content").get_text().replace('\n', '')
                print('Story Text:')
                # print(story_text)

                if FREQUENCY_MEASURE_SEARCH.search(story_text):
                    # searches for and stores the reporting frequency in the story text
                    reporting_frequency = re.search(FREQUENCY_MEASURE_SEARCH, story_text).group()
                elif FREQUENCY_MEASURE_NO_UPDATE_SEARCH.search(story_text):
                    reporting_frequency = re.search(FREQUENCY_MEASURE_NO_UPDATE_SEARCH, story_text).group()
                else:
                    reporting_frequency = "Does not exist"
                print('Reporting Frequency:')
                print(reporting_frequency)

                # appends the reporting frequency to the list of all reporting frequencies
                reporting_frequency_list.append(reporting_frequency)

                # searches for the page update date
                if PAGE_UPDATE_DATE_SEARCH.search(story_text):
                    page_update_date = re.search(PAGE_UPDATE_DATE_SEARCH, story_text).group()
                else:
                    page_update_date = "Does not exist"
                print('Page Update Date:')
                print(page_update_date)

                # appends the page update date to the list of all page updates
                page_update_date_list.append(page_update_date)

                # writes the records that were just collected
                wr.writerow([
                    four_by_four_list[index],
                    measure_link_list[index],
                    measure_story_link_list[index],
                    measure_id_list[index],
                    measure_name_list[index],
                    measure_value_list[index],
                    measure_target_value_list[index],
                    measure_status_list[index],
                    recent_reporting_year_list[index],
                    reporting_frequency_list[index],
                    page_update_date_list[index],
                    measure_data_last_timestamp_list[index]
                ])

            # push
            # catches any exception that is generated
            except Exception as e:
                # writes the records that were just collected
                wr.writerow([
                    four_by_four_list[index],
                    "Error: " + traceback.format_exc()
                ])

            myfile.flush()
            index = index + 1

    # write the csv files
    # note: to get apostrophes to display properly in excel have to encode as utf-8
    with open(save_folder_location + '/get_api_and_scrape.csv', 'w', encoding='utf-8-sig') as myfile:

        # feeds the field names in through a Python Dictionary
        # also has a quote_all argument
        # this formats everything in the csv with quotes debatable whether to keep this or not
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

        # write each of the field columns  to csv
        index = 0
        list_length = len(four_by_four_list)

        wr.writerow([
            '4x4 (testing only)',
            'Link to Measure',
            'Link to Story',
            'Measure ID',
            'Measure Name',
            'Measure Value',
            'Target Value',
            'Measure Status',
            'Most Recent Reporting Year',
            'Reporting Frequency',
            'Page Update Date',
            'Metadata Update Date'
        ])
        while index < list_length:
            wr.writerow([
                four_by_four_list[index],
                measure_link_list[index],
                measure_story_link_list[index],
                measure_id_list[index],
                measure_name_list[index],
                measure_value_list[index],
                measure_target_value_list[index],
                measure_status_list[index],
                recent_reporting_year_list[index],
                reporting_frequency_list[index],
                page_update_date_list[index],
                measure_data_last_timestamp_list[index]
            ])
            index = index + 1

    driver.quit()


if __name__ == '__main__':
    from PyQt5 import QtCore, QtGui, QtWidgets
    import sys
    app = QtWidgets.QApplication(sys.argv)
    print('Select your measure_4x4_and_story_link_list.csv file:')
    open_file = QtWidgets.QFileDialog.getOpenFileName()
    print(open_file[0])
    print('Copy and Paste the above path for the following dialog: ')
    open_file_location = input('Enter measure_4x4_and_story_link_list.csv location: ')

    # get the save directory
    print('Select the folder to save get_api_and_scrape.csv to: ')
    open_file = QtWidgets.QFileDialog.getExistingDirectory()
    print(open_file)
    # run the above function
    print('Copy and Paste the above path for the following dialog: ')
    save_folder_location = input('Enter Save Folder Location: ')
    get_api_and_scrape(open_file_location, save_folder_location)

    # keeps the program running
    sys.exit(app.exec_())

