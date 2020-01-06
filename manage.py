#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ['AWS_ACCESS_KEY_ID'] = 'AKIARDNEJAIQYLYQSD5K'
    os.environ['AWS_SECRET_ACCESS_KEY'] = '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'
    os.environ['AWS_STORAGE_BUCKET_NAME'] = 'postento'
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'postentoApplication.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
