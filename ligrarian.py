#!/usr/bin/env python3

"""Automatically update Goodreads and local Spreadsheet with book read info.

Without arguments ligrarian.py loads a GUI. This can be bypassed via arguments

Args:
    Title of Book: Enclosed in double quotation marks
    Author of Book: Enclosed in double quotation marks
    Read Date: (t)oday, (y)esterday or a date formatted DD/MM/YY
    Format: (p)aperback, (h)ardcover, (k)indle or (e)book
    Rating: Number between 1 and 5

Optional Args:
    Review (Optional): Enclosed in double quotation marks

"""

import argparse
import configparser
from datetime import datetime as dt
from datetime import timedelta
import sys
import tkinter as tk
import tkinter.messagebox

import bs4
import openpyxl
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


class GuiInput():
    """Ligrarian GUI layout and related methods."""

    def __init__(self, master, email, password, today, yesterday):
        self.email = email
        self.password = password
        self.today = today
        self.yesterday = yesterday

        self.master = master
        self.master.title("Ligrarian")
        self.width = 665
        self.height = 560
        self.geometry_string = "{}x{}".format(self.width, self.height)
        self.master.geometry(self.geometry_string)

        # Labels
        self.login_label = tk.Label(self.master, text="Login")
        self.login_label.grid(row=2, column=1, sticky='W',
                              pady=(30, 5), padx=10)

        self.title_label = tk.Label(self.master, text="Title")
        self.title_label.grid(row=3, column=1, sticky='W', padx=10)

        self.author_label = tk.Label(self.master, text="Author")
        self.author_label.grid(row=4, column=1, sticky='W', padx=10)

        self.date_label = tk.Label(self.master, text="Date")
        self.date_label.grid(row=5, column=1, sticky='W', padx=10)

        self.format_label = tk.Label(self.master, text="Format")
        self.format_label.grid(row=6, column=1, sticky='W', padx=10)

        self.rating_label = tk.Label(self.master, text="Rating")
        self.rating_label.grid(row=7, column=1, sticky='W', padx=10)

        self.review_label = tk.Label(self.master, text="Review\n (optional)",
                                     padx=10)
        self.review_label.grid(row=8, column=1, sticky='W')

        # Widgets
        self.login_email = tk.Entry(self.master, width=20)
        if self.email:
            self.login_email.insert(0, self.email)
        else:
            self.login_email.insert(0, 'Email')
        self.login_email.grid(row=2, column=2, columnspan=3,
                              sticky='W', pady=(30, 5))

        self.login_password = tk.Entry(self.master, width=20)
        if self.password:
            self.login_password.insert(0, '********')
        else:
            self.login_password.insert(0, 'Password')
        self.login_password.grid(row=2, column=4, columnspan=3, sticky='W',
                                 pady=(30, 5))

        self.save = tk.IntVar()
        self.save_box = tk.Checkbutton(self.master, text='Save Password',
                                       variable=self.save, onvalue=True,
                                       offvalue=False)
        self.save_box.grid(row=2, column=7, sticky='W', pady=(30, 5))
        # Select save by default if password already saved
        if self.password:
            self.save_box.select()

        self.title = tk.Entry(self.master, width=45)
        self.title.grid(row=3, column=2, columnspan=6,
                        sticky='W', pady=10)

        self.author = tk.Entry(self.master, width=45)
        self.author.grid(row=4, column=2, columnspan=6, sticky='w', pady=5)

        self.date = tk.Entry(self.master, width=8)
        self.date.insert(0, today)
        self.date.grid(row=5, column=2, sticky='W', pady=10, ipady=3)

        self.today_button = tk.Button(self.master, text="Today",
                                      command=self.set_today)

        self.today_button.grid(row=5, column=3, sticky='W', pady=10,)

        self.yesterday_button = tk.Button(self.master, text="Yesterday",
                                          command=self.set_yesterday)
        self.yesterday_button.grid(row=5, column=4, sticky='W', pady=10)

        def_format = get_setting('Defaults', 'Format')
        formats = ("Paperback", "Hardback", "Kindle", "Ebook",)
        self.book_format = tk.StringVar()
        self.book_format.set(def_format)
        self.format = tk.OptionMenu(self.master, self.book_format, *formats)
        self.format.grid(row=6, column=2, columnspan=3,
                         sticky='W', pady=5)

        def_rating = get_setting('Defaults', 'Rating')
        stars = ("1", "2", "3", "4", "5")
        self.star = tk.StringVar()
        self.star.set(def_rating)
        self.rating = tk.OptionMenu(self.master, self.star, *stars)
        self.rating.grid(row=7, column=2, sticky='W', pady=5)

        self.review = tk.Text(self.master, height=15, width=75, wrap=tk.WORD)
        self.review.grid(row=8, column=2, columnspan=7, sticky='W', pady=5)

        self.submit_button = tk.Button(self.master, text="Mark as Read",
                                       command=self.parse_input)
        self.submit_button.grid(row=12, column=7, columnspan=2,
                                sticky='E', pady=15)

    def set_today(self):
        """Insert today's date into date Entry field."""
        self.date.delete(0, 8)
        self.date.insert(0, self.today)

    def set_yesterday(self):
        """Insert yesterday's date into date Entry field."""
        self.date.delete(0, 8)
        self.date.insert(0, self.yesterday)

    def parse_input(self):
        """Create and verify the book details inputted to the GUI."""
        self.email = self.login_email.get()
        self.save = self.save.get()

        password = self.login_password.get()
        if password != '********':
            self.password = password

        self.book_title = self.title.get()
        self.book_author = self.author.get()
        self.book_format = self.book_format.get()
        self.book_rating = self.star.get()
        self.book_date = self.date.get()
        self.book_review = self.review.get('1.0', 'end-1c')

        try:
            assert self.email != 'Email'
            assert self.password != 'Password'
            assert self.book_title
            assert self.book_author
            assert self.book_format
            assert self.book_rating
            assert self.book_date != 'DD/MM/YY'
            self.master.destroy()

        except AssertionError:
            tk.messagebox.showwarning(message="Complete all non-optional "
                                      "fields before marking as read.")


