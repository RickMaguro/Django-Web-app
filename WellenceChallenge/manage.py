#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.management import execute_from_command_line

def init_db():
    from django.db import connections
    from django.db.utils import OperationalError
    try:
        connection = connections['default']
        connection.cursor()
    except OperationalError:
        print("Database does not exist, creating...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("Database creation and migration complete")
    else:
        print("Database already exists, checking for pending migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("Migrations check complete")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WellenceChallenge.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        init_db()
    
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
