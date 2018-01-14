#!/usr/bin/env python3

"""Automatically updates Books Read spreadsheet and Goodreads account."""

import configparser
import sys
import time
import datetime
from datetime import timedelta
import requests
import openpyxl
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


def get_date():
    """Return the date the book was read formatted (DD/MM/YY)."""
    today = datetime.datetime.now()

    if len(sys.argv) == 4:
        date = today.strftime('%d/%m/%y')

    elif sys.argv[4].lower() == 'y':
        yesterday = today - timedelta(days=1)
        date = yesterday.strftime('%d/%m/%y')

    elif sys.argv[4].lower() == 'c':
        date = input('Enter the date the book was finished (DD/MM/YY): ')

    return date


def goodreads_find():
    """Find the correct book, in the correct format, on Goodreads."""
    driver.get('https://goodreads.com')

    # Login
    email_elem = driver.find_element_by_name('user[email]')
    email_elem.send_keys(username)
    pass_elem = driver.find_element_by_name('user[password]')
    pass_elem.send_keys(password)
    pass_elem.send_keys(Keys.ENTER)

    # Find correct book and edition
    search_terms = sys.argv[1]
    search_elem = driver.find_element_by_class_name('searchBox__input')
    search_elem.send_keys(search_terms + '%3Dauthor')
    search_elem.send_keys(Keys.ENTER)

    driver.find_element_by_class_name('bookTitle').click()

    driver.find_element_by_class_name('otherEditionsLink').click()

    # Format
    book_format = sys.argv[2].lower()
    filter_elem = driver.find_element_by_name('filter_by_format')
    filter_elem.click()
    filter_elem.send_keys(book_format)
    filter_elem.send_keys(Keys.ENTER)
    time.sleep(2)

    driver.find_element_by_class_name('bookTitle').click()

    return driver.current_url


MONTH_CONV = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May',
              '06': 'June', '07': 'July', '08': 'Aug', '09': 'Sep', '10': 'Oct',
              '11': 'Nov', '12': 'Dec'}


def goodreads_update():
    """Update Goodreads by marking book as read and adding information."""
    # Mark as Read
    menu_elem = driver.find_element_by_class_name('wtrRight.wtrUp')
    menu_elem.click()
    time.sleep(1)
    menu_elem.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER)

    # Date Selection
    # year_elem = driver.find_element_by_class_name('endedAtYear.readingSession'
    #                                                'DatePicker.smallPicker')
    # year_elem.click()
    # year_elem.send_keys('2', Keys.ENTER)


    # # FIXME Original implementation doesn't work for double digit days and
    # # FIXME the new code is limited to only setting it to today's date
    # day_elem = driver.find_element_by_class_name('endedAtDay.readingSession'
    #                                               'DatePicker.smallPicker')
    # day_elem.click()
    # day_elem.send_keys(str(date_finished[0:2]))
    # time.sleep(1)
    # day_elem.send_keys(Keys.ENTER)


    # month_elem = driver.find_element_by_class_name('endedAtMonth.largePicker'
    #                                                 '.readingSessionDatePicker')
    # month_elem.click()
    # month_elem.send_keys(MONTH_CONV[date_finished[3:5]], Keys.ENTER)

    # Set to today
    today_elem = driver.find_element_by_class_name('endedAtSetTodayLink.gr-button')
    today_elem.click()

    # Save review
    save_elem = driver.find_element_by_name('next')
    save_elem.click()

    # Shelf selection
    shelves_elems = driver.find_elements_by_class_name('actionLinkLite.'
                                                       'bookPageGenreLink')
    shelves = []
    for shelf in shelves_elems:
        if ' users' not in shelf.text and shelf.text not in shelves:
            shelves.append(shelf.text)

    menu_elem = driver.find_element_by_class_name('wtrRight.wtrDown')
    menu_elem.click()
    time.sleep(1)
    shelf_search_elem = driver.find_element_by_class_name('wtrShelfSearchField')

    for i in range(len(shelves)):
        shelf_search_elem.send_keys(shelves[i], Keys.ENTER)
        shelf_search_elem.send_keys(Keys.SHIFT, Keys.HOME, Keys.DELETE)

    menu_elem.click()

    # Give star rating
    rating = sys.argv[3]
    stars_elem = driver.find_elements_by_class_name('star.off')
    for stars in stars_elem:
        if stars.text.strip() == '{} of 5 stars'.format(rating):
            stars.click()
            break

    # TODO Add 5-star-books shelf to shelves if star rating is 5

    return shelves


def parse_page():
    """Parse and return page information needed for updating the spreadsheet."""
    info_list = []
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    title_elem = soup.select('#bookTitle')

    rough_title = title_elem[0].getText().strip().split('\n')
    if len(rough_title) == 1:
        title = rough_title[0].strip()
    else:
        title = rough_title[0].strip() + ' ' + rough_title[2].strip()

    info_list.append(title)

    author_elem = soup.select('.authorName')
    author = author_elem[0].getText().strip()
    info_list.append(author)

    pages_elem = soup.select('#details .row')
    pages = pages_elem[0].getText().split(',')[1].strip(' pages')
    info_list.append(pages)

    if shelves_list[0] == 'Fiction' or shelves_list[0] == 'Nonfiction':
        category = shelves_list[0]
        genre = shelves_list[1]
    else:
        genre = shelves_list[0]
        if 'Fiction' in shelves_list:
            category = 'Fiction'
        else:
            category = 'Nonfiction'

    info_list.append(category)
    info_list.append(genre)

    return info_list


def input_info(sheet_name):
    """Write the book information to the first blank row on the given sheet."""
    sheet = wb.get_sheet_by_name(sheet_name)
    input_row = 1
    data = ''
    while data != None:
        data = sheet.cell(row=input_row, column=1).value
        input_row += 1

    input_row -= 1

    sheet.cell(row=input_row, column=1).value = info[0]        # Title
    sheet.cell(row=input_row, column=2).value = info[1]        # Author
    sheet.cell(row=input_row, column=3).value = int(info[2])   # Pages
    sheet.cell(row=input_row, column=4).value = info[3]        # Category
    sheet.cell(row=input_row, column=5).value = info[4]        # Genre
    sheet.cell(row=input_row, column=6).value = date_finished


config = configparser.ConfigParser()
config.read('/home/finners/Documents/Coding//Python/Booktracker/settings.ini')
username = config.get('User', 'Username')
password = config.get('User', 'Password')
path = config.get('Spreadsheet', 'Path')

date_finished = get_date()

print('Opening a computer controlled browser window and updating Goodreads...')
driver = webdriver.Firefox()
driver.implicitly_wait(5)

url = goodreads_find()
shelves_list = goodreads_update()
driver.close()
print('Goodreads account updated.')


wb = openpyxl.load_workbook(path)
print('Updating Spreadsheet...')
info = parse_page()

input_info('20' + date_finished[-2:])
input_info('Overall')

wb.save(path)

print('Spreadsheet has been updated.')
print('Booktracker has completed updating both the website and the spreadsheet'
      ' and will now close.')
