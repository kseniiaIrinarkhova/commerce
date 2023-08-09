from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Listing(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=7,decimal_places=2)
    image = models.URLField(blank=True)
    category = models.ForeignKey("Category", models.SET_NULL, blank=True, null=True)
    auctioneer = models.ForeignKey("User", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class Bid(models.Model):
    bidder = models.ForeignKey("User", on_delete=models.CASCADE)
    context = models.ForeignKey("Listing", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    bid_date = models.DateTimeField()


class Comment(models.Model):
    context = models.ForeignKey("Listing", on_delete=models.CASCADE)
    author = models.ForeignKey("User", on_delete=models.CASCADE)
    text = models.TextField()
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

class Category(models.Model):
    title = models.CharField(max_length=50)