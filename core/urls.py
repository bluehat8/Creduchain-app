# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include

from apps.home import views  # add this

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("", include("apps.home.urls")),             # UI Kits Html files
    path('issue-credentials/', views.issue_credentials, name='issue_credentials'),
    path('verify-credentials/', views.verify_credentials, name='verify_credentials')
]
