from django.db import models

class Parking(models.Model):
    
    class TypeEnum(models.TextChoices):
        FREE = 'free'
        PAID = 'paid'
    
    owner = models.ForeignKey("user.CustomUser",on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=20,choices=TypeEnum.choices, default=TypeEnum.PAID)
    address = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    latitude = models.FloatField()
    longitude = models.FloatField() 
    price = models.FloatField()

class Floor(models.Model):
    parking = models.ForeignKey(Parking,on_delete=models.CASCADE)
    number = models.IntegerField()
    suffix = models.CharField(max_length=2)
    
class Slot(models.Model):
    floor = models.ForeignKey(Floor,on_delete=models.CASCADE)
    number = models.IntegerField()
    status = models.BooleanField(default=False)

class Booking(models.Model):

    class StatusEnum(models.TextChoices):
        BOOKED = 'booked'
        ARRIVED = 'arrived'
        LEFT = 'left'
        REJECTED = 'rejected'

    car_number = models.CharField(max_length=100)
    slot = models.ForeignKey(Slot,on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=StatusEnum.choices,default=StatusEnum.BOOKED)
    booked_time = models.DateTimeField(auto_now_add=True)
    arrived_time = models.DateTimeField(blank=True,null=True)
    left_time = models.DateTimeField(blank=True,null=True)
    rejected_time = models.DateTimeField(blank=True,null=True)


class History(models.Model):
    user = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE)
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.SET_NULL, null=True)
    arrived_time = models.DateTimeField(blank=True,null=True)
    left_time = models.DateTimeField(blank=True,null=True)
