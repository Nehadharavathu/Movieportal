import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

class Movie(models.Model):
    CERTIFICATE_CHOICES = [
        ('U', 'U (Unrestricted Public Exhibition)'),
        ('UA', 'UA (Parental Guidance Required under 12)'),
        ('A', 'A (Adults Only)'),
        ('R', 'R (Restricted)'),
    ]

    title = models.CharField(max_length=200)
    synopsis = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField(help_text="Duration in minutes")
    certificate = models.CharField(max_length=10, choices=CERTIFICATE_CHOICES, default='U')
    language = models.CharField(max_length=50)
    genre = models.CharField(max_length=100)
    poster_url = models.URLField(max_length=500, blank=True, null=True, help_text="Direct link to poster image")

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0.0

    @property
    def vote_count(self):
        return self.reviews.count()


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    start_time = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        formatted_time = self.start_time.strftime('%Y-%m-%d %I:%M %p')
        return f"{self.movie.title} - {formatted_time}"


class Booking(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    seats = models.CharField(max_length=255, help_text="Comma-separated list of seat numbers (e.g. A1,A2)")
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    booking_reference = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_seats_list(self):
        if not self.seats:
            return []
        return [seat.strip().upper() for seat in self.seats.split(',') if seat.strip()]

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            # Generate a clean unique code
            self.booking_reference = 'MOV-' + str(uuid.uuid4().hex[:8]).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.booking_reference} for {self.showtime.movie.title} ({self.seats})"


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating between 1 and 5 stars"
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        # Enforce that a user can only review a movie once
        unique_together = ('movie', 'user')

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star review for {self.movie.title}"