def goodreads_login(driver, email, password):
    """Login to Goodreads account from the homepage."""
    driver.get('https://goodreads.com')

    email_elem = driver.find_element_by_name('user[email]')
    email_elem.send_keys(email)
    pass_elem = driver.find_element_by_name('user[password]')
    pass_elem.send_keys(password)
    pass_elem.send_keys(Keys.ENTER)

    try:
        driver.find_element_by_class_name('siteHeader__personal')
    except NoSuchElementException:
        print('Failed to login - Email and/or Password probably incorrect.')
        driver.close()
        exit()


def goodreads_find(driver, title, author, book_format):
    """Find the book in the specified format on Goodreads and return URL."""

    # Find correct book and edition
    search_elem = driver.find_element_by_class_name('searchBox__input')
    search_elem.send_keys(title + ' ' + author + '%3Dauthor')
    search_elem.send_keys(Keys.ENTER)

    try:
        edition_elem = driver.find_element_by_partial_link_text('edition')
        edition_elem.click()
    except NoSuchElementException:
        print("Failed to find book - Title or Author probably incorrect.")
        driver.close()
        exit()

    pre_filter_url = driver.current_url

    # Filter by format
    filter_elem = driver.find_element_by_name('filter_by_format')
    filter_elem.click()
    filter_elem.send_keys(book_format)
    filter_elem.send_keys(Keys.ENTER)

    # Make sure filtered page is loaded before clicking top book
    WebDriverWait(driver, 10).until(
        EC.url_changes((pre_filter_url))
    )

    # Select top book
    title_elem = driver.find_element_by_class_name('bookTitle')
    title_elem.click()

    return driver.current_url


