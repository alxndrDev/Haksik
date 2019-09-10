from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "index"),
    path('crawler', views.crawler),
    path('today/', views.today),
    path('tomorrow/',views.tomorrow),
    #path('deleteDB/', views.deleteDB)
    path("available/", views.available)
]