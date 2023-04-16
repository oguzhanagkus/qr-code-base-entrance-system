import csv
import base64
import datetime
import tempfile
import logging as log

import xlwt
import weasyprint
import pyqrcode

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from entrance_system.forms import ImportForm, PersonnelForm
from entrance_system.models import Personnel, Department
from entrance_system import utils

page = "/entrance_system/personnel/"


def view(request):
    import_form = ImportForm()
    personnel_form = PersonnelForm()
    personnel_list = Personnel.objects.all().order_by("id")
    data = {
        "title": "Personnel",
        "import_form": import_form,
        "personnel_form": personnel_form,
        "personnel_list": personnel_list,
    }
    return render(request, "personnel/main.html", data)


@csrf_exempt
def add(request):
    try:
        if request.method == "POST":
            form = PersonnelForm(request.POST)
            if form.is_valid():
                form_data = form.cleaned_data
                form.save()
                log.info("New personnel added: {} {}".format(form_data["first_name"], form_data["last_name"]))
                messages.info(request, "Personnel added.")
            else:
                log.warning("Submitted form is not valid.")
                messages.warning(request, "Submitted form is not valid.")
    except Exception as exception:
        log.error("Exception occurred while adding personnel: {}".format(str(exception)))
        messages.error(request, "Error occurred while adding.")
    finally:
        return redirect(page)


@csrf_exempt
def edit(request, id_):
    response = None
    try:
        if request.method == "POST":
            instance = Personnel.objects.filter(id=id_).first()
            form = PersonnelForm(request.POST or None, instance=instance)
            if form.is_valid():
                log.info("Personnel edited: {} {}".format(instance.first_name, instance.last_name))
                form.save()
            else:
                log.error("Personnel cannot edit.")
            response = HttpResponseRedirect(request.path_info)
    except Exception as exception:
        log.error("Exception occurred while editing personnel: {}".format(str(exception)))
    finally:
        if not response:
            instance = Personnel.objects.filter(id=id_).first()
            form = PersonnelForm(instance=instance)
            data = {
                "title": "Personnel | Edit",
                "personnel_form": form,
            }
            response = render(request, "personnel/edit.html", data)
        return response


@csrf_exempt
def delete(request, id_):
    try:
        personnel = Personnel.objects.filter(id=id_).first()
        personnel.delete()
        log.info("Personnel deleted: {} {}".format(personnel.first_name, personnel.last_name))
        messages.info(request, "Personnel deleted.")
    except Exception as exception:
        log.error("Exception occurred while deleting personnel: {}".format(str(exception)))
        messages.error(request, "Error occurred while deleting.")
    finally:
        return redirect(page)


def change_status(request, id_):
    try:
        personnel = Personnel.objects.filter(id=id_).first()
        personnel.active = not personnel.active
        personnel.save()
        log.info(
            "Personnel status changed: {} {} -> {}".format(personnel.first_name, personnel.last_name, personnel.active))
        messages.info(request, "Personnel status changed.")
    except Exception as exception:
        log.error("Exception occurred while changing personnel status: {}".format(str(exception)))
        messages.error(request, "Error occurred while changing status.")
    finally:
        return redirect(page)


def send_qr_code(request, id_):
    try:
        personnel = Personnel.objects.filter(id=id_).first()
        send_mail(personnel)
        messages.info(request, "QR code sent successfully.")
    except Exception as exception:
        messages.error(request, "Error occurred while sending QR code.")
    finally:
        return redirect(request.META.get('HTTP_REFERER', '/'))


def renew_qr_code(request, id_):
    try:
        personnel = Personnel.objects.filter(id=id_).first()
        personnel.secret_token = utils.secret_token()
        personnel.generate_qr_code_data()
        personnel.save()
        log.info("Personnel QR code renewed: {} {}".format(personnel.first_name, personnel.last_name))
        messages.info(request, "Personnel QR code renewed.")
    except Exception as exception:
        log.error("Exception occurred while renewing QR code: {}".format(str(exception)))
        messages.error(request, "Error occurred while renewing QR code.")
    finally:
        return redirect(request.META.get('HTTP_REFERER', '/'))


