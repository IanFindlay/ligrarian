#!/usr/bin/env python3

"""Automatically updates Books Read spreadsheet and Goodreads."""

import sys
import time
import datetime
from datetime import timedelta
import requests
import openpyxl
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


with open('/home/finners/Documents/Coding/Python/Booktracker/config') as f:
    INFO = f.readlines()
    USERNAME = INFO[0].strip()
    PASSWORD = INFO[1].strip()
    PATH = INFO[2].strip()

# Determine the date (DD/MM/YY) to write as book finished
def get_date():
    """Return the date the book was read formatted (DD/MM/YY)."""
    today = datetime.datetime.now()

    date_day = today.day
    if len(str(date_day)) == 1:
        date_day = '0' + str(date_day)
    date_month = today.month
    if len(str(date_month)) == 1:
        date_month = '0' + str(date_month)

    date_year = str(today.year)[-2:]

    if len(sys.argv) == 4:
        date = '{}/{}/{}'.format(date_day, date_month, date_year)

    else:
        date_read = sys.argv[4]

        if date_read == 'y':
            if date_day != 1:
                date = '{}/{}/{}'.format('0' + str(int(date_day) - 1),
                                         date_month, date_year)
            else:
                yesterday = datetime.datetime.now() - timedelta(days=1)

                date_day = yesterday.day
                date_month = yesterday.month
                if len(str(date_month)) == 1:
                    date_month = '0' + str(date_month)
                date_year = str(yesterday.year)[-2:]

                date = '{}/{}/{}'.format(date_day, date_month, date_year)

        elif date_read == 'c':
            date = input('Enter the date the book was finished: ')

    return date

DATE_READ = get_date()

MONTH_CONV = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May',
              '06': 'June', '07': 'July', '08': 'Aug', '09': 'Sep', '10': 'Oct',
               '11': 'Nov', '12': 'Dec'}

# Selenium starts
print('Updating Goodreads...')
browser = webdriver.Firefox()
browser.get('https://goodreads.com')

# Login
email_elem = browser.find_element_by_name('user[email]')
email_elem.send_keys(USERNAME)
pass_elem = browser.find_element_by_name('user[password]')
pass_elem.send_keys(PASSWORD)
pass_elem.send_keys(Keys.ENTER)
time.sleep(5)

# Find correct book and edition
SEARCH_TERMS = sys.argv[1]
SEARCH_LIST = SEARCH_TERMS.split()       # UNUSED???
search_elem = browser.find_element_by_class_name('searchBox__input')
search_elem.send_keys(SEARCH_TERMS + '%3Dauthor')
search_elem.send_keys(Keys.ENTER)
time.sleep(3)

title_elem = browser.find_element_by_class_name('bookTitle')
title_elem.click()
time.sleep(3)

editions_elem = browser.find_element_by_class_name('otherEditionsLink')
editions_elem.click()

# Format
FORMAT = sys.argv[2]
filter_elem = browser.find_element_by_name('filter_by_format')
filter_elem.click()
filter_elem.send_keys(FORMAT)
filter_elem.send_keys(Keys.ENTER)
time.sleep(3)

book_elem = browser.find_element_by_class_name('bookTitle')
book_elem.click()

# Mark as Read
menu_elem = browser.find_element_by_class_name('wtrRight.wtrUp')
menu_elem.click()
time.sleep(1)
menu_elem.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER)
time.sleep(2)

# Give star rating
RATING = sys.argv[3]
stars_elem = browser.find_elements_by_class_name('star.off')
skip = 2
for stars in stars_elem:
    if stars.text.strip() == '{} of 5 stars'.format(RATING):
        skip -= 1
        if skip == 0:
            stars.click()
            break


# Date Selection
year_elem = browser.find_element_by_class_name('endedAtYear.readingSessionDatePicker.smallPicker')
year_elem.click()
time.sleep(1)
year_elem.send_keys('2', Keys.ENTER)

