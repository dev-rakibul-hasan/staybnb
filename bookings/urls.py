from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:listing_id>/', views.create_booking, name='create_booking'),
    path('pay/<int:booking_id>/', views.payment_page, name='payment_page'),
    path('pay/<int:booking_id>/process/', views.process_payment, name='process_payment'),
    path('guest/my-bookings/', views.guest_bookings, name='guest_bookings'),
    path('host/requests/', views.host_requests, name='host_requests'),
    path('host/requests/<int:booking_id>/accept/', views.accept_booking, name='accept_booking'),
    path('host/requests/<int:booking_id>/decline/', views.decline_booking, name='decline_booking'),
]
