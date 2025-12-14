from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone
from django.db.models import Q

from accounts.models import User
from listing.models import Listing
from .models import Booking

# CREATE booking (updated) — after creation redirect to payment page
def create_booking(request, listing_id):
    if "user_id" not in request.session:
        return HttpResponse("Please login as a guest to book.")

    user = User.objects.get(id=request.session["user_id"])

    if user.role != "guest":
        return HttpResponse("Only guests can book properties.")

    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == "POST":
        check_in_str = request.POST.get("check_in")
        check_out_str = request.POST.get("check_out")

        check_in = datetime.strptime(check_in_str, "%Y-%m-%d").date()
        check_out = datetime.strptime(check_out_str, "%Y-%m-%d").date()

        if check_out <= check_in:
            return HttpResponse("Check-out must be after check-in.")

        nights = (check_out - check_in).days
        total_price = nights * listing.price_per_night

        booking = Booking.objects.create(
            guest=user,
            listing=listing,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price,
            status='pending',
            is_paid=False
        )

        return redirect('payment_page', booking_id=booking.id)

    return HttpResponse("Invalid request.")


# Payment page (simple simulation)
def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if "user_id" not in request.session or request.session["user_id"] != booking.guest.id:
        return HttpResponse("Access denied.")

    return render(request, "payment_page.html", {"booking": booking})


# Process payment (simulate success/fail)
def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if "user_id" not in request.session or request.session["user_id"] != booking.guest.id:
        return HttpResponse("Access denied.")

    if request.method == "POST":
        card_number = request.POST.get("card_number", "")
        card_number_digits = ''.join(filter(str.isdigit, card_number))
        success = False
        if card_number_digits:
            last_digit = int(card_number_digits[-1])
            success = (last_digit % 2 == 0)

        if success:
            booking.is_paid = True
            booking.save()
            return render(request, "payment_result.html", {"success": True, "booking": booking})
        else:
            return render(request, "payment_result.html", {"success": False, "booking": booking})

    return HttpResponse("Invalid request.")


# Guest bookings (unchanged)
def guest_bookings(request):
    if "user_id" not in request.session:
        return HttpResponse("Login Required")

    user = User.objects.get(id=request.session["user_id"])

    if user.role != "guest":
        return HttpResponse("Only guests can view their bookings")

    bookings = Booking.objects.filter(guest=user).order_by('-created_at')

    return render(request, "guest_bookings.html", {"bookings": bookings, "user": user})


# Host requests (unchanged)
def host_requests(request):
    if "user_id" not in request.session:
        return HttpResponse("Login Required")

    user = User.objects.get(id=request.session["user_id"])

    if user.role != "host":
        return HttpResponse("Only hosts can view their bookings")

    bookings = Booking.objects.filter(listing__host=user, status='pending').order_by('-created_at')

    return render(request, "host_requests.html", {"bookings": bookings, "user": user})


# Host accept with conflict check
def accept_booking(request, booking_id):
    if "user_id" not in request.session:
        return HttpResponse("Login Required")

    user = User.objects.get(id=request.session["user_id"])

    if user.role != "host":
        return HttpResponse("Only hosts can accept bookings")

    booking = get_object_or_404(Booking, id=booking_id, listing__host=user)

    if not booking.is_paid:
        return HttpResponse("Cannot accept booking — guest hasn't paid yet.")

    conflict_qs = Booking.objects.filter(
        listing=booking.listing,
        status='confirmed'
    ).filter(
        check_in__lt=booking.check_out,
        check_out__gt=booking.check_in
    )

    if conflict_qs.exists():
        return HttpResponse("Cannot accept: there is a conflicting confirmed booking for these dates.")

    if request.method == "POST":
        booking.status = 'confirmed'
        booking.save()
        return redirect('host_requests')

    return render(request, "confirm_accept.html", {"booking": booking})


# Host decline (unchanged)
def decline_booking(request, booking_id):
    if "user_id" not in request.session:
        return HttpResponse("Login Required")

    user = User.objects.get(id=request.session["user_id"])

    if user.role != "host":
        return HttpResponse("Only hosts can decline bookings")

    booking = get_object_or_404(Booking, id=booking_id, listing__host=user)

    if request.method == "POST":
        booking.status = 'cancelled'
        booking.save()
        return redirect('host_requests')

    return render(request, "confirm_decline.html", {"booking": booking})    

    