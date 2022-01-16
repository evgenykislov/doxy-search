# doxy-search
A search engine for searching doxygen generated documentation.
The server allows you to search the documentation not only by keywords, but also by description.
Unlike doxysearch ??? the server allows you to search for a part of the string.
The server also supports working with several documentation.
To work, you do not need access to the Internet and other cloud solutions.

The server is designed to run on a local computer, in the same place where the generated documentation is located.

The doxy-search server uses the Django python framework for its work.

The following describes how to install and use the server.


* ** Pre-installed software **
Requires python version 3 installed which has Django package installed. Python and Django are free software. The description of its installation for your version of the operating system is easiest to find on the Internet.

* **Installation**
  In the folder of the downloaded doxy-search (it contains the manage.py file), execute the following commands:
  1. ** Initializing the database **
  python3 manage.py makemigrations
  python3 manage.py migrate
  1. ** Run doxy-search **
  python3 manage.py runserver

* Add documentation
You will need to change the settings in the Doxyfile and make two generations of documentation:
  - Open Doxyfile in doxywizard and set the following fields in the Expert tab in the HTML topic:
    - SEARCHENGINE - Yes
    - SERVER_BASED_SEARCH - Yes
    - EXTERNAL_SEARCH - Yes
    - SEARCHENGINE_URL - empty string
    - SEARCHDATA_FILE - searchdata.xml (it's default value)
  - we generate documentation
  - we find the file searchdata.xml (usually located in the parent folder relative to the generated documentation) and remember its path
  - create a project in doxy-search
    - Open the page in the browser: http://127.0.0.1:8000/localsrv/admin
    - Click to add documentation
    - Enter the desired documentation name and the path to the searchdata.xml file. You can also specify 'slug' (optional).
    - Click Save and Exit
  - On the main page for the created documentation, copy the search link.
  - Open Doxyfile in doxywizard and set the following fields in the Expert tab in the HTML topic:
    - SEARCHENGINE_URL - indicate the link (see the previous step)
  - we generate documentation
  - On the main page for the generated documentation, click the update button (after the second generation)

* Using search
- Open the documentation in the browser (index.html)
- In the search field, type the desired line, press the search button or enter.

* Documentation update
If the documentation has been updated, then the search base must also be updated.
To do this, go to the main page: http://127.0.0.1:8000/localsrv/admin/
And for the required documentation, click Update.


Kislov Evgeniy, 2021-2022. 



