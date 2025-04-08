from rest_framework.routers import DefaultRouter
from .views import RegisterView,ProfileViewset,CardViewset
from django.urls import path,include

user = DefaultRouter()

user.register(r'auth', RegisterView, basename='auth')
user.register(r'profile', ProfileViewset, basename='profile')
user.register(r'card', CardViewset, basename='card')

urlpatterns = [
    path('', include(user.urls))
]