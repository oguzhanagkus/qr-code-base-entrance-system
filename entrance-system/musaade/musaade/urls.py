from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/entrance_system/login/')),
    path('admin/', admin.site.urls),
    path('entrance_system/', include('entrance_system.urls')),
    path('api/', include('api.urls'))
]
