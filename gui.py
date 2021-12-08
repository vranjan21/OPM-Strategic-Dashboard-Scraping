import scrape_story_link_and_four_by_fours
import get_api_and_scrape
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


# define the GUI function
def gui():
    print('GUI')


# define the reference other functions
if __name__ == '__main__':
    while 0 < 1:
        print('A for Scraping the List of Measures')
        print('B for Outputting the API and Scrape')
        print('X to exit')
        selection = input('Enter Selection: ')
        if selection == 'A':
            app = QtWidgets.QApplication(sys.argv)
            print('Select where you want the measure_4x4_and_story_link_list.csv to be written:')
            open_file = QtWidgets.QFileDialog.getExistingDirectory()
            print(str(open_file))
            # scrape_story_link.py executed as script
            # run the above function
            # print('Copy and Paste the above path for the following dialog: ')
            # save_folder_location = input('Enter Save Folder Location: ')
            save_folder_location = str(open_file)
            scrape_story_link_and_four_by_fours.scrape_story_link_and_four_by_fours(save_folder_location)
        if selection == 'B':
            app = QtWidgets.QApplication(sys.argv)
            print('Select your measure_4x4_and_story_link_list.csv file:')
            open_file = QtWidgets.QFileDialog.getOpenFileName()
            print(open_file[0])
            # print('Copy and Paste the above path for the following dialog: ')
            # open_file_location = input('Enter measure_4x4_and_story_link_list.csv location: ')
            open_file_location = open_file[0]
            # get the save directory
            print('Select the folder to save get_api_and_scrape.csv to: ')
            open_file = QtWidgets.QFileDialog.getExistingDirectory()
            print(open_file)
            # run the above function
            # print('Copy and Paste the above path for the following dialog: ')
            # save_folder_location = input('Enter Save Folder Location: ')
            save_folder_location = str(open_file)
            get_api_and_scrape.get_api_and_scrape(open_file_location, save_folder_location)
        if selection == 'X':
            sys.exit()
        else:
            print('Enter a valid input')

        # idk why we're executing gui() lol
        gui()

# to-do: pyqt stuff