from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from .models import Movie, Showtime, Booking, Review

class CinemaPortalTestCase(TestCase):
    def setUp(self):
        # Create standard test movie
        self.movie = Movie.objects.create(
            title="Sci-Fi Adventure",
            synopsis="An epic space voyage.",
            release_date=timezone.now().date(),
            duration=120,
            certificate="U",
            language="English",
            genre="Sci-Fi"
        )
        
        # Create showtime
        self.showtime = Showtime.objects.create(
            movie=self.movie,
            start_time=timezone.now() + timedelta(hours=3),
            ticket_price=Decimal("10.00")
        )
        
        # Create test users
        self.user1 = User.objects.create_user(username="testuser1", password="pass123", email="user1@example.com")
        self.user2 = User.objects.create_user(username="testuser2", password="pass123", email="user2@example.com")

    def test_movie_average_rating_and_vote_count(self):
        # Default rating with no reviews should be 0.0
        self.assertEqual(self.movie.average_rating, 0.0)
        self.assertEqual(self.movie.vote_count, 0)
        
        # Create first review
        Review.objects.create(movie=self.movie, user=self.user1, rating=5, comment="Amazing movie!")
        self.assertEqual(self.movie.average_rating, 5.0)
        self.assertEqual(self.movie.vote_count, 1)
        
        # Create second review
        Review.objects.create(movie=self.movie, user=self.user2, rating=4, comment="Good watch.")
        self.assertEqual(self.movie.average_rating, 4.5)
        self.assertEqual(self.movie.vote_count, 2)

    def test_review_rating_validators(self):
        # Attempt to create a review with invalid rating > 5
        review_invalid = Review(movie=self.movie, user=self.user1, rating=6, comment="Invalid rating")
        with self.assertRaises(ValidationError):
            review_invalid.full_clean()

        # Attempt to create a review with invalid rating < 1
        review_invalid2 = Review(movie=self.movie, user=self.user1, rating=0, comment="Invalid rating")
        with self.assertRaises(ValidationError):
            review_invalid2.full_clean()

    def test_booking_reference_and_seats_list(self):
        # Create booking
        booking = Booking.objects.create(
            showtime=self.showtime,
            customer_name="John Doe",
            customer_email="john@example.com",
            seats="A1, A2",
            total_price=Decimal("20.00")
        )
        
        # Reference should be auto-generated
        self.assertTrue(booking.booking_reference.startswith("MOV-"))
        self.assertEqual(len(booking.booking_reference), 12)  # MOV- + 8 characters
        
        # Seats list parsing
        self.assertEqual(booking.get_seats_list(), ["A1", "A2"])
