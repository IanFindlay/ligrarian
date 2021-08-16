# Ligrarian

A Goodreads librarian - Automates marking a book as read (or reread) on [Goodreads](https://www.goodreads.com/) and stores book information on a local spreadsheet.


  * Automatically logs in and updates your Goodreads account by doing the following:  

    * **Marks the book (specified by URL or through search terms) as read or adds a reread date if previously read**
    * **Sets the Date Finshed to user specified date**
    * **Sets the book's Rating to user specified value**
    * **Inputs Review (optional)**
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
    * **How many of the books are fiction and how many are nonfiction**
    * **Most read author, how many books of theirs you've read and what percentage of your total that equates to**
    * **How many different authors you've read**
    * **Most read genre, how many books in that genre you've read and what percentage of your total that equates to**
    * **How many different genres you've read**

    The Overall sheet is similar but instead of tracking and calculating based upon the current year it does so based upon all years. 


## Usage Instructions

To get started using Ligrarian, download the directory and place it wherever you want within your system. Install the modules listed in requirements.txt as well as a recent release of Firefox and the [geckodriver](https://github.com/mozilla/geckodriver) for it.

Ligrarian has three different input modes - (g)ui, (s)earch and (u)rl. Suffix any of these with the --help argument to print information about their arguments to the terminal.

GUI mode loads the Ligrarian GUI and can be invoked by:

```
python3 ligrarian.py gui
```

There are two different modes on the GUI corresponding to the two other operational modes. The GUI defaults to 'Search Mode' but can be switched to 'URL Mode' via a labelled checkbutton. Enter all non-optional information, press submit and Ligrarian will get to work.

> *__Note__*: *Your Email is saved to the config.ini file in the same directory, so you won't have to enter it every time, and your Password can be saved (insecurely in plaintext) by checking the 'Save Password' box at the end of the first row of the GUI. Once saved, your Password will appear as asterixs in future GUI sessions.*

The other two modes are soley driven by the command-line. If your Email and/or Password aren't saved you will be prompted for that information, asked if you would like to save your password (your email is saved by default) and finally, if you decided not to save your password, asked if you want to remove the save password prompt for future sessions. These settings, the path to the spreadsheet and some GUI defaults can be modified within the settings.ini file.

Search mode will utilise Goodreads search and your chosen format to automatically navigate to a book's page and update it. Arguments are positional and in the following order:
"Search Terms" Format Date Rating ["Review"]

Example Usage:

```
python3 ligrarian.py search "East of Eden John Steinbeck" kindle today 5 "Timshel"
```

The above would update your Goodreads account as having finished reading East of Eden by John Steinbeck on today's date, in Kindle format, rating it 5 stars and leaving "Timshel" as a review for the book.

URL mode bypasses the need to search Goodreads for the book and choose the format as you provide it with a direct link to the book's page that you wish to update. Arguments are positional and in the following order:

URL Date Rating ["Review"] 

Example Usage:

```
python3 ligrarian.py url https://Goodreads.com/ExampleBookUrl t 4
```

Would mark the book at the given URL as having been read today and it would be rated 4 stars.

### Argument Notes:
* The first letter of the operational mode can be used instead of the full word i.e. 'g' rather than 'gui'
* The search terms must be enclosed in quotes if multiple words are used
* The first letter of the format can be used i.e. (p)aperback, (h)ardcover, (k)indle or (e)book
* The date can be (t)oday, (y)esterday or any date written in the DD/MM/YYYY format e.g. 01/01/18 for 1st January 2018
* The rating is a number between 1 and 5
* The review is also enclosed in quotes but is entirely optional in both modes.
