import re
from typing import List

from django.core import checks
from django.core.checks .messages import CheckMessage, DEBUG, INFO, WARNING, ERROR
from django.conf import settings

from mypy import api


# The check framework is used for multiple different kinds of checks. As such, errors
# and warnings can originate from models or other django objects. The `CheckMessage`
# requires an object as the source of the message and so we create a temporary object
# that simply displays the file and line number from mypy (i.e. "location")
class MyPyErrorLocation:
    def __init__(self, location):
        self.location = location

    def __str__(self):
        return self.location


@checks.register()
def mypy(app_configs, **kwargs) -> List:
    print("Performing mypy checks...\n")
    # By default run mypy against the whole database everytime checks are performed.
    # If performance is an issue then `app_configs` can be inspected and the scope 
    # of the mypy check can be restricted
    mypy_args = ['--show-error-codes', '--non-interactive']
    results = api.run(['--show-error-codes', settings.BASE_DIR])
    error_messages = results[0]
    # mypy: install-types 
    if not error_messages:
        return []

    # Example: myproject/checks.py:17: error: Need type annotation for 'errors'
    #pattern = re.compile("^(.+\d+): (\w+): (.+)")
    pattern = re.compile("^(.+\d+): (\w+): (.*?) \[([^]]+)\]")

    errors = [] 
    for message in error_messages.rstrip().split("\n"):
        parsed = re.match(pattern, message)
        if not parsed:
            continue

        location = parsed.group(1)
        mypy_level = parsed.group(2)
        message = parsed.group(3)
        code = parsed.group(4)  
        # now I can filter out messages with specific error codes here...
        # ...
        level = checks.messages.DEBUG
        if mypy_level == "note":
            level = checks.messages.INFO
        elif mypy_level == "warning":
            level = checks.messages.WARNING
        elif mypy_level == "error":
            level = checks.messages.ERROR
        else:
            print(f"Unrecognized mypy level: {mypy_level}")
        
        # negative search
        if (code in ['import']
                or location in ['opt/ceramic_isles_dev/django_artisan/fields.py:21']
                or any(x in message.strip() for x in ['has no attribute "profile"'])) == False:
            errors.append(checks.messages.CheckMessage(level, message, code, obj=MyPyErrorLocation(location)))
        
        #positive search
        # any(x in message.strip() for x in ['Name "_" already defined'])
        # if (code in ['attr-defined']) == True and \
        #     any(x in message.strip() for x in ['has no attribute "profile"']) == False:
        #     errors.append(CheckMessage(level, message, code, obj=MyPyErrorLocation(location)))

    return errors
