import sys

import os

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    BASE_DIR = os.environ.get("DJANGO_BASE_DIR", os.path.abspath(os.path.dirname(__file__)))
    os.environ.setdefault("DJANGO_BASE_DIR", BASE_DIR)

    DJANGO_SETTINGS_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE", "tests.settings")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)

    execute_from_command_line(sys.argv)
