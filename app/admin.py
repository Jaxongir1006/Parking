from django.contrib import admin
from .models import Parking,Slot,Floor,Booking,History

admin.site.register(Parking)
admin.site.register(Slot)
admin.site.register(Floor)
admin.site.register(Booking)
admin.site.register(History)