def goodreads_update(driver, date_done, review, rating):
    """Review book on Goodreads, parse and return the book's 'Top Shelves'."""
    # Mark as Read
    menu_elem = driver.find_element_by_class_name('wtrShelfButton')
    menu_elem.click()
    search_elem = driver.find_element_by_class_name('wtrShelfSearchField')
    search_elem.click()
    search_elem.send_keys('read', Keys.ENTER)

    # Date Selection
    year = '20' + date_done[6:]
    month = date_done[3:5].lstrip('0')
    day = date_done[:2].lstrip('0')

    year_class = 'rereadDatePicker.smallPicker.endYear'
    month_class = 'rereadDatePicker.largePicker.endMonth'
    day_class = 'rereadDatePicker.smallPicker.endDay'
    Select(driver.find_element_by_class_name(year_class)
           ).select_by_visible_text(year)

    Select(driver.find_element_by_class_name(month_class)
           ).select_by_value(month)

    Select(driver.find_element_by_class_name(day_class)
           ).select_by_visible_text(day)

    # Write review if one entered
    if review:
        review_elem = driver.find_element_by_name('review[review]')
        review_elem.click()
        review_elem.send_keys(review)

    # Save
    save_elem = driver.find_element_by_name('next')
    save_elem.click()

    # Shelf selection
    shelves_elems = driver.find_elements_by_class_name('actionLinkLite.'
                                                       'bookPageGenreLink')
    shelves = []
    for shelf in shelves_elems:
        if ' users' not in shelf.text and shelf.text not in shelves:
            shelves.append(shelf.text)

    if rating == '5':
        shelves.append('5-star-books')

    # Wait until review box is invisible
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, "box"))
    )

    menu_elem = driver.find_element_by_class_name('wtrShelfButton')
    menu_elem.click()
    shelf_elem = driver.find_element_by_class_name('wtrShelfSearchField')

    for i in range(len(shelves)):
        shelf_elem.send_keys(shelves[i], Keys.ENTER)
        shelf_elem.send_keys(Keys.SHIFT, Keys.HOME, Keys.DELETE)

    # Close dropdown and wait until it disappears
    menu_elem.click()
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "wtrShelfList"))
    )

    # Give star rating
    stars_elem = driver.find_elements_by_class_name('star.off')
    for stars in stars_elem:
        if stars.text.strip() == '{} of 5 stars'.format(rating):
            stars.click()
            break

    return shelves


def parse_page(url, shelves_list):
    """Parse and return page information needed for spreadsheet."""
    info = {}
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    title_elem = soup.select('#bookTitle')

    rough_title = title_elem[0].getText().strip().split('\n')
    if len(rough_title) == 1:
        title = rough_title[0].strip()
    else:
        title = rough_title[0].strip() + ' ' + rough_title[2].strip()

    info['title'] = title

    author_elem = soup.select('.authorName')
    author = author_elem[0].getText().strip()
    info['author'] = author

    pages_elem = soup.findAll('span', attrs={'itemprop': 'numberOfPages'})
    pages = int(pages_elem[0].getText().strip(' pages'))
    info['pages'] = pages

    if shelves_list[0] == 'Fiction' or shelves_list[0] == 'Nonfiction':
        category = shelves_list[0]
        genre = shelves_list[1]
    else:
        genre = shelves_list[0]
        if 'Nonfiction' in shelves_list:
            category = 'Nonfiction'
        else:
            category = 'Fiction'

    info['category'] = category
    info['genre'] = genre

    return info


def input_info(wb, sheet_name, title, author, pages, category, genre, date):
    """Write the book information to the first blank row on the given sheet."""
    sheet_names = wb.sheetnames
    if sheet_name not in sheet_names:
        create_sheet(wb, sheet_names[-1], sheet_name)

    sheet = wb[sheet_name]

    input_row = first_blank(sheet)

    sheet.cell(row=input_row, column=1).value = title
    sheet.cell(row=input_row, column=2).value = author
    sheet.cell(row=input_row, column=3).value = pages
    sheet.cell(row=input_row, column=4).value = category
    sheet.cell(row=input_row, column=5).value = genre
    sheet.cell(row=input_row, column=6).value = date


def first_blank(sheet):
    """Return the number of the first blank row of the given sheet."""
    input_row = 1
    data = ''
    while data is not None:
        data = sheet.cell(row=input_row, column=1).value
        input_row += 1
    input_row -= 1
    return input_row


def create_sheet(wb, last_sheet, sheet_name):
    """Create a new sheet by copying and modifying the latest one."""
    sheet = wb.copy_worksheet(wb[last_sheet])
    sheet.title = sheet_name
    last_row = first_blank(sheet)
    while last_row > 1:
        for col in range(1, 7):
            sheet.cell(row=last_row, column=col).value = None
        last_row -= 1
    day_tracker = '=(TODAY()-DATE({},1,1))/7'.format(sheet_name)
    sheet.cell(row=5, column=9).value = day_tracker


