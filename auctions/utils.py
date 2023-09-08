from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.utils import ErrorList
from .models import User, Listing, Bid, Category

class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list':'list__%s' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % str(item).title()
        data_list += '</datalist>'

        return (text_html + data_list)
    
class ListingForm(ModelForm):
    categoryTitle = forms.CharField(label="Category")                
    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields["categoryTitle"].widget = ListTextWidget(
            data_list=Category.objects.all(), 
            name='category_list',
            attrs={'autocomplete': 'off'})

    class Meta:
        model = Listing
        exclude = ['category', 'auctioneer', 'is_active', 'created_date', 'closed_date']
        labels = {
            'title': "Listing Title",
            "description:": "Short Description of lisitng",
            "price": "Price in $",
            "image:": "URL for image"}
        
class BidForm(ModelForm):
    class Meta:
        model = Bid
        exclude = ['bidder', 'context', 'bid_date']
        labels = {
            "price": "Your bid in $"
        }

def getCategory(categoryTitle):
    return Category.objects.get(title = categoryTitle)
        
def getWatchListAction(listing_id, user):
    
    if user.watchlist.filter(pk = listing_id).exists():
        return "del_watchlist"   
    return "add_watchlist"


def checkNewBid(new_bid, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    try:
        max_bid = Bid.objects.filter(context = listing).order_by("id").latest("id")
        return new_bid > max_bid.price
    except Bid.DoesNotExist:
        return new_bid >= listing.price