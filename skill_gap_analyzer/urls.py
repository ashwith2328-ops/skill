"""
URL configuration for Placement-Oriented Skill Gap Analyzer.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('skill_gap.urls')),
]
