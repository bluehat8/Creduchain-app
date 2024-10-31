# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home.views import views
from apps.home.views import credentials, pinata_service

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('emit-credentials', credentials.credentials_management, name='emit_credentials'),
    path('emit-credentials/', credentials.credentials_management, name='emit-credentials_no_slash'),
    path('upload_to_pinata/', pinata_service.upload_to_pinata, name='upload_to_pinata'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]
