import logging

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from management_system.forms import CustomerForm
from management_system.models import Customer
from management_system import utils

page = "/customers/"


@csrf_exempt
def user_login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/customers/")
        return redirect('/login/')
    else:
        pass


def user_logout(request):
    logout(request)
    return redirect('/login/')


@csrf_exempt
def completed(request):
    try:
        company_name = request.POST['company_name']
        ip = request.POST['ip']
        customer_ = Customer.objects.get(company_name=company_name)
        customer_.ip_address = ip
        customer_.save()
        utils.notify_customer(customer_.company_name, customer_.email, customer_.ip_address)
    except Exception as exception:
        logging.exception(exception)
    finally:
        return HttpResponse('')


def customer(request):
    data = {
        "title": "Customers",
        "customer_form": CustomerForm(),
        "customer_list": Customer.objects.all().order_by("id"),
    }
    return render(request, "customer/main.html", data)


@csrf_exempt
def customer_add(request):
    try:
        if request.method == "POST":
            form = CustomerForm(request.POST)
            if form.is_valid():
                form_data = form.cleaned_data
                form.save()
                logging.info("New customer added: {}".format(form_data["company_name"]))
                messages.info(request, "Customer added. Instance initializing.")
                droplet_id = utils.init_instance(form_data["company_name"])
                logging.info("Creating droplet with ID: {}".format(droplet_id))
            else:
                logging.warning("Submitted form is not valid.")
                messages.warning(request, "Submitted form is not valid.")
    except Exception as exception:
        logging.error(exception)
        logging.error("Exception occurred while adding customer: {}".format(str(exception)))
        messages.error(request, "Error occurred while adding.")
    finally:
        return redirect(page)


@csrf_exempt
def customer_delete(request, id_):
    try:
        customer_ = Customer.objects.filter(id=id_).first()
        customer_.delete()
        logging.info("Customer deleted: {}".format(customer_.company_name))
        messages.info(request, "Customer deleted.")
    except Exception as exception:
        logging.error("Exception occurred while deleting customer: {}".format(str(exception)))
        messages.error(request, "Error occurred while deleting.")
    finally:
        return redirect(page)


@csrf_exempt
def customer_edit(request, id_):
    response = None
    try:
        if request.method == "POST":
            instance = Customer.objects.filter(id=id_).first()
            form = CustomerForm(request.POST or None, instance=instance)
            if form.is_valid():
                logging.info("Customer edited: {}".format(instance.company_name))
                form.save()
            else:
                logging.error("Customer cannot edit.")
            response = HttpResponseRedirect(request.path_info)
    except Exception as exception:
        logging.error("Exception occurred while editing customer: {}".format(str(exception)))
    finally:
        if not response:
            instance = Customer.objects.filter(id=id_).first()
            form = CustomerForm(instance=instance)
            data = {
                "title": "Customer | Edit",
                "customer_form": form,
            }
            response = render(request, "customer/edit.html", data)
        return response
