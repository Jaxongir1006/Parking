from rest_framework.routers import DefaultRouter
from .views import RegisterParkingViewset,BookingViewset,HistoryViewSet
from django.urls import path,include

app = DefaultRouter()

app.register(r'register_parking', RegisterParkingViewset, basename='register_parking')
app.register(r'booking', BookingViewset, basename='booking')
app.register(r'history', HistoryViewSet, basename='history')

urlpatterns = [
    path('', include(app.urls))
]