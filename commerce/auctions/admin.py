from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "korean_name")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "seller", "title", "starting_price", "current_price")

class BidAdmin(admin.ModelAdmin):
    list_display = ("bidder", "time", "price", "listing")

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)
admin.site.register(Watchlist)
