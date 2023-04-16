import re

from django.conf import settings
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, "user")
        is_authenticated = request.user.is_authenticated
        path = request.path_info.lstrip("/")
        is_exempt_url = any(url.match(path) for url in self.exempt_urls)

        if is_authenticated and path == "entrance_system/login/":
            return redirect("/entrance_system/dashboard/")
        elif is_authenticated or is_exempt_url:
            return None
        else:
            return redirect("/entrance_system/login/")
