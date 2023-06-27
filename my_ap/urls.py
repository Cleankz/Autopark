"""my_ap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from autopark import views as user_views
from autopark.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autopark/', include('autopark.urls')),
    path('', RedirectView.as_view(url='/autopark/', permanent=True)),
    path('api/v1/vehiclelist/view/',VehicleAPIView.as_view()),
    path('api/v1/vehiclelist/<int:pk>/', VehicleAPIDetailView.as_view()),
    path('api/v1/vehiclelist/list/', VehicleAPIList.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),


]
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# <!--                    <a class="nav-item nav-link" href="{% url 'register' %}">Регистрация</a>-->
