Clone the project
First do you need its clone the project of github from this link https://github.com/JACClockdown/task.git
after that you need run enviroment 

# Activate Virtual Env
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

Move to de Config folder 
cd config

Then you need run this command inside Virtual Enviroment
pip install django djangorestframework djangorestframework-simplejwt mysqlclient pytest pytest-django

After that you need run this commands

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Inicialize category
python manage.py init_categorias

# Create superuser (optional)
python manage.py createsuperuser

# Execute server
python manage.py runserver
