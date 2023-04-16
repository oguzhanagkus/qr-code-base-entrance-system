from django.urls import path

from entrance_system.views import *

urlpatterns = [
    path('', auth.user_login),
    path('login/', auth.user_login),
    path('logout/', auth.user_logout),
    path('dashboard/', dashboard.view),

    path('personnel/', personnel.view),
    path('personnel/add/', personnel.add),
    path('personnel/delete/<int:id_>/', personnel.delete),
    path('personnel/edit/<int:id_>/', personnel.edit),
    path('personnel/edit/<int:id_>/change_status/', personnel.change_status),
    path('personnel/edit/<int:id_>/send_qr_code/', personnel.send_qr_code),
    path('personnel/edit/<int:id_>/renew_qr_code/', personnel.renew_qr_code),
    path('personnel/import/csv/', personnel.import_csv),
    path('personnel/export/csv/', personnel.export_csv),
    path('personnel/export/excel/', personnel.export_excel),
    path('personnel/export/pdf/', personnel.export_pdf),

    path('departments/', department.view),
    path('departments/add/', department.add),
    path('departments/delete/<int:id_>/', department.delete),
    path('departments/edit/<int:id_>/', department.edit),

    path('locations/', location.view),
    path('locations/add/', location.add),
    path('locations/delete/<int:id_>/', location.delete),
    path('locations/edit/<int:id_>/', location.edit),
    path('locations/edit/<int:id_>/change_status', location.change_status),
    path('locations/edit/<int:id_>/download_qr_code', location.download_qr_code),

    path('access_points/', access_point.view),
    path('access_points/add/', access_point.add),
    path('access_points/delete/<int:id_>/', access_point.delete),
    path('access_points/edit/<int:id_>/', access_point.edit),

    path('personnel_activity/', personnel_activity.view),
    path('personnel_activity/export/csv/', personnel_activity.export_csv),
    path('personnel_activity/export/excel/', personnel_activity.export_excel),
    path('personnel_activity/export/pdf/', personnel_activity.export_pdf),

    path('hes_activity/', hes_activity.view),
    path('hes_activity/export/csv/', hes_activity.export_csv),
    path('hes_activity/export/excel/', hes_activity.export_excel),
    path('hes_activity/export/pdf/', hes_activity.export_pdf),

    path('settings/', user_settings.view)
]
