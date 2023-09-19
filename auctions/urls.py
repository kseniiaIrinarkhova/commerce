from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/new", views.new_listing, name="new_listing"),
    path("listing/mine", views.my_listings, name="my_listings"),
    path("listing/watchlist", views.my_watchlist, name="my_watchlist"),
    path("listing/<int:listing_id>/edit", views.edit, name="edit"),
    path("listing/<int:listing_id>/edit_watchlist", views.edit_watchlist, name="edit_watchlist"),
    path("listing/<int:listing_id>/place_bid", views.place_bid, name="place_bid"),
    path("listing/<int:listing_id>/close_auction", views.close_auction, name="close_auction"),
    path("listing/<int:listing_id>/add_comment", views.add_comment, name="add_comment")
]
