from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .utils import ListingForm, getCategory, checkNewBid
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
    listing = Listing.objects.get(pk = listing_id)
    is_in_watchlist = is_editable = is_watchable = False
    if request.user.is_authenticated:
        user = User.objects.get(username = request.user.username)
        is_editable =  listing.auctioneer == user
        is_watchable = not is_editable
        if is_watchable:
            is_in_watchlist = user.watchlist.filter(pk = listing_id).exists()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_editable": is_editable,
        "is_watchable": is_watchable,
        "is_in_watchlist": is_in_watchlist,
        "bid_message": "Some bid message"
    })



@login_required
def new_listing(request):
    if request.method == "POST":
        print(request)
        form = ListingForm(request.POST)
        print(form)
        if form.is_valid():
            newListing = form.save(commit=False)
            newListing.auctioneer = User.objects.get(username=request.user.username)
            newListing.created_date = datetime.datetime.now()
            newListing.is_active = True
            newListing.category = getCategory(form.cleaned_data["categoryTitle"])
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
    listing = Listing.objects.get(pk = listing_id)
    if listing is not None:
        if request.method == "POST":
            form = ListingForm(request.POST, instance=listing)
            if form.is_valid():
                listing = form.save(commit=False)
                listing.category = getCategory(form.cleaned_data["categoryTitle"])
                listing.save()
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            else:
                return render(request, "auctions/editor.html", {
                    "title" : f"{listing.title} - Edit",
                    "listing_id" : listing_id,
                    "action" : "edit",
                    "form" : form
                }) 
        form = ListingForm(instance=listing, initial={'categoryTitle': listing.category})
        return render(request, "auctions/editor.html", {
            "title" : f"{listing.title} - Edit",
            "listing_id" : listing_id,
            "action" : "edit",
            "form" : form
        })
    
@login_required
def edit_watchlist(request, listing_id):
    user = User.objects.get(username = request.user.username)
    listing = Listing.objects.get(pk=listing_id)
    if user.watchlist.filter(pk=listing.id).exists():
        user.watchlist.remove(listing)
    else:
        user.watchlist.add(listing)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def my_watchlist(request):
    user = User.objects.get(username = request.user.username)
    return render(request,"auctions/watchlist.html", {
        "active_list": user.watchlist.all().filter(is_active = True),
        "closed_list": user.watchlist.all().filter(is_active = False) 
    })

@login_required
def place_bid(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    user = User.objects.get(username = request.user.username)
    is_in_watchlist = is_editable = is_watchable = False
    is_editable =  listing.auctioneer == user
    is_watchable = not is_editable
    if is_watchable:
        is_in_watchlist = user.watchlist.filter(pk = listing_id).exists()
    if listing is not None:
        if request.method == "POST":
            try:
                new_bid = float(request.POST['bid'])
                if new_bid != "" :
                    if checkNewBid(new_bid, listing_id):
                        newBid = Bid()
                        newBid.bidder = user
                        newBid.context = listing
                        newBid.price = new_bid
                        newBid.bid_date = datetime.datetime.now()
                        newBid.save()
                    else:
                        return render(request, "auctions/listing.html", {
                            "listing": listing,
                            "is_editable": is_editable,
                            "is_watchable": is_watchable,
                            "is_in_watchlist": is_in_watchlist,
                            "bid_message": f"Your bid ${new_bid} is too low!"
                        })
            except ValueError:
                return render(request, "auctions/listing.html", {
                            "listing": listing,
                            "is_editable": is_editable,
                            "is_watchable": is_watchable,
                            "is_in_watchlist": is_in_watchlist,
                            "bid_message": "Bid should be a decimal number!"
                        })

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))