The application implements search features into doxygen documentation.  
Features:
- allows to find help pages by text into description
- supports searching by substring
- single application supports working with some instances of documentations
- don't need internet access

The application uses the Python + Django for its work.  
The application is designed to run on the local computer where a generated documentation is located.  

**Prerequisites:**  
- Python vers. 3 with Django framework (free software).  
Its easy to find on the Internet a description of installation process.

**Installation**  
Execute the following commands in the folder of doxy-search (contains the manage.py):  
1. Initializing the database  
**python3 manage.py makemigrations**  
**python3 manage.py migrate**  
1. Run doxy-search application  
**python3 manage.py runserver**  

**Usage**
Open link [doxy-search admin](http://127.0.0.1:8000) into browser and follow **Quick start** section.    
  
Evgeny Kislov, 2021-2022. 
