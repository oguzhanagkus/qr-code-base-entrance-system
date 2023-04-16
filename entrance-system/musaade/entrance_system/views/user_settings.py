import json

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from entrance_system.forms import SettingsForm


@csrf_exempt
def view(request):
    if request.method == "POST":
        form = SettingsForm(request.POST or None)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            settings_data = json.load(open(settings.USER_SETTINGS_FILE))
            settings_data["email"]["host"] = cleaned_data["email_host"]
            settings_data["email"]["port"] = cleaned_data["email_port"]
            settings_data["email"]["use_tls"] = cleaned_data["email_use_tls"]
            settings_data["email"]["user"] = cleaned_data["email_user"]
            settings_data["email"]["password"] = cleaned_data["email_password"]
            settings_data["hes_api"]["url"] = cleaned_data["hes_api_url"]
            settings_data["hes_api"]["token"] = cleaned_data["hes_api_token"]
            json.dump(settings_data, open(settings.USER_SETTINGS_FILE, "w"), indent=4)

            settings.HES_API_URL = settings_data["hes_api"]["url"]
            settings.HES_API_TOKEN = settings_data["hes_api"]["token"]

            settings.EMAIL_HOST = settings_data["email"]["host"]
            settings.EMAIL_PORT = settings_data["email"]["port"]
            settings.EMAIL_HOST_USER = settings_data["email"]["user"]
            settings.EMAIL_HOST_PASSWORD = settings_data["email"]["password"]
            settings.EMAIL_USE_TLS = settings_data["email"]["use_tls"]

        return HttpResponseRedirect(request.path_info)
    else:
        settings_data = json.load(open(settings.USER_SETTINGS_FILE))
        data = {
            'title': "Settings",
            "form": SettingsForm(
                initial={
                    "hes_api_url": settings_data["hes_api"]["url"],
                    "hes_api_token": settings_data["hes_api"]["token"],
                    "email_host": settings_data["email"]["host"],
                    "email_port": settings_data["email"]["port"],
                    "email_use_tls": settings_data["email"]["use_tls"],
                    "email_user": settings_data["email"]["user"],
                    "email_password": settings_data["email"]["password"],
                }
            )
        }
        return render(request, "settings.html", data)
