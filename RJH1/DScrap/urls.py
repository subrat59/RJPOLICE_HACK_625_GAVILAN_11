from django.urls import path
from . import views

urlpatterns = [
    path('scrape/',views.DWeb_Scraper,name='DWeb_Scraper')
]