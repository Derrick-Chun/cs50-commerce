from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import ListingForm
from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

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
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

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


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect("index")
    else:
        form = ListingForm()
    return render(request, "auctions/create_listing.html", {
        "form": form
    })


def listing(request, listing_id):
    item = get_object_or_404(Listing, pk=listing_id)
    comments = Comment.objects.filter(listing=item)
    return render(request, "auctions/listing.html", {
        "listing": item,
        "comments": comments
    })


@login_required
def place_bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == "POST":
        try:
            bid_amount = float(request.POST["bid"])
        except ValueError:
            return HttpResponse("Invalid bid amount.")

        if bid_amount > listing.starting_bid:
            Bid.objects.create(listing=listing, bidder=request.user, amount=bid_amount)
            listing.starting_bid = bid_amount
            listing.save()
        else:
            return HttpResponse("Your bid must be higher than the current price.")

    return redirect("listing", listing_id=listing.id)


@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == "POST":
        content = request.POST["comment"]
        Comment.objects.create(listing=listing, commenter=request.user, content=content)
    return redirect("listing", listing_id=listing.id)


@login_required
def add_to_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    request.user.watchlist.add(listing)
    return redirect("listing", listing_id=listing.id)


@login_required
def remove_from_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    request.user.watchlist.remove(listing)
    return redirect("listing", listing_id=listing.id)


@login_required
def watchlist_view(request):
    listings = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.user != listing.owner:
        return HttpResponse("You are not authorized to close this auction.")

    listing.is_active = False

    highest_bid = Bid.objects.filter(listing=listing).order_by("-amount").first()
    if highest_bid:
        listing.winner = highest_bid.bidder

    listing.save()
    return redirect("listing", listing_id=listing.id)


def categories(request):
    all_categories = Listing.objects.exclude(category__isnull=True).exclude(category__exact="").values_list('category', flat=True).distinct()
    return render(request, "auctions/categories.html", {
        "categories": all_categories
    })


def category_listings(request, category_name):
    listings = Listing.objects.filter(category=category_name, is_active=True)
    return render(request, "auctions/category_listings.html", {
        "category": category_name,
        "listings": listings
    })

