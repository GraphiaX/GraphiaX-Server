from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello_view, name='hello'),
    path('react/', views.project_structure_view, name='react'),
]
