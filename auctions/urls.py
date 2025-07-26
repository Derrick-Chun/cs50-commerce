from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("listing/<int:listing_id>/bid", views.place_bid, name="place_bid"),
    path("listing/<int:listing_id>/comment", views.add_comment, name="add_comment"),
    path("listing/<int:listing_id>/add_watchlist", views.add_to_watchlist, name="add_watchlist"),
    path("listing/<int:listing_id>/remove_watchlist", views.remove_from_watchlist, name="remove_watchlist"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("listing/<int:listing_id>/close", views.close_auction, name="close_auction"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category_name>", views.category_listings, name="category_listings")
]
