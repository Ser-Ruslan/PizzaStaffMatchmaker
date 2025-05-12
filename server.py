import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Add the pizza_recruitment directory to the Python path
pizza_recruitment_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pizza_recruitment')
sys.path.insert(0, pizza_recruitment_dir)

# Set the Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pizza_recruitment.settings')

# Import Django setup
import django
django.setup()

# Import the WSGI application
from pizza_recruitment.wsgi import application

# Import the HTTP server
from werkzeug.serving import run_simple

if __name__ == '__main__':
    # Run the application on 0.0.0.0:5000
    run_simple('0.0.0.0', 5000, application, use_reloader=True, use_debugger=True)
