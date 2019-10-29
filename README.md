# Django book Catalog Assignment 2019 v107

This web application creates an online catalog for a small local library, where users can browse available books and manage their accounts.

The main features that have currently been implemented are:

* Book catalog Using basic CRUD approach (book, Category, Author, Review) 
* Endpoint using RESTFUL API using Django Rest Framework
* Sign-up, Activate using E-mail, login,logout
* feature to keep track of readed books.  

* Additional Requirement
* Front-end to use the application.
* Social Authentication 
* images upload ()book cover, for example 
                                                                               
* The link to this Application is on PythonAnywhere website as | http://bignamekd.pythonanywhere.com |



## Quick Start

To get this project up and running locally on your computer:
1. Set up the [Python development environment]
   We recommend using a Python virtual environment.
1. Assuming you have Python setup, run the following commands (if you're on Windows you may use `py` or `py -3` instead of `python` to start Python):
   ```
   pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate
   python manage.py collectstatic
   python manage.py runserver
 
 ``
1. Open tab to `http://127.0.0.1:8000/catalog` to see the main site, with your new objects.


