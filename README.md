TASK PROJECT - BACKEND SETUP
===========================

This document describes the steps required to set up and run the Task
backend project locally using Django.

--------------------------------------------------
1. Clone the Repository
--------------------------------------------------

First, clone the project from GitHub:

git clone https://github.com/JACClockdown/task.git

Navigate into the project directory:

cd task

--------------------------------------------------
2. Activate Virtual Environment
--------------------------------------------------

Make sure you have Python installed and activate the virtual environment.

Windows:
venv\Scripts\activate

Mac / Linux:
source venv/bin/activate

--------------------------------------------------
3. Project Configuration
--------------------------------------------------

Move to the configuration folder:

cd config

--------------------------------------------------
4. Install Dependencies
--------------------------------------------------

Inside the virtual environment, install the required dependencies:

pip install django djangorestframework djangorestframework-simplejwt mysqlclient pytest pytest-django

-----------------------------------

python manage.py createsuperuser

# Execute server
python manage.py runserver
