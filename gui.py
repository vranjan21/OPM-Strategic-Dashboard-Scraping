import scrape_story_link
import scrape_four_by_fours
import get_api_and_scrape


# define the GUI function
def gui():
    print('GUI')


# define the reference other functions
if __name__ == '__main__':
    print('A for Scraping the Story Links')
    print('B for Scraping Four by Fours')
    print('C for Outputting the API and Scrape')
    selection = input('Enter Selection: ')
    if selection == 'A':
        scrape_story_link.scrape_story_link()
    if selection == 'B':
        scrape_four_by_fours.scrape_four_by_fours()
    if selection == 'C':
        get_api_and_scrape.get_api_and_scrape()
    else:
        print('Enter a valid input')
    gui()
