"""
URL configuration for csieCampProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from csieCampApp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_app, name='login'),
    path("logout/", views.logout_app, name="logout"),
    path('admin_control/', views.control, name='control'),
    path('admin_log/', views.admin_log, name='admin_log'),
    path('detail/', views.detail, name='detail'),
    path('team_log/', views.team_log, name='team_log'),
    path('bingorules/', views.bingo, name='bingo'),
    path('casinorules/', views.casino, name='casino'),
    path('startbingo/', views.bingostart, name='start'),
    path('resetgame/', views.resetGamestatus, name='resetgame'),
    path('"delete/<int:record_id>/"', views.delete_record, name='delete'),
    #path('foradmin/', admin.site.urls),
    path('ftgyhj8y2er/', views.create_user, name='create'),
    path('w3e45r6tyuh/', views.password_change, name='change'),
]
