# Booktracker
Takes four sys arguments: [Book Title Author Name] [Format]-('k'indle|'p'aperback) [Star Rating] [Date Read]-('t'oday|y'esterday|'c'ustom) and:

  * Automatically logins in and updates a [Goodreads](https://www.goodreads.com/) account by doing the following:  

    * **Finds the book in the format specified and marks it as read**  
    * **Sets the 'Date Finshed' to specified date**  
    * **Sets the books rating to the specified number of stars**  
    * **Shelves the book based upon the accounts pre-existing shelves and the sites 'Top Shelves' for the book**  

  * Automtically updates a spreadsheet, both a year sheet and an overall sheet, with the following information:

    * **Book Title with Series Name and Book # in Series (if applicable)**  
    * **Author**  
    * **Number of Pages**  
    * **Category (Fiction or Nonfiction)**  
    * **Genre**  
    * **Date Finished**
