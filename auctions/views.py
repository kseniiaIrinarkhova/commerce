from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .utils import ListingForm, getCategory, checkNewBid
import datetime
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Bid, Category, Comment


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
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
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
            user.first_name = first_name
            user.last_name = last_name
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
    if request.user.is_authenticated:
        user = User.objects.get(username = request.user.username)
        #get additional information about listing according to the user
        listing.check_user_related_data(user)  
    else:
        #set default value for user related information
        listing.check_user_related_data(None)   

    return render(request, "auctions/listing.html", {
        "listing": listing,        
        "bid_message": "",
        "comments" : Comment.objects.all().filter(context = listing)
    })



@login_required
def new_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            newListing = form.save(commit=False)
            newListing.auctioneer = User.objects.get(username=request.user.username)
            newListing.created_date = datetime.datetime.now()
            newListing.is_active = True
            #Try to found existing category or creating a new one
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
        "active_list": Listing.ownerList.getActiveListings(user),
        "closed_list": Listing.ownerList.getClosedListings(user),
    })

@login_required
def edit(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    if listing is not None:
        if request.method == "POST":
            form = ListingForm(request.POST, instance=listing)
            if form.is_valid():
                listing = form.save(commit=False)
                #Try to found existing category or creating a new one
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
            "title" : listing.title,
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
    if request.POST["wl_flag"] == "True":
        return HttpResponseRedirect(reverse("my_watchlist", ))
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
    if listing is not None:
        listing.check_user_related_data(user)
        if request.method == "POST":
            try:
                new_bid = float(request.POST['bid'])
                if new_bid != "" :
                    #Check if new bid is higher than previous or if there is no bids then higher or equel to the price
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
                            "bid_message": f"Your bid ${new_bid} is too low!",
                            "comments" : Comment.objects.all().filter(context = listing)
                        })
            except ValueError:
                return render(request, "auctions/listing.html", {
                            "listing": listing,                           
                            "bid_message": "Bid should be a decimal number!",                          
                            "comments" : Comment.objects.all().filter(context = listing)
                        })

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def close_auction(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    user = User.objects.get(username = request.user.username)
    if user == listing.auctioneer:
        listing.is_active = False
        listing.closed_date = datetime.datetime.now()
        listing.save()
        if Bid.objects.all().filter(context = listing).exists():
            won_bid = Bid.objects.all().filter(context = listing).last()
            won_bid.is_won = True
            won_bid.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def add_comment(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    user = User.objects.get(username = request.user.username)
    if request.method == "POST" and listing is not None:
        comment = request.POST['comment']
        if comment != "" :
            newComment = Comment.objects.create_comment(listing, user, comment)
            newComment.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))