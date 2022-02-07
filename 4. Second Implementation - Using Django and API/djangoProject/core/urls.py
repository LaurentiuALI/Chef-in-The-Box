from django.urls import path
from core import views

urlpatterns = [
    path( 'files/', views.file_list ),
    path( 'files/<str:cat>/', views.file_cat ),
    path( 'files/<str:sdb>/<str:fn>/', views.file_detail ),
]