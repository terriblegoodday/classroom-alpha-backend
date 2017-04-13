"""MathGen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from mathgenapp import views as mathgenapp
from django.views.generic import TemplateView
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', mathgenapp.index),
    url(r'^getTasks/', mathgenapp.api_getTasks),
    url(r'^getAvailableGenerators/', mathgenapp.api_getAvailableGenerators),
    url(r'^reviewAnswers', mathgenapp.api_reviewAnswers),
    url(r'^stats/', mathgenapp.api_getStatistics)
]
