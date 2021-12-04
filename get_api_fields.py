# API calls only
# no scraping so far
# to-do: implement try excepts that preserves the index with a blank entry
# for any additional elements

# imports csv
import csv

# import url
import urllib.request

# import json
import json

# import regex
import re

# import date time package
from datetime import datetime

# create a blank list to store the four by fours
four_by_four_list = []

# create a blank list to store the story page links
measure_story_link_list = []

# open the list of measure 4x4s in read mode
with open('measures_four_by_four_list.csv', 'r') as read_obj:
    # pass the file object to csv.reader() to get the reader object
    csv_reader = csv.reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        # append the first item in the row at index 0 which is the 4x4 to the four_by_four_list
        four_by_four_list.append(row[0])
        # append the second item in the row at index 1 which is the story link to the measure_story_link_list
        measure_story_link_list.append(row[1])

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


# compiles the regex expression to search for
MEASURE_ID_SEARCH = re.compile("^.*?(?=(_|-| ))")

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

    # measure_story_link_text = str(measure_meta_two['metadata'])


    # regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>\\]+|\(([^\s()<>\\]+|(\([^\s()<>\\]+\)))*\))+(?:\(([^\s()<>\\]+|(\([^\s()<>\\]+\)))*\)|[^\s`!()\[\]{};:'\".,<>\\?«»“”‘’]))"

    # measure_story_link_search = re.findall(regex, measure_story_link_text)
    # measure_story_link = [x[0] for x in measure_story_link_search][0]

    # print(measure_story_link)

    # append the measure ID to the list of measure IDs
    measure_id_list.append(measure_id)
    # append the name of the measure to the list of measure names
    measure_name_list.append(measure_name)
    # append the target value to the list of targets
    measure_target_value_list.append(measure_target_value)
    # append the timestamp to the list of timestamps
    measure_data_last_timestamp_list.append(measure_data_last_timestamp)

    # commented and to-be-deleted because we will be getting the measure story links in the initial process
    # append the measure story link to the list of measure story links
    # measure_story_link_list.append(measure_story_link)

# write the csv files
# note: to get apostrophes to display properly in excel have to encode as utf-8
with open('api_fields.csv', 'w', encoding='utf-8-sig') as myfile:

    # feeds the field names in through a Python Dictionary
    # also has a quote_all argument - formats everything in the csv with quotes debatable whether to keep this or not
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

    # write each of the field columns  to csv
    index = 0
    list_length = len(four_by_four_list)

    wr.writerow(['4x4 (testing only)', 'Measure Link (testing only)', 'Measure ID', 'Measure Name', 'Reporting Frequency', 'Most Recent Reporting Year',
                 'Measure Status Color', 'Measure Value', 'Target Value', 'Metadata Update Date',
                 'Link to Story'])
    while index < list_length:
        wr.writerow([four_by_four_list[index], measure_link_list[index], measure_id_list[index], measure_name_list[index], '', '',
                     '', '', measure_target_value_list[index], measure_data_last_timestamp_list[index],
                     measure_story_link_list[index]])
        index = index + 1

