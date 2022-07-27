import datetime
from time import perf_counter

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner, IsNotTooSoon

from flights import serializers
from flights.models import Booking, Flight


class FlightsList(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = serializers.FlightSerializer
    permission_classes = [IsAuthenticated]


class BookingsList(generics.ListAPIView):
    serializer_class = serializers.BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = datetime.date.today()
        return Booking.objects.filter(user=self.request.user, date__gte=today)


class BookingDetails(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = serializers.BookingDetailsSerializer
    lookup_field = "id"
    lookup_url_kwarg = "booking_id"
    permission_classes = [IsOwner, IsNotTooSoon]
 


class UpdateBooking(generics.RetrieveUpdateAPIView):
    queryset = Booking.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "booking_id"
    permission_classes = [IsOwner, IsNotTooSoon]


    def get_serializer_class(self):
        if self.request.user.is_staff:
            return serializers.AdminUpdateBookingSerializer

        return serializers.UpdateBookingSerializer


class CancelBooking(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "booking_id"
    permission_classes = [IsOwner]


class BookFlight(generics.CreateAPIView):
    serializer_class = serializers.AdminUpdateBookingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, flight_id=self.kwargs["flight_id"])


class Register(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer
