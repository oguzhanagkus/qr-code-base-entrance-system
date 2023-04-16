import logging as log

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from entrance_system.forms import ImportForm, DepartmentForm
from entrance_system.models import Department

page = "/entrance_system/departments/"


def view(request):
    import_form = ImportForm()
    department_form = DepartmentForm()
    department_list = Department.objects.all().order_by("id")
    data = {
        "title": "Departments",
        "import_form": import_form,
        "department_form": department_form,
        "department_list": department_list,
    }
    return render(request, "department/main.html", data)


@csrf_exempt
def add(request):
    try:
        if request.method == "POST":
            form = DepartmentForm(request.POST)
            if form.is_valid():
                form_data = form.cleaned_data
                form.save()
                log.info("New department added: {}".format(form_data["name"]))
                messages.info(request, "Department added.")
            else:
                log.warning("Submitted form is not valid.")
                messages.warning(request, "Submitted data is not valid.")
    except Exception as exception:
        log.error("Exception occurred while adding department: {}".format(str(exception)))
        messages.error(request, "Error occurred while adding.")
    finally:
        return redirect(page)


@csrf_exempt
def edit(request, id_):
    response = None
    try:
        if request.method == "POST":
            instance = Department.objects.filter(id=id_).first()
            form = DepartmentForm(request.POST or None, instance=instance)
            if form.is_valid():
                log.info("Department edited: {}".format(instance.name))
                form.save()
            else:
                log.error("Department cannot edit.")
            response = HttpResponseRedirect(request.path_info)
    except Exception as exception:
        log.error("Exception occurred while editing department: {}".format(str(exception)))
    finally:
        if not response:
            instance = Department.objects.filter(id=id_).first()
            form = DepartmentForm(instance=instance)
            data = {
                "title": "Departments | Edit",
                "department_form": form,
            }
            response = render(request, "department/edit.html", data)
        return response


@csrf_exempt
def delete(request, id_):
    try:
        department = Department.objects.filter(id=id_).first()
        department.delete()
        log.info("Department deleted: {}".format(department.name))
        messages.info(request, "Department deleted.")
    except Exception as exception:
        log.error("Exception occurred while deleting department: {}".format(str(exception)))
        messages.error(request, "Error occurred while deleting.")
    finally:
        return redirect(page)
