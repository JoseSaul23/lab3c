from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('iniciativas/', views.proposals, name='iniciativas'),
    path('iniciativa/<str:pk>/', views.proposal, name='iniciativa'),
]