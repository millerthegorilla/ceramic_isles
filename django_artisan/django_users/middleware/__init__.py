from datetime import datetime
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
import re


class ReauthenticateMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.pages = []
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_superuser:
            match = re.match(r'/admin/', request.path)
            if len(
                    self.pages) and self.pages[-1] is not None and match is not None:
                referred = re.match(r'/admin/', self.pages[-1])
                if referred is None and match is not None:
                    messages.add_message(
                        request, messages.INFO, 'You must reauthenticate')
                    logout(request)
                    self.pages = []
                    return redirect('/admin/login/')

            if request.path[-1] == '/':
                self.pages.append(request.path)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