month_elem = browser.find_element_by_class_name('endedAtMonth.largePicker.readingSessionDatePicker')
month_elem.click()
month_elem.send_keys(MONTH_CONV[DATE_READ[3:5]], Keys.ENTER)

day_elem = browser.find_element_by_class_name('endedAtDay.readingSessionDatePicker.smallPicker')
day_elem.click()
day_elem.send_keys(str(DATE_READ[0:2]), Keys.ENTER)

# Save review
save_elem = browser.find_element_by_name('next')
save_elem.click()

# Shelf selection
shelves_elems = browser.find_elements_by_class_name('actionLinkLite.bookPageGenreLink')
shelves = []
for shelf in shelves_elems:
    if ' users' not in shelf.text and shelf.text not in shelves:
        shelves.append(shelf.text)

menu_elem = browser.find_element_by_class_name('wtrRight.wtrDown')
menu_elem.click()
time.sleep(1)
shelf_search_elem = browser.find_element_by_class_name('wtrShelfSearchField')

for i, item in enumerate(shelves):
    shelf_search_elem.send_keys(shelves[i], Keys.ENTER)
    shelf_search_elem.send_keys(Keys.SHIFT, Keys.HOME, Keys.DELETE)

print('Goodreads updated.')

# BS4 Parsing
URL = browser.current_url
RES = requests.get(URL)
RES.raise_for_status()
SOUP = bs4.BeautifulSoup(RES.text, 'html.parser')

TITLE_ELEM = SOUP.select('#bookTitle')

SERIES_ELEM = SOUP.select('#bookTitle > .greyText')
if SERIES_ELEM != []:
    SERIES = SERIES_ELEM[0].getText().strip()
    BOOK_TITLE = TITLE_ELEM[0].getText().strip().strip(SERIES).strip()
    TITLE = BOOK_TITLE + ' ' + SERIES
else:
    TITLE = TITLE_ELEM[0].getText().strip()

print(TITLE)

AUTHOR_ELEM = SOUP.select('.authorName')
AUTHOR = AUTHOR_ELEM[0].getText().strip()

PAGES_ELEM = SOUP.select('#details .row')
PAGES = PAGES_ELEM[0].getText().split(',')[1].strip(' pages')

TAG_ELEM = SOUP.select('.actionLinkLite.bookPageGenreLink')

if TAG_ELEM[0].getText() == 'Fiction' or TAG_ELEM[0].getText() == 'Nonfiction':
    TYPE = TAG_ELEM[0].getText().strip()
    GENRE = TAG_ELEM[2].getText().strip()

else:
    GENRE = TAG_ELEM[0].getText().strip()

    for i in range(0, len(TAG_ELEM) + 1):
        if TAG_ELEM[i].getText() == 'Fiction' or TAG_ELEM[i].getText() == 'Nonfiction':
            TYPE = TAG_ELEM[i].getText()
            break

WB = openpyxl.load_workbook(PATH)
print('Updating Spreadsheet...')

# Write information into sheets
def input_info(sheet_name):
    """Write the book information to the first blank row on the given sheet."""
    sheet = WB.get_sheet_by_name(sheet_name)
    input_row = 1
    data = ''
    while data != None:
        data = sheet.cell(row=input_row, column=1).value
        input_row += 1

    input_row -= 1

    sheet.cell(row=input_row, column=1).value = TITLE
    sheet.cell(row=input_row, column=2).value = AUTHOR
    sheet.cell(row=input_row, column=3).value = int(PAGES)
    sheet.cell(row=input_row, column=4).value = TYPE
    sheet.cell(row=input_row, column=5).value = GENRE
    sheet.cell(row=input_row, column=6).value = DATE_READ


input_info('20' + DATE_READ[-2:])
input_info('Overall')

WB.save(PATH)

print('Spreadsheet has been updated.')

# TODO Organise code into seperate functions
# TODO Rewrite BS4 TAG system as Type and Genre can be found from the list 'Shelves'
# TODO Rewrite title / series using seperaet getText's
# TODO Make constants and variables naming uniform and PEP8 compliant
