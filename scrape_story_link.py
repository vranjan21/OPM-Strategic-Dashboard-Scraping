# make sure you have the right version chrome driver in the /venv/bin

# imports the web driver manager to get the matching chrome web driver
from webdriver_manager.chrome import ChromeDriverManager

# imports Selenium and webdriver to run the chrome window
from selenium import webdriver

# imports BeautifulSoup to parse the webpage xml
from bs4 import BeautifulSoup

# imports regex for easy parsing of matching a URL format
import re

# imports the selenium libraries to help wait for the page to load
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# imports the time library
import time

# imports csv file
import csv

import lxml


def scrape_story_link(save_folder_location):
    # launch url
    url = "https://data.austintexas.gov/stories/s/59fp-raw5"

    # create a new Chrome session called driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver = webdriver.Chrome()

    # waits for up to 30 seconds for an element before throwing an exception
    driver.implicitly_wait(15)
    # navigates to the link and waits until page is fully loaded
    # driver.get(url)

    # Selenium hands the page source to BeautifulSoup
    # soup = BeautifulSoup(driver.page_source, "lxml")

    # create an empty list
    dataList = []

    # create a counter for the end of link
    x = 0

    # compiles a regex expression object to match the name of the story
    # . corresponds to any letter, * corresponds to any number of preceding letter
    # could also use ^ at the front, which searches for anything that starts with the exp
    # use https://medium.com/factory-mind/regex-tutorial-a-simple-cheatsheet-by-examples-649dc1c3f285
    hrefName = re.compile("https://data.austintexas.gov/stories/s/.*")
    notFindStoryList = re.compile(".*59fp-raw5.*")

    # to-do populate the link list using the above components

    uniqueList = []

    # different elements
    story_link = ""

    # populate link with list of outcome category pages on the dashboard
    # to-do: automate this instead of manually collecting links
    linkList = ["https://data.austintexas.gov/stories/s/Culture/u722-ernc/",
                "https://data.austintexas.gov/stories/s/Economic-Opportunity/8t6b-vguj",
                "https://data.austintexas.gov/stories/s/Government-That-Works-for-All-Dashboard/u7qm-zkuf/",
                "https://data.austintexas.gov/stories/s/Health/iane-nkjw/",
                "https://data.austintexas.gov/stories/s/Mobility-Dashboard/gzb5-ykym/",
                "https://data.austintexas.gov/stories/s/Safety-Dashboard/35fg-g2fw"]
    story_link_list = []
    # iterate through links that match the link format
    for link in linkList:

        # Selenium navigates navigates to the outcome link
        driver.get(link)

        # ensures that the measure-result-big-number fully loads
        # waits an additional 15 seconds for the rest of the elements
        # this is an arbitrary number depending on the browser's processing speed
        # can be faster or slower. should we make this variable? ex. deep search?
        try:
            WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,
                                                                                         "measure-result-big-number")))
            time.sleep(18)
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")

        # Selenium hands of the source of the specific job page to a new Beautiful Soup object
        soup_level2 = BeautifulSoup(driver.page_source, "lxml")

        # identify and store story link as a BeautifulSoup tag
        story_link_tag = soup_level2.find_all("div", class_="view-measure-link")
        print(story_link_tag)

        # stores the string inside the tag as story_link
        for story_link in story_link_tag:
            # for this mess - the re.findall looks for the url part of the
            # html via a regex expression (a pre-built expression that looks
            # for text that fits a certain format, in this case a URL format)
            urls = re.findall(
                '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]['
                'a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,'
                '}|www\.[a-zA-Z0-9]+\.[^\s]{2,})',
                str(story_link))

            # The urls[0][:-1] first gets the very first index of the list
            # of urls that are in the urls list. should only be 1/1 (position 0)
            # then it removes the very last character off
            # the regex expression since the above expression has a typo in the
            # regex that leaves on a quotation mark at the end of the link
            # to-do: combine this with the regex expression
            story_link_text = urls[0][:-1]
            print(story_link_text)

            # adds the url to the list of story links
            story_link_list.append(story_link_text)

        # Ask Selenium to click the back button
        driver.execute_script("window.history.go(-1)")

        # increment the counter variable before starting the loop over
        x += 1

    with open(save_folder_location + '/story_link_list.csv', 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for link in story_link_list:
            wr.writerow([link])

    # end the Selenium browser session and closes the browser window
    driver.quit()


# if the file is executed by itself
if __name__ == '__main__':
    from PyQt5 import QtCore, QtGui, QtWidgets
    import sys
    app = QtWidgets.QApplication(sys.argv)
    open_file = QtWidgets.QFileDialog.getExistingDirectory()
    print(open_file)
    # scrape_story_link.py executed as script
    # run the above function
    print('Copy and Paste the above path for the following dialog: ')
    save_folder_location = input('Enter Save Folder Location: ')
    scrape_story_link(save_folder_location)
    sys.exit(app.exec_())
