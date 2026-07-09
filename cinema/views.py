from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
import json

from .models import Movie, Showtime, Booking, Review
from .forms import CinemaUserCreationForm, LoginForm, ReviewForm, BookingForm

def home(request):
    query = request.GET.get('q', '')
    movies = Movie.objects.all()
    if query:
        movies = movies.filter(
            Q(title__icontains=query) |
            Q(genre__icontains=query) |
            Q(language__icontains=query)
        )
    
    # Get a list of genres and languages for filter options (optional, good for UI)
    context = {
        'movies': movies,
        'query': query,
    }
    return render(request, 'movies/home.html', context)


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    showtimes = movie.showtimes.all().order_by('start_time')
    reviews = movie.reviews.all().order_by('-created_at')
    
    # Review form handling
    review_form = ReviewForm()
    user_has_reviewed = False
    
    if request.user.is_authenticated:
        user_has_reviewed = Review.objects.filter(movie=movie, user=request.user).exists()
        
        if request.method == 'POST' and 'submit_review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                if user_has_reviewed:
                    messages.error(request, "You have already reviewed this movie.")
                else:
                    review = review_form.save(commit=False)
                    review.movie = movie
                    review.user = request.user
                    review.save()
                    messages.success(request, "Your review has been submitted!")
                    return redirect('movie_detail', movie_id=movie.id)
            else:
                messages.error(request, "Please correct the errors in your review.")

    context = {
        'movie': movie,
        'showtimes': showtimes,
        'reviews': reviews,
        'review_form': review_form,
        'user_has_reviewed': user_has_reviewed,
    }
    return render(request, 'movies/movie_detail.html', context)


def booking_view(request, showtime_id):
    showtime = get_object_or_404(Showtime, pk=showtime_id)
    
    # Collect currently booked seats
    existing_bookings = Booking.objects.filter(showtime=showtime)
    booked_seats_list = []
    for b in existing_bookings:
        booked_seats_list.extend(b.get_seats_list())
    
    # Convert booked seats to JSON for JS template
    booked_seats_json = json.dumps(booked_seats_list)

    # Prefill name and email if authenticated
    initial_data = {}
    if request.user.is_authenticated:
        initial_data['customer_name'] = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
        initial_data['customer_email'] = request.user.email

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                # Wrap booking in transaction.atomic and select_for_update to prevent duplicate seat assignments
                with transaction.atomic():
                    # Lock the showtime row for update
                    locked_showtime = Showtime.objects.select_for_update().get(pk=showtime_id)
                    
                    # Refetch booked seats inside transaction
                    current_bookings = Booking.objects.filter(showtime=locked_showtime)
                    active_booked_seats = set()
                    for b in current_bookings:
                        active_booked_seats.update(b.get_seats_list())
                    
                    seats_input = form.cleaned_data['seats']
                    requested_seats = [s.strip().upper() for s in seats_input.split(',') if s.strip()]
                    
                    if not requested_seats:
                        raise ValueError("No seats were selected.")
                        
                    # Check for overlaps
                    duplicates = [seat for seat in requested_seats if seat in active_booked_seats]
                    if duplicates:
                        raise ValueError(f"Seat(s) {', '.join(duplicates)} are already booked. Please choose other seats.")

                    # Calculate total price
                    ticket_price = locked_showtime.ticket_price
                    total_price = ticket_price * len(requested_seats)
                    
                    # Save the booking
                    booking = form.save(commit=False)
                    booking.showtime = locked_showtime
                    booking.total_price = total_price
                    if request.user.is_authenticated:
                        booking.user = request.user
                    booking.save()
                    
                    messages.success(request, f"Booking completed successfully for seats {seats_input}!")
                    return redirect('booking_success', booking_reference=booking.booking_reference)

            except ValueError as ve:
                form.add_error(None, str(ve))
                messages.error(request, str(ve))
            except Exception as e:
                form.add_error(None, "An unexpected database error occurred. Please try again.")
                messages.error(request, "Failed to complete transaction.")
    else:
        form = BookingForm(initial=initial_data)

    context = {
        'showtime': showtime,
        'booked_seats_json': booked_seats_json,
        'form': form,
    }
    return render(request, 'movies/booking.html', context)


def booking_success(request, booking_reference):
    booking = get_object_or_404(Booking, booking_reference=booking_reference)
    return render(request, 'movies/booking_success.html', {'booking': booking})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CinemaUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the registration errors.")
    else:
        form = CinemaUserCreationForm()
        
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                next_url = request.GET.get('next', 'home')
                # Avoid open redirect vulnerability
                if not next_url.startswith('/'):
                    next_url = 'home'
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
        
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('home')


@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'movies/user_bookings.html', {'bookings': bookings})
