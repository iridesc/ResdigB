from django.urls import path
from . import views


urlpatterns = [
    #user
    path('', views.home),
    path('api/', views.api),
 
]
