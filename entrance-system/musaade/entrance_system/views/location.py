import base64
import logging as log

import pyqrcode
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from entrance_system.forms import LocationForm
from entrance_system.models import Location
from entrance_system.utils import HardwareInitializer

page = "/entrance_system/locations/"


def view(request):
    location_form = LocationForm()
    location_list = Location.objects.all().order_by("id")
    data = {
        "title": "Locations",
        "location_form": location_form,
        "location_list": location_list,
    }
    return render(request, "location/main.html", data)


@csrf_exempt
def add(request):
    try:
        if request.method == "POST":
            form = LocationForm(request.POST)
            if form.is_valid():
                form_data = form.cleaned_data
                form.save()
                log.info("New locations added: {}".format(form_data["name"]))
                messages.info(request, "Location added.")
            else:
                log.warning("Submitted form is not valid.")
                messages.warning(request, "Submitted form is not valid.")
    except Exception as exception:
        log.error("Exception occurred while adding location: {}".format(str(exception)))
        messages.error(request, "Error occurred while adding.")
    finally:
        return redirect(page)


@csrf_exempt
def edit(request, id_):
    response = None
    try:
        if request.method == "POST":
            instance = Location.objects.filter(id=id_).first()
            form = LocationForm(request.POST or None, instance=instance)
            if form.is_valid():
                log.info("Location edited: {}".format(instance.name))
                form.save()
            else:
                log.error("Location cannot edit.")
            response = HttpResponseRedirect(request.path_info)
    except Exception as exception:
        log.error("Exception occurred while editing location: {}".format(str(exception)))
    finally:
        if not response:
            instance = Location.objects.filter(id=id_).first()
            form = LocationForm(instance=instance)
            data = {
                "title": "Location | Edit",
                "location_form": form,
            }
            response = render(request, "location/edit.html", data)
        return response


@csrf_exempt
def delete(request, id_):
    try:
        location = Location.objects.filter(id=id_).first()
        location.delete()
        log.info("Location deleted: {}".format(location.name))
        messages.info(request, "Location deleted.")
    except Exception as exception:
        log.error("Exception occurred while deleting location: {}".format(str(exception)))
        messages.error(request, "Error occurred while deleting location.")
    finally:
        return redirect(page)


def change_status(request, id_):
    try:
        location = Location.objects.filter(id=id_).first()
        location.active = not location.active
        location.save()
        log.info("Location status changed: {}-> {}".format(location.name, location.active))
        messages.info(request, "Location status changed.")
    except Exception as exception:
        log.error("Exception occurred while changing location status: {}".format(str(exception)))
        messages.error(request, "Error occurred while changing location status.")
    finally:
        return redirect(page)


def download_qr_code(request, id_):
    response = None
    try:
        location = Location.objects.filter(id=id_).first()
        filename = location.name.lower().replace(" ", "_")

        response = HttpResponse(content_type="image/png")
        response["Content-Disposition"] = "attachment; filename={}_setup_qr_code.png".format(filename)

        hardware_initializer = HardwareInitializer(
            location.access_point.ssid,
            location.access_point.password,
            location.api_token
        )

        content = hardware_initializer.generate_qr_code_data()
        response.write(content)

    except Exception as exception:
        log.error("Error occurred while downloading QR code: {}".format(str(exception)))
        messages.error(request, "Error occurred while downloading.")
        response = redirect(page)
    finally:
        return response
