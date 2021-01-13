from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='panels-home'),
    path('about/', views.about, name='panels-about'),
    path('pplr', views.pplr_compare, name='panels-pplr'),
    path('pntDef', views.pntDef_compare, name='panels-pntDef'),
    path('trndDef', views.trndDef_compare, name='panels-trndDef'),
]
