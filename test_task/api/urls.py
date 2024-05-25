from django.urls import path
from .views import *

urlpatterns = [
    path('sections', list_create_sections_view),
    path('sections/<str:title>', rud_sections_view),
    path('student/sections', list_create_usersection_view),
    path('student/sections/<str:section>', rd_usersection_view),
]