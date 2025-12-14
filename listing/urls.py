from django.urls import path
from . import views

app_name = 'listing'

urlpatterns = [
    path('add/', views.host_and_listing, name = 'add_listing'),
    path('dashboard/', views.host_dashboard, name = "host_dashboard"),
    path('edit/<int:listing_id>/', views.edit_listing, name = 'edit_listing'),
    path('delete/<int:listing_id>/', views.delete_listing, name = 'delete_listing'),
    path('search/', views.search_listing, name = 'search_listing'),
    path('<int:listing_id>/', views.listing_detail, name = 'listing_detail'),
    
]
