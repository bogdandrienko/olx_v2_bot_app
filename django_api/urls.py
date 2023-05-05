from django.urls import path
from django_api import views


urlpatterns = [
    path('search/', views.search_f),
    path('ads/', views.ads_f),
]
