# Ligrarian

A Goodreads librarian - Automates marking a book as read on [Goodreads](https://www.goodreads.com/) and stores book information on a local spreadsheet.


  * Automatically logs in and updates your Goodreads account by doing the following:  

    * **Finds the book in the Format specified and marks it as read**
    * **Sets the Date Finshed to user specified date**
    * **Sets the book's Rating to user specified value**
    * **Inputs Review if one is given**
    * **Shelves the book based upon the accounts pre-existing Shelves and the sites 'Top Shelves' for the book**

  * Automtically updates a spreadsheet, both a year sheet and an overall sheet, with the following information:

    * **Book Title with Series Name and Number in Series (if applicable)**
    * **Author**
    * **Number of Pages**
    * **Category (Fiction or Nonfiction)**
    * **Genre**
    * **Date Finished**

  * The spreadsheet calculates and displays the following additional information:  

    * **How many weeks have passed since the beginning of the year**
    * **How many books you've read**
    * **How many pages you've read**
    * **Average book length**
    * **How many of the books are Fiction and how many are Nonfiction**
    * **Most read author, how many books of theirs you've read and what percentage of your total that equates to**
    * **How many different authors you've read**
    * **Most read genre, how many books in that genre you've read and what percentage of your total that equates to**
    * **How many different genres you've read**

    The Overall sheet is similar but instead of tracking and calculating based upon the current year it does so based upon all years. 


## Usage Instructions

To get started using Ligrarian, download the directory and place it wherever you want within your system. Install the modules listed in requirements.txt, Firefox and the [geckodriver](https://github.com/mozilla/geckodriver) for it.

Running ligrarian.py through Python 3 will load the GUI pictured below. Simply fill out all of the non-optional fields and press 'Mark as Read'. The GUI window will close, an automated Firefox session will begin and your account and the spreadsheet will soon be updated.

Your email is saved to the config.ini file in the same directory, so you won't have to enter it every time, but whether or not your password is saved (in plain text in the same file) is up to you. Checking the 'Save Password' box at the end of the first row of the GUI will save your password, which will appear as '********' in future GUI sessions.

This GUI can, however, be bypassed through the use of command line arguments. You will be prompted for your Email and Password if they are not saved, asked if you would like to save your Password and finally, if you opt not to save it, asked if you would like the Save Password prompt itself to be disabled. You can also, at any time, edit the config file direcly usign a text editor.

The format and order for the command line arguments are as follows:

```
python3 ligrarian.py "East of Eden" "John Steinbeck" t k 5 "Insert review here"
```
The above would update your Goodreads account as having finished reading East of Eden by John Steinbeck on today's date, in Kindle format, rating it 5 stars and leaving "Insert review here" as a review for the book

### Note that:
* Both the Book Title and Author Name are enclosed in quotes
* The date can be (t)oday, (y)esterday or any date written in the DD/MM/YY format e.g. 01/01/18 for 1st January 2018
* The first letter of the format can be used i.e. (p)aperback, (h)ardcover, (k)indle or (e)book
* The rating is a number between 1 and 5
* The review is also enclosed in quotes but is entirely optional