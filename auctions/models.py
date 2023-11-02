from django.contrib.auth.models import AbstractUser
from django.db import models

#Owner list manager provide information about owner's active list and closed list        
class OwnerListManager(models.Manager): 
    def getActiveListings(self,user):
        list = self.filter(auctioneer = user, is_active = True)
        for item in list:
            item.check_user_related_data(user)  
        return list
    def getClosedListings(self,user):
        list = self.filter(auctioneer = user, is_active = False)
        for item in list:
            item.check_user_related_data(user)      
        return list

#Listing Model
class Listing(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=7,decimal_places=2)
    image = models.URLField(blank=True)
    category = models.ForeignKey("Category", models.SET_NULL, blank=True, null=True)
    auctioneer = models.ForeignKey("User", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField()
    closed_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    #Define additional properties related to the user's information
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_watchable = False
        self._is_editable = False
        self._is_in_watchlist = False
        self._bid_info = {'count': 0, 'max_bid': 0, 'user_bid': False}
   
    #set additioal properties data according to the user
    def check_user_related_data(self, user):
        if user is not None:
            if self.auctioneer != user:
                #If user is not auctioneer then listing could be added/deleted to user's watch list
                self._is_watchable = True
                self._is_in_watchlist = user.watchlist.filter(pk = self.id).exists()
            else:
                #if listing is owned by user, it could be edited
                self._is_editable = True
            #check the bid information
            if Bid.objects.all().filter(context = self).exists():
                self._bid_info['count'] = Bid.objects.all().filter(context = self).count()
                self._bid_info['max_bid'] = Bid.objects.all().filter(context = self).last().price
                self._bid_info['user_bid'] = user == Bid.objects.all().filter(context = self).last().bidder
        else:
            self._is_editable = False

    @property
    def is_watchable(self):
        return self._is_watchable
    
    @property
    def is_editable(self):
        return self._is_editable
    
    @property
    def is_in_watchlist(self):
        return self._is_in_watchlist
    
    @property
    def bid_info(self):
        return self._bid_info
    
    objects = models.Manager()
    #custom manager for owner list
    ownerList = OwnerListManager()
        
    
class User(AbstractUser):
    #property that represented list of items in user's watch list
    watchlist = models.ManyToManyField(Listing, blank=True, related_name='subscribers')    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Bid(models.Model):
    bidder = models.ForeignKey("User", on_delete=models.CASCADE)
    context = models.ForeignKey("Listing", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    bid_date = models.DateTimeField()
    is_won = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.bidder}: ${self.price}"

class CommentManager(models.Manager):
    def create_comment(self, context, author, text):
        comment = self.create(context = context, author = author, text = text)
        return comment

class Comment(models.Model):
    context = models.ForeignKey("Listing", on_delete=models.CASCADE)
    author = models.ForeignKey("User", on_delete=models.CASCADE)
    text = models.TextField()

    objects = CommentManager()


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    

