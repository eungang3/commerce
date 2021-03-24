from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django import forms

from .models import *

def index(request):
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.all()
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

# for rendering each category page
def get_items(request, catname):
    category = Category.objects.filter(english_name=catname).first()
    return render(request, "auctions/items.html", {
        "catname" : category,
        "listings" : Listing.objects.filter(category=category.id)
    })

# for rendering whole category page
def get_all_items(request):
    return render(request, "auctions/items.html", {
        "catname" : "전체",
        "listings" : Listing.objects.all()
    })

# create the form class
class BiddingForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['price']
        widgets = {
            'price': forms.NumberInput(attrs={'placeholder': '입찰가를 입력하세요'}),
        }

# for rendering each listing page
def get_listing(request, catname, listingid):
    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.filter(id=listingid).first(),
        "current_price": "5000",
        "bidding_form": BiddingForm()
    })

# when user places a bid, save it in database and redirect
def bid(request):
    if request.method == "POST":
        form = BiddingForm(request.POST)
        if form.is_valid():
            price = form.cleaned_data['price']
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/listing.html", {
            "listing": Listing.objects.filter(id=listingid).first(),
            "current_price": "5000",
            "bidding_form": BiddingForm()
        })
