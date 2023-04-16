import datetime
from django.shortcuts import render


from entrance_system.models import Personnel, Location, PersonnelActivity, HESActivity


def view(request):
    data = {
        "title": "Dashboard",
        "personnel": {},
        "location": {},
        "personnel_activity": {},
        "hes_activity": {},
    }

    personnel_list = Personnel.objects.all()
    location_list = Location.objects.all()
    personnel_activity_list = PersonnelActivity.objects.all().filter(time__gte=datetime.date.today())
    hes_activity_list = HESActivity.objects.all().filter(time__gte=datetime.date.today())

    data['personnel']["active"] = personnel_list.filter(active=True).count()
    data['personnel']["total"] = personnel_list.count()
    if data['personnel']["total"] > 0:
        data['personnel']["rate"] = data['personnel']["active"] / data['personnel']["total"] * 100
    else:
        data['personnel']["rate"] = 0

    data['location']["active"] = location_list.filter(active=True).count()
    data['location']["total"] = location_list.count()
    if data['location']["total"] > 0:
        data['location']["rate"] = data['location']["active"] / data['location']["total"] * 100
    else:
        data['location']["rate"] = 0

    data['personnel_activity']["success"] = personnel_activity_list.filter(result=True).count()
    data['personnel_activity']["total"] = personnel_activity_list.count()
    if data['personnel_activity']["total"] > 0:
        data['personnel_activity']["rate"] = data['personnel_activity']["success"] / data['personnel_activity']["total"] * 100
    else:
        data['personnel_activity']["rate"] = 0

    data['hes_activity']["success"] = hes_activity_list.filter(result=True).count()
    data['hes_activity']["total"] = hes_activity_list.count()
    print(data['hes_activity']["total"])
    if data['hes_activity']["total"] > 0:
        data['hes_activity']["rate"] = data['hes_activity']["success"] / data['hes_activity']["total"] * 100
    else:
        data['hes_activity']["rate"] = 0

    return render(request, "dashboard.html", data)

