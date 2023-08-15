from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
import datetime
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Bid, Category


def index(request):
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.filter(is_active = True)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def listing(request, listing_id):
    print("Listing view")
    listing = Listing.objects.get(pk = listing_id)
    if request.user.is_authenticated:
        is_editable =  listing.auctioneer == User.objects.get(username = request.user.username)
    else:
        is_editable = False
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_editable": is_editable 
    })

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'image', 'category', 'auctioneer', 'is_active', 'created_date', 'closed_date']

@login_required
def new_listing(request):
    if request.method == "POST":
        print(request)
        form = ListingForm(request.POST)
        print(form)
        if form.is_valid():
            newListing = form.save()
            newListing.save()
            return HttpResponseRedirect(reverse("listing", args=(newListing.id,)))
        else:
           return render(request, "auctions/editor.html", {
            "title" : "New listing",
            "action" : "new_listing",
            "listing_id": None,
            "form" : form
            }) 
    form = ListingForm()
    form.fields["auctioneer"].initial = User.objects.get(username=request.user.username)
    form.fields["created_date"].initial = datetime.datetime.now()
    form.fields["is_active"].initial = True
    return render(request, "auctions/editor.html", {
        "title" : "New listing",
        "action" : "new_listing",
        "listing_id": None,
        "form" : form
    })

@login_required
def my_listings(request):
    user = User.objects.get(username = request.user.username)
    return render(request,"auctions/owner_list.html", {
        "active_list": Listing.objects.filter(auctioneer = user, is_active = True),
        "closed_list": Listing.objects.filter(auctioneer = user, is_active = False) 
    })

@login_required
def edit(request, listing_id):
    print("Edit view")
    listing = Listing.objects.get(pk = listing_id)
    print(listing)
    if listing is not None:
        if request.method == "POST":
            form = ListingForm(request.POST, instance=listing)
            print(form)
            if form.is_valid():
                print("Valid form")
                form.save()
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            else:
                print("Not valid form")
                return render(request, "auctions/editor.html", {
                    "title" : f"{listing.title} - Edit",
                    "listing_id" : listing_id,
                    "action" : "edit",
                    "form" : form
                }) 
        print("Get")    
        form = ListingForm(instance=listing)
        return render(request, "auctions/editor.html", {
            "title" : f"{listing.title} - Edit",
            "listing_id" : listing_id,
            "action" : "edit",
            "form" : form
        })