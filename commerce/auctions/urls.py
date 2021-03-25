from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("all", views.get_all_items, name="get_all_items"),
    path("listings/<str:catname>/", views.get_items),
    path("listings/<str:catname>/<str:listingid>/", views.get_listing, name="get_listing"),
    path("bid", views.bid, name="place_bid"),
    path("comment", views.comment, name="comment")
]
