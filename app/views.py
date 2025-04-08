from rest_framework.viewsets import ViewSet,ModelViewSet
from .serializers import RegisterParkingSerializer,BookingSerializer,BookingDetailSerializer,HistorySerializer
from .models import Parking,Booking,History
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from rest_framework.decorators import action



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
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return History.objects.filter(user=self.request.user)