from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_page, name= 'signup'),
    path('login/', views.login_page, name = 'login'),
    path('guest_dashboard/', views.guest_dashboard, name = 'guest_dashboard'),
    path('host_dashboard/', views.host_dashboard, name = 'host_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    
]