#!/usr/bin/env python3

"""Automatically update Goodreads and local Spreadsheet with book read info."""

import configparser
from datetime import datetime as dt
from datetime import timedelta
import tkinter as tk
import tkinter.messagebox
import sys

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


class GuiInput:
    """Ligrarian GUI structure and related methods."""

    def __init__(self, master):
        self.master = master
        self.master.title("Ligrarian")
        self.width = 665
        self.height = 560
        self.geometry_string = "{}x{}".format(self.width, self.height)
        root.geometry(self.geometry_string)

        # Labels
        self.login_label = tk.Label(root, text="Login")
        self.login_label.grid(row=2, column=1, sticky='W',
                              pady=(30, 5), padx=10)

        self.title_label = tk.Label(root, text="Title")
        self.title_label.grid(row=3, column=1, sticky='W', padx=10)

        self.author_label = tk.Label(root, text="Author")
        self.author_label.grid(row=4, column=1, sticky='W', padx=10)

        self.date_label = tk.Label(root, text="Date")
        self.date_label.grid(row=5, column=1, sticky='W', padx=10)

        self.format_label = tk.Label(root, text="Format")
        self.format_label.grid(row=6, column=1, sticky='W', padx=10)

        self.rating_label = tk.Label(root, text="Rating")
        self.rating_label.grid(row=7, column=1, sticky='W', padx=10)

        self.review_label = tk.Label(root, text="Review\n (optional)", padx=10)
        self.review_label.grid(row=8, column=1, sticky='W')

        # Widgets
        self.email = tk.Entry(root, width=20)
        if user['email']:
            self.email.insert(0, user['email'])
        else:
            self.email.insert(0, 'Email')
        self.email.grid(row=2, column=2, columnspan=3,
                        sticky='W', pady=(30, 5))

        self.password = tk.Entry(root, width=20)
        if user['password']:
            self.password.insert(0, '********')
        else:
            self.password.insert(0, 'Password')
        self.password.grid(row=2, column=4, columnspan=3, sticky='W',
                           pady=(30, 5))

        self.save = tk.IntVar()
        self.save_box = tk.Checkbutton(root, text='Save Password',
                                       variable=self.save, onvalue=True,
                                       offvalue=False)
        self.save_box.grid(row=2, column=7, sticky='W', pady=(30, 5))
        # Select save by default if password already saved
        if user['password']:
            self.save_box.select()

        self.title = tk.Entry(root, width=45)
        self.title.grid(row=3, column=2, columnspan=6,
                        sticky='W', pady=10)

        self.author = tk.Entry(root, width=45)
        self.author.grid(row=4, column=2, columnspan=6, sticky='w', pady=5)

        self.date = tk.Entry(root, width=8)
        self.date.insert(0, today)
        self.date.grid(row=5, column=2, sticky='W', pady=10, ipady=3)

        self.today_button = tk.Button(root, text="Today",
                                      command=self.set_today)

        self.today_button.grid(row=5, column=3, sticky='W', pady=10,)

        self.yesterday_button = tk.Button(root, text="Yesterday",
                                          command=self.set_yesterday)
        self.yesterday_button.grid(row=5, column=4, sticky='W', pady=10)

        formats = ("Paperback", "Hardback", "Kindle", "Ebook",)
        self.book_format = tk.StringVar()
        self.book_format.set('Kindle')
        self.format_drop = tk.OptionMenu(root, self.book_format, *formats)
        self.format_drop.grid(row=6, column=2, columnspan=3,
                              sticky='W', pady=5)

        stars = ("1", "2", "3", "4", "5")
        self.star = tk.StringVar()
        self.star.set('3')
        self.rating = tk.OptionMenu(root, self.star, *stars)
        self.rating.grid(row=7, column=2, sticky='W', pady=5)

        self.review = tk.Text(root, height=15, width=75, wrap=tk.WORD)
        self.review.grid(row=8, column=2, columnspan=7, sticky='W', pady=5)

        self.submit_button = tk.Button(root, text="Mark as Read",
                                       command=self.parse_input)
        self.submit_button.grid(row=12, column=7, columnspan=2,
                                sticky='E', pady=15)

    def set_today(self):
        """Insert today's date into date Entry field."""
        self.date.delete(0, 8)
        self.date.insert(0, today)

    def set_yesterday(self):
        """Insert yesterday's date into date Entry field."""
        self.date.delete(0, 8)
        self.date.insert(0, yesterday)

    def parse_input(self):
        """Create and verify the book details inputted to the GUI."""
        user['email'] = self.email.get()
        user['save_pass'] = self.save.get()

        password = self.password.get()
        if password != '********':
            user['password'] = password

        book_info['title'] = self.title.get()
        book_info['author'] = self.author.get()
        book_info['format'] = self.book_format.get()
        book_info['rating'] = self.star.get()
        book_info['date'] = self.date.get()
        book_info['review'] = self.review.get('1.0', 'end-1c')

        try:
            assert user['email'] != 'Email'
            assert user['password'] != 'Password'
            assert book_info['title']
            assert book_info['author']
            assert book_info['format']
            assert book_info['rating']
            assert book_info['date'] != 'DD/MM/YY'
            root.destroy()

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
    """Find the correct book, in the correct format, on Goodreads."""

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
    """Update Goodreads by marking book as read and adding information."""
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