def write_config(email, password, prompt):
    """Write configuration file."""
    config = configparser.ConfigParser()
    config.read('settings.ini')
    config.set('User', 'Email', email)
    config.set('User', 'Password', password)
    config.set('Settings', 'Prompt', prompt)

    with open('settings.ini', 'w') as configfile:
        config.write(configfile)


def get_setting(section, option):
    """Return the value associated with option under section in settings"""
    config = configparser.ConfigParser()
    config.read('settings.ini')
    value = config.get(section, option)

    return value


def user_info():
    """Prompt for missing user info unless prompt is disabled."""
    if not get_setting('User', 'Email'):
        email = input('Email: ')
    if not get_setting('User', 'Password'):
        password = input('Password: ')
        if get_setting('Settings', 'Prompt') == 'no':
            return (email, password)

        save = input("Save Password?(y/n): ")
        if save.lower() == 'y':
            write_config(email, password, 'yes')
        elif save.lower() == 'n':
            disable = input("Disable save Password prompt?(y/n): ")
            if disable.lower() == 'y':
                write_config(email, "", 'no')
            else:
                write_config(email, "", 'yes')


def parse_arguments():
    """Parse command line arguments and return a dictionary of their values."""
    parser = argparse.ArgumentParser(description="Goodreads updater")
    parser.add_argument('title', metavar="'title'",
                        help="Book title enclosed within quotes")
    parser.add_argument('author', metavar="'author'",
                        help="Book author enclosed within quotes")
    parser.add_argument('date', help=("(t)oday, (y)esterday or "
                                      "date formatted DD/MM/YY"))
    parser.add_argument('format', metavar='format',
                        choices=['e', 'h', 'k', 'p'],
                        help="(p)aperback, (h)ardcover, (k)indle, (e)book")
    parser.add_argument('rating', type=int, metavar='rating',
                        choices=[1, 2, 3, 4, 5],
                        help="A number 1 through 5")
    parser.add_argument('review', nargs='?', metavar="'review'",
                        help="Review enclosed in quotes")

    args = parser.parse_args()

    return vars(args)


def main():
    """Coordinate Updating of Goodreads account and writing to spreasheet."""
    today = dt.strftime(dt.now(), '%d/%m/%y')
    yesterday = dt.strftime(dt.now() - timedelta(1), '%d/%m/%y')
    email = get_setting('User', 'Email')
    password = get_setting('User', 'Password')

    # Bypass GUI and process command line arguments if given
    if len(sys.argv) > 1:
        user_info()
        book_info = parse_arguments()

        # Process date if given as (t)oday or (y)esterday into proper format
        if book_info['date'].lower() == 't':
            book_info['date'] = today
        elif book_info['date'].lower() == 'y':
            book_info['date'] = yesterday

    else:
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW", exit)
        gui = GuiInput(root, email, password, today, yesterday)
        root.mainloop()
        book_info = {
            'title': gui.book_title, 'author': gui.book_author,
            'date': gui.book_date, 'format': gui.book_format,
            'rating': gui.book_rating,  'review': gui.book_review,
        }

        if gui.save:
            write_config(email, password, 'no')
        else:
            write_config(email, "", 'yes')

    print('Opening a computer controlled browser and updating Goodreads...')
    driver = webdriver.Firefox()
    driver.implicitly_wait(20)

    goodreads_login(driver, email, password)
    url = goodreads_find(driver, book_info['title'], book_info['author'],
                         book_info['format'])

    shelves_list = goodreads_update(driver, book_info['date'],
                                    book_info['review'], book_info['rating'])
    driver.close()
    print('Goodreads account updated.')

    path = get_setting('Settings', 'Path')
    wb = openpyxl.load_workbook(path)
    print('Updating Spreadsheet...')
    info = parse_page(url, shelves_list)

    year_sheet = '20' + book_info['date'][-2:]

    input_info(wb, year_sheet, info['title'], info['author'], info['pages'],
               info['category'], info['genre'], book_info['date'])

    input_info(wb, 'Overall', info['title'], info['author'], info['pages'],
               info['category'], info['genre'], book_info['date'])

    wb.save(path)

    print('Ligrarian has completed and will now close.')


if __name__ == '__main__':
    main()
