# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home.views import views
from apps.home.views import credentials, pinata_service
from apps.home import Notifications_Endpoints

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('emit-credentials', credentials.credentials_management, name='emit_credentials'),
    path('emit-credentials/', credentials.credentials_management, name='emit-credentials_no_slash'),
    path('upload_to_pinata/', pinata_service.upload_to_pinata, name='upload_to_pinata'),

    #API's
    path('get_notifications/', Notifications_Endpoints.get_notifications, name='get_notifications'),
    path('get_notifications_template/', Notifications_Endpoints.get_notifications_items_template, name='get_notifications_template'),


    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

    

]
