from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Bit, Comment, Listing,Category

# Register your models here.


admin.site.register(User, UserAdmin)
admin.site.register(Listing)
admin.site.register(Bit)
admin.site.register(Comment)
admin.site.register(Category)