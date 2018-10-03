# Ligrarian

A Goodreads librarian - Automates marking a book as read on [Goodreads](https://www.goodreads.com/) and stores book information on a local spreadsheet.


  * Automatically logins in and updates your Goodreads account by doing the following:  

    * **Finds the book in the format specified and marks it as read**  
    * **Sets the 'Date Finshed'**  
    * **Sets the books rating**
    * **Inputs review if one is given through the GUI**  
    * **Shelves the book based upon the accounts pre-existing shelves and the sites 'Top Shelves' for the book**  

  * Automtically updates a spreadsheet, both a year sheet and an overall sheet, with the following information:

    * **Book Title with Series Name and Book # in Series (if applicable)**  
    * **Author**  
    * **Number of Pages**  
    * **Category (Fiction or Nonfiction)**  
    * **Genre**  
    * **Date Finished**

## Installation


## Usage Instructions

The first time you run Ligrarian, you will be prompted for your Goodreads Username and Password and asked whether you wish this information to be saved locally (in the config.ini file in the same directory) or forgotten once the program terminates. After that the GUI shown below will load. Fill out all of the information and then press Submit. A Selenium automated browser window will load, update your Goodreads account and then close.

This GUI can, however, be bypassed by entering the book's details as arguments to the program from the command line. For example:

```
python3 ligrarian.py "East of Eden" "John Steinbeck" 31/01/18 k 5
```
Would update your Goodreads account as having read East of Eden by John Steinbeck, in Kindle format, rating it 5 stars and marking it as completed on the 31st of January 2018.

Note that both the Book Title and Author Name are enclosed in quotes, the date is formatted as DD/MM/YY, the first letter of the format is used i.e. 'p' for paperback and the rating is a number between 1 and 5.