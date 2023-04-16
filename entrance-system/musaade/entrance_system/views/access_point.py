import logging as log

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from entrance_system.forms import AccessPointForm
from entrance_system.models import AccessPoint

page = "/entrance_system/access_points/"


def view(request):
    access_point_form = AccessPointForm()
    access_point_list = AccessPoint.objects.all().order_by("id")
    data = {
        "title": "Access Points",
        "access_point_form": access_point_form,
        "access_point_list": access_point_list,
    }
    return render(request, "access_point/main.html", data)


@csrf_exempt
def add(request):
    try:
        if request.method == "POST":
            form = AccessPointForm(request.POST)
            if form.is_valid():
                form_data = form.cleaned_data
                form.save()
                log.info("New access point added: {}".format(form_data["ssid"]))
                messages.info(request, "Access point added.")
            else:
                log.warning("Submitted form is not valid.")
                messages.warning(request, "Submitted form is not valid.")
    except Exception as exception:
        log.error("Exception occurred while adding access point: {}".format(str(exception)))
        messages.error(request, "Error occurred while adding.")
    finally:
        return redirect(page)


@csrf_exempt
def edit(request, id_):
    response = None
    try:
        if request.method == "POST":
            instance = AccessPoint.objects.filter(id=id_).first()
            form = AccessPointForm(request.POST or None, instance=instance)
            if form.is_valid():
                log.info("Access point edited: {}".format(instance.ssid))
                form.save()
            else:
                log.error("Access point cannot edit.")
            response = HttpResponseRedirect(request.path_info)
    except Exception as exception:
        log.error("Exception occurred while editing access point: {}".format(str(exception)))
    finally:
        if not response:
            instance = AccessPoint.objects.filter(id=id_).first()
            form = AccessPointForm(instance=instance)
            data = {
                "title": "Access Point | Edit",
                "access_point_form": form,
            }
            response = render(request, "access_point/edit.html", data)
        return response


@csrf_exempt
def delete(request, id_):
    try:
        access_point = AccessPoint.objects.filter(id=id_).first()
        access_point.delete()
        log.info("Access point deleted: {}".format(access_point.ssid))
        messages.info(request, "Access point deleted.")
    except Exception as exception:
        log.error("Exception occurred while deleting access point: {}".format(str(exception)))
        messages.error(request, "Error occurred while deleting access point.")
    finally:
        return redirect(page)
