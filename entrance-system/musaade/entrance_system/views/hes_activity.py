import csv
import datetime
import tempfile
import logging as log

import xlwt
import weasyprint

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from entrance_system.models import HESActivity

page = "/entrance_system/hes_activity/"


def view(request):
    activities = HESActivity.objects.all().order_by("-id")
    data = {
        "title": "HES Activity",
        "activities": activities,
    }
    return render(request, "hes_activity/main.html", data)


def export_csv(request):
    response = None
    try:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=hes_activity_{}.csv".format(
            datetime.datetime.now())

        column_names = HESActivity.get_printable_column_names()
        data = HESActivity.objects.all().order_by("-id")

        writer = csv.writer(response)
        writer.writerow(column_names)
        for activity in data:
            writer.writerow(activity.get_printable_data())
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
        response["Content-Disposition"] = "attachment; filename=hes_activity_{}.xls".format(
            datetime.datetime.now())

        column_names = HESActivity.get_printable_column_names()
        data = HESActivity.objects.all().order_by("-id")

        workbook = xlwt.Workbook(encoding="utf-8")
        worksheet = workbook.add_sheet("HES Activity")

        row = 0
        for column in range(len(column_names)):
            worksheet.write(row, column, column_names[column])
        for activity in data:
            row += 1
            activity_data = activity.get_printable_data()
            for column in range(len(column_names)):
                worksheet.write(row, column, str(activity_data[column]))
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
        response["Content-Disposition"] = "inline; attachment; filename=hes_activity_{}.pdf".format(
            datetime.datetime.now())
        response["Content-Transfer-Encoding"] = "binary"

        column_names = HESActivity.get_printable_column_names()
        data = HESActivity.objects.all().order_by("-id")

        html_string = render_to_string("hes_activity/export.html", {"column_names": column_names, "data": data})
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

