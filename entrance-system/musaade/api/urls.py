from django.urls import path

from api import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('make_query/', views.make_query),
    path('login/', obtain_auth_token),
    path('location/', views.LocationsView.as_view()),
    path('activity/', views.ActivityView.as_view()),
]
