from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import ListingForm
from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.filter(is_active=True).order_by("-id")
    return render(request, "auctions/index.html", {"listings": listings})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/login.html", {
            "message": "Invalid username and/or password."
        })
    return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        confirmation = request.POST.get("confirmation", "")
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
    return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            # ensure new listings are active by default
            if listing.is_active is None:
                listing.is_active = True
            listing.save()
            return redirect("index")
    else:
        form = ListingForm()
    return render(request, "auctions/create_listing.html", {"form": form})


def listing(request, listing_id):
    item = get_object_or_404(Listing, pk=listing_id)
    comments = Comment.objects.filter(listing=item).select_related("commenter")

    you_won = request.user.is_authenticated and item.winner_id == request.user.id

    return render(request, "auctions/listing.html", {
        "listing": item,
        "comments": comments,
        "you_won": you_won
    })



@login_required
def place_bid(request, listing_id):
    item = get_object_or_404(Listing, pk=listing_id)
    if not item.is_active:
        return HttpResponse("Auction is closed.")
    if request.method == "POST":
        try:
            amount = float(request.POST.get("bid", ""))
        except ValueError:
            return HttpResponse("Invalid bid amount.")
        # current price = highest of starting_bid and any existing bids
        top = Bid.objects.filter(listing=item).order_by("-amount").first()
        current_price = top.amount if top else item.starting_bid
        if amount <= current_price:
            return HttpResponse("Your bid must be greater than the current price.")
        Bid.objects.create(listing=item, bidder=request.user, amount=amount)
        # reflect current price on the listing for quick display
        item.starting_bid = amount
        item.save()
    return redirect("listing", listing_id=item.id)


@login_required
def add_comment(request, listing_id):
    item = get_object_or_404(Listing, pk=listing_id)
    if request.method == "POST":
        content = request.POST.get("comment", "").strip()
        if content:
            Comment.objects.create(listing=item, commenter=request.user, content=content)
    return redirect("listing", listing_id=item.id)


@login_required
def add_to_watchlist(request, listing_id):
    item = get_object_or_404(Listing, pk=listing_id)
    request.user.watchlist.add(item)
    return redirect("listing", listing_id=item.id)


@login_required
def remove_from_watchlist(request, listing_id):
    item = get_object_or_404(Listing, pk=listing_id)
    request.user.watchlist.remove(item)
    return redirect("listing", listing_id=item.id)


@login_required
def watchlist_view(request):
    listings = request.user.watchlist.all().order_by("-id")
    return render(request, "auctions/watchlist.html", {"listings": listings})


@login_required
def close_auction(request, listing_id):
    item = get_object_or_404(Listing, pk=listing_id)
    if request.user != item.owner:
        return HttpResponse("You are not authorized to close this auction.")
    if request.method == "POST":
        item.is_active = False
        highest = Bid.objects.filter(listing=item).order_by("-amount").first()
        if highest:
            item.winner = highest.bidder
        item.save()
    return redirect("listing", listing_id=item.id)

def categories(request):
    categories = (
        Listing.objects
        .exclude(category__isnull=True)
        .exclude(category__exact="")
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )
    return render(request, "auctions/categories.html", {"categories": categories})

def category_listings(request, category_name):
    listings = Listing.objects.filter(is_active=True, category=category_name).order_by("-id")
    return render(request, "auctions/category_listings.html", {
        "category": category_name,
        "listings": listings
    })# --- categories views (added) ---
def categories(request):
    categories = (
        Listing.objects
        .exclude(category__isnull=True)
        .exclude(category__exact="")
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )
    return render(request, "auctions/categories.html", {"categories": categories})

def category_listings(request, category_name):
    listings = Listing.objects.filter(is_active=True, category=category_name).order_by("-id")
    return render(request, "auctions/category_listings.html", {
        "category": category_name,
        "listings": listings
    })
def categories(request):
    categories = (
        Listing.objects
        .exclude(category__isnull=True)
        .exclude(category__exact="")
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )
    return render(request, "auctions/categories.html", {"categories": categories})

def category_listings(request, category_name):
    listings = Listing.objects.filter(is_active=True, category=category_name).order_by("-id")
    return render(request, "auctions/category_listings.html", {
        "category": category_name,
        "listings": listings
    })
