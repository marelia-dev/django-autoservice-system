from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/autoservice/', permanent=True)),
    path('autoservice/', include('autoservice.urls')),
    path('order/', include('autoservice.urls')),
]