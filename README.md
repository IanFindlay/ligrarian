# Booktracker
Takes three obligatory sys arguments: [Book Title Author Name] [Format]-('h'ardback | 'k'indle | 'p'aperback) [Star Rating]  
and a fourth optional argument: [Date Read]-(defaults to today's date but can be set to 'y'esterday or 'c'ustom) and:

  * Automatically updates your [Goodreads](https://www.goodreads.com/) account by doing the following:  

    * **Finds the book in the format the user specifies and marks it as read**  
    * **Sets the 'Date Finshed' to a user specified date**  
    * **Sets the books rating to a user specified number of stars**  
    * **Shelves the book based upon the users pre-existing shelves and the sites 'Top Shelves' for the book**  

  * Automtically updates a spreadsheet with the following info derived from the book's Goodreads page:

    * **Book Title with Series Name and Book # in Series (if applicable)**  
    * **Author**  
    * **Number of Pages**  
    * **Category (Fiction or Nonfiction)**  
    * **Genre**  
    * This information, alongside **Date Finished** is added to both this year's sheet and an overall sheet.
