import datetime
from email import message
from rest_framework.permissions import BasePermission

"""Adjust the permissions of the BookingsList and BookFlight so that only logged in users can access this view."""

"""Adjust the permissions of the BookingDetails, UpdateBooking and CancelBooking so that only an owner of the booking or staff can access the view."""


class IsOwner(BasePermission):
    message = "You must be the owner of this booking to perform this action."
    def has_object_permission(self, request, view, obj) :
        return request.user.is_staff or obj.user == request.user


"""Adjust the permissions of the UpdateBooking and CancelBooking so that the booking cannot be canceled or modified unless it's more than 3 days away.
"""
class IsNotTooSoon(BasePermission):
    message = "You cannot cancel or modify a booking before 3 days after the flight."
    def has_object_permission(self, request, view, obj):
        return obj.date >= datetime.date.today() + datetime.timedelta(days=3)