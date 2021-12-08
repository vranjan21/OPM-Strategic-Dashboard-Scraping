import scrape_story_link_and_four_by_fours
import get_api_and_scrape
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


# define the GUI function
def gui():
    print('OPM Strategic Performance Dashboard Scraper')


# define the reference other functions
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    gui()
    while 0 < 1:
        print('A for Scraping the List of Measures')
        print('B for Outputting the API and Scrape')
        print('X to exit')
        selection = input('Enter Selection: ')
        folder_flag = 'invalid'
        file_flag = 'invalid'

        if selection == 'A':
            while folder_flag == 'invalid':
                print('Select where you want the measure_4x4_and_story_link_list.csv to be written:')
                open_folder = QtWidgets.QFileDialog.getExistingDirectory()
                print(str(open_folder))
                if open_folder != '':
                    print('Folder is verified')
                    folder_flag = 'valid'
                else:
                    print('Select a valid folder')
            # scrape_story_link.py executed as script
            # run the above function
            # print('Copy and Paste the above path for the following dialog: ')
            # save_folder_location = input('Enter Save Folder Location: ')
            save_folder_location = str(open_folder)
            scrape_story_link_and_four_by_fours.scrape_story_link_and_four_by_fours(save_folder_location)
        if selection == 'B':
            while file_flag == 'invalid':
                print('Select your measure_4x4_and_story_link_list.csv file:')
                open_file = QtWidgets.QFileDialog.getOpenFileName()
                print(open_file[0])
                if open_file[0].endswith('measure_4x4_and_story_link_list.csv'):
                    print('File name is verified')
                    file_flag = 'valid'
                else:
                    print('Ensure you selected a valid file')
            # print('Copy and Paste the above path for the following dialog: ')
            # open_file_location = input('Enter measure_4x4_and_story_link_list.csv location: ')
            open_file_location = open_file[0]
            # get the save directory
            while folder_flag == 'invalid':
                print('Select the folder to save get_api_and_scrape.csv to: ')
                open_folder = QtWidgets.QFileDialog.getExistingDirectory()
                print(str(open_folder))
                if open_folder != '':
                    print('Folder is verified')
                    folder_flag = 'valid'
                else:
                    print('Select a valid folder')
            # run the above function
            # print('Copy and Paste the above path for the following dialog: ')
            # save_folder_location = input('Enter Save Folder Location: ')
            save_folder_location = str(open_folder)
            get_api_and_scrape.get_api_and_scrape(open_file_location, save_folder_location)
        if selection == 'X':
            sys.exit()
        else:
            print('Enter a valid input')

# to-do: pyqt stuff