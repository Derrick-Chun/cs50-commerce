from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

    path("create/", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("listing/<int:listing_id>/bid/", views.place_bid, name="place_bid"),
    path("listing/<int:listing_id>/comment/", views.add_comment, name="add_comment"),
    path("listing/<int:listing_id>/watch/", views.add_to_watchlist, name="add_watchlist"),
    path("listing/<int:listing_id>/unwatch/", views.remove_from_watchlist, name="remove_watchlist"),

    path("close/<int:listing_id>/", views.close_auction, name="close_auction"),

    path("watchlist/", views.watchlist_view, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:category_name>/", views.category_listings, name="category_listings"),
]
