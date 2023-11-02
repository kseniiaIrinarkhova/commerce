from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.utils import ErrorList
from .models import User, Listing, Bid, Category, Comment
from django.utils.html import format_html, html_safe

#class for Custom TextInput field
class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list':'list__%s' % self._name, 'class': 'form-control'})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        #Form the datalist of Categories
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % str(item).title()
        data_list += '</datalist>'

        return format_html(text_html + data_list)
    
#Form for Listing object    
class ListingForm(ModelForm):
    #Add new attribute to have an opportunity of both creating and choosing Category
    categoryTitle = forms.CharField(label="Category")                
    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields["categoryTitle"].widget = ListTextWidget(
            data_list=Category.objects.all(), 
            name='category_list')

    #Use a Listing Model as a source for form
    class Meta:
        model = Listing
        exclude = ['category', 'auctioneer', 'is_active', 'created_date', 'closed_date']
        labels = {
            'title': "Listing Title",
            "description:": "Short Description of lisitng",
            "price": "Price in $",
            "image:": "URL for image"}

#Form for Bid information        
class BidForm(ModelForm):
    class Meta:
        model = Bid
        exclude = ['bidder', 'context', 'bid_date']
        labels = {
            "price": "Your bid in $"
        }

#Function for analysing the Category of Listing
def getCategory(categoryTitle):
    #Try to get the category from existing ones
    try:
        category = Category.objects.get(title = categoryTitle)
    except Category.DoesNotExist:
        #Create a new category from InputField
        category = Category()
        category.title = categoryTitle
        category.save()
    return category 

#Get current action for watching list        
def getWatchListAction(listing_id, user):
    #If user has listing in watch list then available action is to delete listing from watch list
    if user.watchlist.filter(pk = listing_id).exists():
        return "del_watchlist"   
    #otherwise available action to add listing to watchlist
    return "add_watchlist"

#Check if it possible to place bid that user wanted to place
def checkNewBid(new_bid, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    try:
        #If there are bids, check that new one is higher than the highest one 
        max_bid = Bid.objects.filter(context = listing).order_by("id").latest("id")
        return new_bid > max_bid.price
    except Bid.DoesNotExist:
        #If there is the first bid - check that it is higher than or equel to the listing price
        return new_bid >= listing.price
    
    