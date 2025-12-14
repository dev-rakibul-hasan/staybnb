from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Listing
from accounts.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q


def host_and_listing(request):
    if 'user_id' not in request.session:
        return redirect('accounts:login')
    
    user = User.objects.get(id = request.session['user_id'])

    if user.role != "host":
        return HttpResponse("Only hosts can add listings")
    
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        price = request.POST.get('price')
        guests = request.POST.get('guests')
        image = request.FILES.get('image')



        Listing.objects.create(
            host= user,
            title = title,
            description = description,
            address = address,
            city = city,
            country = country,
            price_per_night = price,
            max_guests = guests,
            image = image
        )

        return redirect("listing:host_dashboard")
    
    return render(request, "add_listing.html")
    

def host_dashboard(request):
    if 'user_id' not in request.session:
        return HttpResponse("Login required.")
    
    user = User.objects.get(id = request.session["user_id"])

    if user.role != "host":
        return HttpResponse("Only hosts can access this page")  
    
    listings = Listing.objects.filter(host = user)

    return render(request, "host_dashboard.html", {"listings": listings, "user": user})

def edit_listing(request, listing_id):
    if "user_id" not in request.session:
        return HttpResponse("Login required.")
    
    user = User.objects.get(id = request.session['user_id'])

    if user.role != "host":
        return HttpResponse("Only hosts can edit listings")
    
    listing = get_object_or_404(Listing, id = listing_id, host = user)

    if request.method == "POST":
        listing.title = request.POST.get('title')
        listing.description = request.POST.get('description')
        listing.address = request.POST.get('address')
        listing.city = request.POST.get('city')
        listing.country = request.POST.get('country')
        listing.price_per_night = request.POST.get('price')
        listing.max_guests = request.POST.get('guests')
        new_image = request.FILES.get('image')
        if new_image:
            listing.image = new_image
        listing.save()
        
        return redirect("listing:host_dashboard")
    
    return render(request, "edit_listing.html", {"listing": listing})


def delete_listing(request, listing_id):
    if "user_id" not in request.session:
        return HttpResponse("Login required.")

    
    user = User.objects.get(id = request.session['user_id'])

    if user.role != "host":
        return HttpResponse("Only hosts can delete listings")
    
    listing = get_object_or_404(Listing, id = listing_id, host = user)

    if request.method == "POST":
        listing.delete()
        return redirect("listing:host_dashboard")
    
    return render(request, "confirm_delete.html", {"listing": listing})
    

def search_listing(request):
    query = request.GET.get("q", "")
    city = request.GET.get("city", "")

    listings = Listing.objects.all()

    if query:
        listings = listings.filter(
            Q(title__icontains = query) |
            Q(description__icontains = query)
        ) 
    
    if city:
        listings = listings.filter(city__icontains = city)
    
    return render(request, "search_results.html", {"listings": listings, "query": query, "city": city})


def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id = listing_id)
    return render(request, "listing_detail.html", {"listing": listing})