def parse_page(url):
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


def input_info(sheet_name, title, author, pages, category, genre, date_done):
    """Write the book information to the first blank row on the given sheet."""
    sheet_names = wb.sheetnames
    if sheet_name not in sheet_names:
        create_sheet(sheet_names[-1], sheet_name)

    sheet = wb[sheet_name]

    input_row = first_blank(sheet)

    sheet.cell(row=input_row, column=1).value = title
    sheet.cell(row=input_row, column=2).value = author
    sheet.cell(row=input_row, column=3).value = pages
    sheet.cell(row=input_row, column=4).value = category
    sheet.cell(row=input_row, column=5).value = genre
    sheet.cell(row=input_row, column=6).value = date_done


def first_blank(sheet):
    """Return the first blank row of the given sheet."""
    input_row = 1
    data = ''
    while data is not None:
        data = sheet.cell(row=input_row, column=1).value
        input_row += 1
    input_row -= 1
    return input_row


def create_sheet(last_sheet, sheet_name):
    """Create a new sheet by copying and modifying the last one."""
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
    with open('settings.ini', 'w') as f:
        f.write('[User]\n')
        f.write('Email = ' + email + '\n')
        f.write('Password = ' + password + '\n')
        f.write('\n')
        f.write('[Settings]\n')
        f.write('Prompt = ' + prompt)


def user_info():
    """Prompt for missing user info unless prompt is disabled."""
    if not user['email']:
        email = input('Email: ')
    if not user['password']:
        password = input('Password: ')
        if user['prompt'] == 'no':
            return

        save = input("Save Password?(y/n): ")
        if save.lower() == 'y':
            write_config(email, password, 'yes')
        elif save.lower() == 'n':
            disable = input("Disable save Password prompt?(y/n): ")
            if disable.lower() == 'y':
                write_config(email, "", 'no')
            else:
                write_config(email, "", 'yes')


def retrieve_user(gui=True):
    """Retrieve user info from config file."""
    config = configparser.ConfigParser()
    config.read('settings.ini')
    email = config.get('User', 'Email')
    password = config.get('User', 'Password')
    prompt = config.get('Settings', 'Prompt')

    if gui:
        return (email, password)

    return (email, password, prompt)


if __name__ == '__main__':

    today = dt.strftime(dt.now(), '%d/%m/%y')
    yesterday = dt.strftime(dt.now() - timedelta(1), '%d/%m/%y')

    if len(sys.argv) in (6, 7):
        retrieved_info = retrieve_user(gui=False)
        user['email'], user['password'], user['prompt'] = retrieved_info
        user_info()
        book_info = {
            'title': sys.argv[1], 'author': sys.argv[2], 'date': sys.argv[3],
            'format': sys.argv[4], 'rating': sys.argv[5],  'review': None,
        }
        if len(sys.argv) == 7:
            book_info['review'] = sys.argv[6]

        # Process date if given as (t)oday or (y)esterday into proper format
        if book_info['date'].lower() == 't':
            book_info['date'] = today
        elif book_info['date'].lower() == 'y':
            book_info['date'] = yesterday

    else:
        user = {}
        user['email'], user['password'] = retrieve_user()
        book_info = {}
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW", exit)
        gui = GuiInput(root)
        root.mainloop()
        if user['save_pass']:
            write_config(user['email'], user['password'], 'no')
        else:
            write_config(user['email'], "", 'yes')

    print('Opening a computer controlled browser and updating Goodreads...')
    driver = webdriver.Firefox()
    driver.implicitly_wait(20)

    goodreads_login(driver, user['email'], user['password'])
    url = goodreads_find(driver, book_info['title'], book_info['author'],
                         book_info['format'])

    shelves_list = goodreads_update(driver, book_info['date'],
                                    book_info['review'], book_info['rating'])
    driver.close()
    print('Goodreads account updated.')

    wb = openpyxl.load_workbook('Ligrarian.xlsx')
    print('Updating Spreadsheet...')
    info = parse_page(url)

    year_sheet = '20' + book_info['date'][-2:]

    input_info(year_sheet, info['title'], info['author'], info['pages'],
               info['category'], info['genre'], book_info['date'])

    input_info('Overall', info['title'], info['author'], info['pages'],
               info['category'], info['genre'], book_info['date'])

    wb.save('Ligrarian.xlsx')

    print('Ligrarian has completed and will now close.')
