from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from mongo_client import mongo_db
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta


def home(request):
    return  HttpResponse("Hello Team ZeorsEdge, The airbnb is working fine.")
def signup_page(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        role = request.POST.get('role')

        hashed_pass  = make_password(password)

        try:
            User.objects.create(
                full_name = full_name,
                email = email,
                phone = phone,
                password = hashed_pass,
                role = role
            )

            #mongodb
            users_collection = mongo_db["users"]
            users_collection.insert_one({
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "password": hashed_pass,
                "role": role
            })

            return redirect('accounts:login')
        except Exception as e:
            if "UNIQUE constraint failed" in str(e) or "duplicate key" in str(e):
                form = {} # You might want to pass the form data back, but for now let's just show the error
                return render(request, 'signup.html', {'message': "Email or Phone already exists."})
            else:
                return HttpResponse(f"An error occurred: {e}")
    return render (request, 'signup.html')



def login_page(request):
    message= ""

    if request.method == 'POST':
        identifier  = request.POST.get('identifier')
        password = request.POST.get('password')

        try:
            user = User.objects.get(Q(email=identifier) | Q(phone=identifier))
        except User.DoesNotExist:
            message = "Invalid email/phone or password"
            return render(request,'login.html', {'message': message})
        
        now = timezone.now()
        if user.is_locked and user.lock_until > now:
            remaining = (user.lock_until - now).seconds
            message = f"Account Locked. Try again after {remaining} seconds."
            return render(request, 'login.html', {'message': message})
        
        if check_password(password, user.password):
            user.failed_attempts = 0
            user.is_locked = False
            user.lock_until = None
            user.save()

            request.session['user_id']  = user.id
            request.session['user_role'] = user.role

            if user.role == 'host':
                return redirect('accounts:host_dashboard')
            else: 
                return redirect('accounts:guest_dashboard')
            
        else:
            user.failed_attempts +=1

            if user.failed_attempts >= 3:
                user.is_locked = True
                user.lock_until = now + timedelta(minutes=2)

            user.save()
            
            message = "Invalid email/phone or password."

    return render(request, "login.html", {"message": message})



def guest_dashboard(request):
    return HttpResponse("Guest Dashboard ----- Logged in as Guest")

def host_dashboard(request):
    return redirect("listing:host_dashboard")

def home(request):
    return render(request, "home.html")

def logout_view(request):
    request.session.flush()
    return redirect('home')

    