@csrf_exempt
def import_csv(request):
    try:
        if request.method == "POST":
            form = ImportForm(request.POST, request.FILES)
            if form.is_valid():
                fs = FileSystemStorage()
                csv_file = form.cleaned_data["csv_file"]
                file_name = fs.save(csv_file.name, csv_file)
                with open(file_name, "r") as file:
                    saved = 0
                    failed = 0
                    reader = csv.DictReader(file)
                    for row in reader:
                        try:
                            personnel = Personnel(
                                national_id=row["National ID"],
                                first_name=row["First Name"],
                                last_name=row["Last Name"],
                                email=row["Email"],
                                department=Department.objects.get(name=row["Department"]),
                                active=True if row["Active"].lower() == "true" else False
                            )
                            personnel.save()
                            saved += 1
                            log.info("New personnel saved: {} {}".format(personnel.first_name, personnel.last_name))
                            # send_mail(personnel)
                        except Exception as exception:
                            failed += 1
                            log.warning("Error occurred while saving personnel ({} {}): {}".format(row["First Name"],
                                                                                                   row["Last Name"],
                                                                                                   str(exception)))
                fs.delete(file_name)
                log.info("Personnel importing completed. Saved: {} - Failed: {}".format(saved, failed))
                messages.info(request, "Personnel importing completed. Saved: {} - Failed: {}".format(saved, failed))
            else:
                log.warning("File is not a valid CSV file.")
                messages.warning(request, "File is not a valid CSV file.")
    except Exception as exception:
        log.error("Exception occurred while importing personnel CSV: {}".format(str(exception)))
        messages.error(request, "Error occurred while importing.")
    finally:
        return redirect(page)


def export_csv(request):
    response = None
    try:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=personnel_{}.csv".format(datetime.datetime.now())

        column_names = Personnel.get_printable_column_names()
        data = Personnel.objects.all().order_by("id")

        writer = csv.writer(response)
        writer.writerow(column_names)
        for personnel in data:
            writer.writerow(personnel.get_printable_data())
    except Exception as exception:
        log.error("Error occurred while exporting as CSV: {}".format(str(exception)))
        messages.error(request, "Error occurred while exporting.")
        response = redirect(page)
    finally:
        return response


def export_excel(request):
    response = None
    try:
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = "attachment; filename=personnel_{}.xls".format(datetime.datetime.now())

        column_names = Personnel.get_printable_column_names()
        data = Personnel.objects.all().order_by("id")

        workbook = xlwt.Workbook(encoding="utf-8")
        worksheet = workbook.add_sheet("Personnel")

        row = 0
        for column in range(len(column_names)):
            worksheet.write(row, column, column_names[column])
        for personnel in data:
            row += 1
            personnel_data = personnel.get_printable_data()
            for column in range(len(column_names)):
                worksheet.write(row, column, str(personnel_data[column]))
        workbook.save(response)
    except Exception as exception:
        log.error("Error occurred while exporting as excel: {}".format(str(exception)))
        messages.error(request, "Error occurred while exporting.")
        response = redirect(page)
    finally:
        return response


def export_pdf(request):
    response = None
    try:
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "inline; attachment; filename=personnel_{}.pdf".format(
            datetime.datetime.now())
        response["Content-Transfer-Encoding"] = "binary"

        column_names = Personnel.get_printable_column_names()
        data = Personnel.objects.all().order_by("id")

        html_string = render_to_string("personnel/export.html", {"column_names": column_names, "data": data})
        html_string = weasyprint.HTML(string=html_string)
        result = html_string.write_pdf()

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, "rb")
            response.write(output.read())
    except Exception as exception:
        log.error("Error occurred while exporting as PDF: {}".format(str(exception)))
        messages.error(request, "Error occurred while exporting.")
        response = redirect(page)
    finally:
        return response


def send_mail(personnel):
    try:
        filename = "{}_{}.png".format(personnel.first_name, personnel.last_name).lower()
        mimetype = "image/png"
        qr_code = pyqrcode.create(personnel.qr_code_data + "#")
        content = qr_code.png_as_base64_str(scale=25)
        content = base64.b64decode(content)

        mail = EmailMessage("QR Code Information", "You can use this QR code at entrance locations.",
                            "Müsaade Entrance System <{}>".format(settings.EMAIL_HOST_USER), [personnel.email])
        mail.attach(filename, content, mimetype)
        mail.send()

        log.info("QR code sent successfully: {} {}".format(personnel.first_name, personnel.last_name))
    except Exception as exception:
        log.error("Exception occurred while sending QR code: {}".format(str(exception)))
        raise exception
