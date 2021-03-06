from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='panels-home'),
    path('about/', views.about, name='panels-about'),
    path('pplr', views.pplr_compare, name='panels-pplr'),
    path('pntDef', views.pntDef_compare, name='panels-pntDef'),
    path('trndDef', views.trndDef_compare, name='panels-trndDef'),
    path('ppcl', views.ppcl_compare, name='panels-ppcl'),
    path('pntSrtr', views.pntSrtr_compare, name='panels-pntSrtr'),
    path('P2BpntDef', views.P2BpntDef_compare, name='panels-P2BpntDef'),
]
