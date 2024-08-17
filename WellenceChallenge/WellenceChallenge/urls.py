"""
URL configuration for WellenceChallenge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from WellenceApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing_page'),
    path('DataEntry', views.data_entry, name='data_entry'),
    path('DashBoard', views.dash_board, name='dash_board'),
    path('password_verify_link', views.password_verify_link, name='password_verify_link'),
    path('password_verify', views.password_verify, name='password_verify'),
    path('DataEntry_add', views.data_entry_add, name='data_entry_add'),
]



