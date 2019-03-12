from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('keyboard/', include("meals.urls")),
    path('crawler/', include("meals.urls"))
]
