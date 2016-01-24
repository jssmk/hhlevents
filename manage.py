#!/usr/bin/env python
import os
import sys
import environ

if __name__ == "__main__":
    if os.path.isfile('.env'):
        environ.Env.read_env('.env')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hhlevents.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)