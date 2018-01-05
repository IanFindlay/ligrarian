#!/usr/bin/env python3

"""Automatically updates Books Read spreadsheet with Goodreads data.

Usage:
booktracker.py <URL> - Updates spreadsheet with info from URL and today's date.
booktracker.py <URL> <y/c>- Allows date to be <y>esterday's date or <c>ustom.
"""

import sys
import datetime
from datetime import timedelta
import requests
import openpyxl
import bs4

# Extract information from Goodreads page
URL = sys.argv[1]
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

# Determine the date to write as book finished
TODAY = datetime.datetime.now()

DAY = TODAY.day
if len(str(DAY)) == 1:
    DAY = '0' + str(DAY)
MONTH = TODAY.month
if len(str(MONTH)) == 1:
    MONTH = '0' + str(MONTH)

YEAR = str(TODAY.year)[-2:]

if len(sys.argv) == 2:
    DATE = '{}/{}/{}'.format(DAY, MONTH, YEAR)

else:
    DATE_READ = sys.argv[2]

    if DATE_READ == 'y':
        if DAY != 1:
            DATE = '{}/{}/{}'.format('0' + str(int(DAY) - 1), MONTH, YEAR)
        else:
            YESTERDAY = datetime.datetime.now() - timedelta(days=1)

            DAY = YESTERDAY.day
            MONTH = YESTERDAY.month
            if len(str(MONTH)) == 1:
                MONTH = '0' + str(MONTH)
            YEAR = str(YESTERDAY.year)[-2:]

            DATE = '{}/{}/{}'.format(DAY, MONTH, YEAR)

    elif DATE_READ == 'c':
        DATE = input('Enter the date the book was finished: ')


WB = openpyxl.load_workbook('/home/finners/Documents/Misc/Books Read.xlsx')
print('Updating Spreadsheet...')

# Write information into year sheet
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
    sheet.cell(row=input_row, column=6).value = DATE

    # Edit Formulas - Most Read Author, Most Read Genre
    sheet['I11'] = ('=INDEX($B$2:$B${0},MODE(MATCH($B$2:$B${0},$B$2:$B${0},0)'
                    '))'.format(input_row))

    sheet['I14'] = ('=INDEX($E$2:$E${0},MODE(MATCH($E$2:$E${0},$E$2:$E${0},0)'
                    '))'.format(input_row))


input_info('20' + YEAR)
input_info('Overall')

WB.save('/home/finners/Documents/Misc/Books Read.xlsx')

print('Spreadsheet has been updated.')
