# make sure you have the right version chrome driver in the /venv/bin

# imports Selenium and webdriver to run the chrome window
from selenium import webdriver

# imports BeautifulSoup to parse the webpage xml
from bs4 import BeautifulSoup

# imports the selenium libraries to help wait for the page to load
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# imports the time library
import time

# imports csv file
import csv

# create a new chrome session called driver
driver = webdriver.Chrome()

# set driver to wait for up to 30 seconds for an element before throwing an exception
driver.implicitly_wait(30)


url_list = []
# open file in read mode
with open('story_link_list.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = csv.reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # row variable is a list that represents a row in csv
        for link in row:
            url_list.append(link)

# create a blank list to store measure links
measure_link_list = []

# create a blank list to store measure 4x4s
four_by_list = []

# gets all unique URLs in the list as a set
# this eliminates duplicate URLs
url_set = set(url_list)

# iterates through url list
for url in url_set:
    # navigates to the story URL page
    driver.get(url)

    # wait until calculated measure result number is fully loaded
    # then delays 200 milliseconds just in case there are additional elements
    try:
        WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,
                                                                                     "measure-result-big-number")))
        time.sleep(0.2)
    # if it times out after 30 seconds, then it breaks out and continues forward
    except TimeoutException:
        print("link not found ... breaking out")
        print()

    # Selenium hands the page source to BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "lxml")

    # gets a set of all the unique measure links in the story page
    # usually only one will be in the set
    # except there's weird story pages like https://data.austintexas.gov/stories/s/uwxu-e5zh
    measure_link_set = set(soup.find_all(class_="view-measure-link"))

    # iterates through the measure links in the measure link set
    # usually only one iteration
    for measure_link in measure_link_set:
        # finds the very first match of a URL
        measure_link_raw = measure_link.find('a', href=True)
        measure_link_text = measure_link_raw['href']
        print(measure_link_text)
        measure_link_list.append(measure_link_text)
        four_by_four_text = measure_link_text[-9:]
        print(four_by_four_text)
        four_by_list.append(four_by_four_text)

# write the csv files
with open('measures_link_list.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for link in measure_link_list:
        wr.writerow([link])
    print("measures_link_list.csv is written to the project directory")

with open('measures_four_by_four_list.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for link in four_by_list:
        wr.writerow([link])
    print("measures_four_by_four_list.csv is written to the project directory")

# end the Selenium browser session and closes the browser window
driver.quit()
