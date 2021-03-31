from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib import messages

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
                "message": "유효하지 않은 아이디/비밀번호입니다"
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

        if not username:
            return render(request, "auctions/register.html", {
                "message": "아이디를 입력하세요"
            })

        if not password:
            return render(request, "auctions/register.html", {
                "message": "비밀번호를 입력하세요"
            })

        if not confirmation:
            return render(request, "auctions/register.html", {
                "message": "비밀번호를 다시 입력하세요"
            })

        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "비밀번호가 일치하지 않습니다."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "이미 존재하는 아이디입니다."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# for rendering each category page
def get_items(request, catname):
    category = Category.objects.get(english_name=catname)
    return render(request, "auctions/items.html", {
    "catname" : Category.objects.get(english_name=catname),
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
        labels = {
            'price':''
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content' : forms.TextInput(attrs={'placeholder': '댓글을 입력하세요'}),
        }
        labels = {
            'content': ''
        }
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['class'] = 'comment_input'

# for rendering each listing page
def get_listing(request, catname, listingid):
    listing = Listing.objects.get(id=listingid)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bidding_form": BiddingForm(),
        "comment_form": CommentForm(),
        "bidders_count" : Bid.objects.filter(listing=listing).count()
    })

# when user places a bid, save it in database and redirect
def bid(request, listingid):
    
    # get category of the listing, listing, and bidder info
    listing = Listing.objects.get(id=listingid)
    catname = listing.category
    bidder = request.user
    
    if request.method == "POST":
        form = BiddingForm(request.POST)
        
        # if form is invalid, end function
        if not form.is_valid():
            messages.error(request, "다시 시도해보세요")
            return HttpResponseRedirect(reverse("get_listing", kwargs={'catname': 'interior','listingid':1}))

        # get submitted price
        price = form.cleaned_data['price']

        # check if bidding price is valid
        # in case there was no previous bid
        if listing.current_price == 0 and price < listing.starting_price:
            messages.error(request, "시작 가격과 같거나 높게 제시하세요")
            return HttpResponseRedirect(reverse("get_listing", kwargs={'catname': catname,'listingid':listingid}))

        # in case there was a bid
        if listing.current_price != 0 and price <= listing.current_price:
            messages.error(request, "현재 가격보다 높게 제시하세요")
            return HttpResponseRedirect(reverse("get_listing", kwargs={'catname': catname,'listingid':listingid}))
        
        # update current_price of Listing object
        listing.current_price = price
        listing.save()

        # if user placed a bid before, update price field of Bid object
        if Bid.objects.filter(listing=listing, bidder=bidder).exists():             
            obj = Bid.objects.get(listing=listing, bidder=bidder)
            obj.price = price
            obj.save()

        # else, create new Bid object
        else:
            obj = Bid(listing=listing, bidder=bidder, price=price)
            obj.save()

        # show success message
        messages.success(request, "입찰에 성공했어요!")

        return HttpResponseRedirect(reverse("get_listing", kwargs={'catname': catname,'listingid':listingid}))

    else:
        return render(request, "auctions/listing.html", {
            "listing": Listing.objects.filter(id=listingid).first(),
            "current_price": "5000",
            "bidding_form": BiddingForm(),
            "comment_form": CommentForm()
        })

# when user comments, save it in database and redirect
def comment(request):
    if request.method =="POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['content']
            return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/listing.html", {
            "listing": Listing.objects.filter(id=listingid).first(),
            "current_price": "5000",
            "bidding_form": BiddingForm(),
            "comment_form": CommentForm()
        })

# form for sell function

class SellForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['category', 'title', 'starting_price', 'description']
   
        labels = {
            'title':'제목',
            'description': '설명',
            'starting_price':'시작 가격'
        }

    photo = forms.URLField(required=False, label="사진 (선택)", widget=forms.TextInput(attrs={'placeholder': 'URL을 입력하세요(미입력시 기본 사진 사용)'}))

    category = forms.ModelChoiceField(label="카테고리",queryset=Category.objects.all(), empty_label='카테고리를 선택하세요')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields['starting_price'].widget.attrs['min'] = 1
 

def sell(request):
    if request.method =="POST":
        return HttpResponse("yay")
    
    else:
        return render(request, "auctions/sell.html", {
            "form" : SellForm()
        })