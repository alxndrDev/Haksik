from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "index"),
    path('keyboard/', views.keyboard),
    path('crawler', views.crawler),
    path('today/', views.today),
    path('tomorrow/',views.tomorrow),
    path('deleteDB/', views.deleteDB)
]