from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('manual_scrape/',views.DWeb_Scraper,name='DWeb_Scraper'),
    path('auto_scrape/',views.auto_Scraper,name='auto_Scraper'),
    path('search_view/',views.search_view,name='search_view'),
    path('result_auto/',views.result_auto,name='result_auto'),
    path('',views.index_DWeb,name='index_DWeb'),
    path('scrap/',views.scrapimage,name='scrapimage'),
    path('scrapss/',views.preview_screenshot,name='preview_screenshot'),
    path('viewarchieves/',views.view_archives,name='viewarchieves'),
    path('viewhistory/',views.view_archives_dashboard,name='view_archives_dashboard')
]
    # path('connect_vpn/',views.connect_vpn,name='connect_vpn')