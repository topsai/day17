"""day17 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from hostmanager import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login', views.login),
    url(r'^index$', views.index),
    url(r'^exit', views.login_off),
    url(r'^add_host', views.add_host),
    url(r'^add_user', views.add_user),
    url(r'^host_info', views.host_info),
    url(r'^host_del', views.host_del),
    url(r'^host_edit', views.host_edit),
    # url(r'^index-(\d)-(\d).html', views.test),

]
