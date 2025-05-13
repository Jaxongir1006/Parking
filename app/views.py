from rest_framework.viewsets import ViewSet,ModelViewSet
from .serializers import RegisterParkingSerializer,BookingSerializer,BookingDetailSerializer,HistorySerializer,ParkingShortSeraizer,ParkingDetailSeraizer
from .models import Parking,Booking,History
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from rest_framework.decorators import action
from .tasks import test_task
from django.core.cache import cache
from django.db.models import Count,Q

class RegisterParkingViewset(ModelViewSet):

    serializer_class = RegisterParkingSerializer
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Parking.objects.filter(owner = self.request.user)
    
    def perform_create(self, serializer):
        data = serializer.save(owner = self.request.user)
        return data
    
class BookingViewset(ViewSet):

    @action(methods=['POST'],detail=False)
    def book(self, request, *args, **kwargs):
        serializer = BookingSerializer(data = request.data, context = {'request':request})

        serializer.is_valid(raise_exception=True)
        data = serializer.save(action = 'book')
        ss = BookingDetailSerializer(data)
        return Response(ss.data)
    
    @action(methods=['POST'],detail=False)
    def arrive(self, request, *args, **kwargs):
        user = request.user

        car_number = request.data.get('car_number')
        slot_id = request.data.get('slot_id')

        if user.is_authenticated:
            car_number = user.car_number
        if not car_number or not slot_id:
            return Response({'error':'car_number bn slot_id kerak'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            booking = Booking.objects.get(car_number=car_number,slot_id=slot_id)
        except Booking.DoesNotExist:
            return Response({'error':'booking mavjud emas'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = Booking.StatusEnum.ARRIVED
        booking.arrived_time = now()
        print(booking.status)
        booking.save()
        serializer = BookingDetailSerializer(booking)
        return Response(serializer.data)


    @action(methods=['POST'],detail=False)
    def left(self, request, *args, **kwargs):
        user = request.user

        car_number = request.data.get('car_number')
        slot_id = request.data.get('slot_id')

        if user.is_authenticated:
            car_number = user.car_number
        if not car_number or not slot_id:
            return Response({'error':'car_number bn slot_id kerak'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            booking = Booking.objects.get(car_number=car_number,slot_id=slot_id)
        except Booking.DoesNotExist:
            return Response({'error':'booking mavjud emas'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = Booking.StatusEnum.LEFT
        booking.arrived_time = now()
        booking.slot.status = False
        print(booking.status)
        booking.save()
        serializer = BookingDetailSerializer(booking)
        return Response(serializer.data)

    @action(methods=['POST'],detail=False)
    def reject(self, request, *args, **kwargs):
        user = request.user

        car_number = request.data.get('car_number')
        slot_id = request.data.get('slot_id')

        if user.is_authenticated:
            car_number = user.car_number
        if not car_number or not slot_id:
            return Response({'error':'car_number bn slot_id kerak'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            booking = Booking.objects.get(car_number=car_number,slot_id=slot_id)
        except Booking.DoesNotExist:
            return Response({'error':'booking mavjud emas'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = Booking.StatusEnum.REJECTED
        booking.arrived_time = now()
        print(booking.status)
        booking.slot.status = False
        booking.save()
        serializer = BookingDetailSerializer(booking)
        return Response(serializer.data)


class HistoryViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = HistorySerializer
    # permission_classes = [IsAuthenticated]
    def get_queryset(self):
        test_task()
        return History.objects.filter(user=self.request.user)

class ParkingViewSet(ViewSet):
    
    def list(self,request):

        parking_data = cache.get('parking_data',None)
        
        test_task()

        if not parking_data:
            parkings = Parking.objects.all()
            serializer = ParkingShortSeraizer(parkings,many = True)
            parking_data = serializer.data
            cache.set('parking_data',parking_data,timeout=600)
            print("db")
        else:
            print("cache")
        return Response(parking_data)

    @action(methods=['POST'],detail=False)
    def parking_detail(self,request,*args,**kwargs):
        parking_id = request.data.get('parking_id',None)
        parking = Parking.objects.annotate(floor_count = Count('floors',distinct=True),free_slot = Count("floors__slot", filter=Q(floors__slot__status=False))).get(id = parking_id)
        serializer = ParkingDetailSeraizer(parking)
        return Response(serializer.data)