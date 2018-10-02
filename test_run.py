#!/usr/bin/env python3

"""Do a test run of the Selenium automation that resets account afterwards."""

from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import booktracker as main


username, password = main.user_info()
today = dt.strftime(dt.now(), '%d/%m/%y')
book_info = {
    'title': 'Cannery Row', 'author': 'John Steinbeck', 'date': today,
    'format': 'kindle', 'rating': '4',  'review': 'Test Review',
}

driver = webdriver.Firefox()
driver.implicitly_wait(10)

main.goodreads_login(driver, username, password)
url = main.goodreads_find(driver, book_info['title'], book_info['author'],
                          book_info['format'])

shelves_list = main.goodreads_update(driver, book_info['date'],
                                     book_info['review'], book_info['rating'])


print('Goodreads account updated.')

undo_elem = driver.find_element_by_class_name('wtrStatusRead.wtrUnshelve')
undo_elem.click()
alert_obj = driver.switch_to.alert
alert_obj.accept()

print('Goodreads account reset.')
# Check book no longer marked as read before closing window
driver.find_element_by_class_name('wtrToRead')
driver.close()
