import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_booking.settings")
django.setup()

from cinema.models import Movie, Showtime, Review
from django.contrib.auth.models import User

def seed():
    # 1. Create movies
    m1, _ = Movie.objects.get_or_create(
        title="Interstellar",
        defaults={
            "synopsis": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
            "release_date": datetime(2014, 11, 7).date(),
            "duration": 169,
            "certificate": "UA",
            "language": "English",
            "genre": "Sci-Fi / Adventure",
            "poster_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=600&auto=format&fit=crop"
        }
    )

    m2, _ = Movie.objects.get_or_create(
        title="Inception",
        defaults={
            "synopsis": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
            "release_date": datetime(2010, 7, 16).date(),
            "duration": 148,
            "certificate": "UA",
            "language": "English",
            "genre": "Sci-Fi / Action",
            "poster_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?q=80&w=600&auto=format&fit=crop"
        }
    )

    m3, _ = Movie.objects.get_or_create(
        title="The Dark Knight",
        defaults={
            "synopsis": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
            "release_date": datetime(2008, 7, 18).date(),
            "duration": 152,
            "certificate": "UA",
            "language": "English",
            "genre": "Action / Drama",
            "poster_url": "https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0?q=80&w=600&auto=format&fit=crop"
        }
    )

    m4, _ = Movie.objects.get_or_create(
        title="Avatar: The Way of Water",
        defaults={
            "synopsis": "Jake Sully lives with his newfound family formed on the extrasolar moon Pandora. Once a familiar threat returns to finish what was previously started, Jake must work with Neytiri and the army of the Na'vi race to protect their home.",
            "release_date": datetime(2022, 12, 16).date(),
            "duration": 192,
            "certificate": "UA",
            "language": "English",
            "genre": "Action / Adventure",
            "poster_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=600&auto=format&fit=crop"
        }
    )

    print("Movies seeded successfully.")

    # 2. Create showtimes
    now = timezone.now()
    
    # Clean old showtimes
    Showtime.objects.all().delete()
    
    # Create for Movie 1 (Interstellar)
    Showtime.objects.create(
        movie=m1,
        start_time=now + timedelta(hours=2),
        ticket_price=12.50
    )
    Showtime.objects.create(
        movie=m1,
        start_time=now + timedelta(days=1, hours=4),
        ticket_price=15.00
    )

    # Create for Movie 2 (Inception)
    Showtime.objects.create(
        movie=m2,
        start_time=now + timedelta(hours=5),
        ticket_price=10.00
    )
    Showtime.objects.create(
        movie=m2,
        start_time=now + timedelta(days=1, hours=2),
        ticket_price=12.00
    )

    # Create for Movie 3 (The Dark Knight)
    Showtime.objects.create(
        movie=m3,
        start_time=now + timedelta(hours=8),
        ticket_price=11.50
    )

    # Create for Movie 4 (Avatar)
    Showtime.objects.create(
        movie=m4,
        start_time=now + timedelta(days=2, hours=1),
        ticket_price=14.00
    )

    print("Showtimes seeded successfully.")

    # 3. Create users & reviews
    u1, _ = User.objects.get_or_create(username="john_doe", defaults={"email": "john@example.com"})
    u1.set_password("pass123")
    u1.save()
    
    u2, _ = User.objects.get_or_create(username="movie_buff", defaults={"email": "buff@example.com"})
    u2.set_password("pass123")
    u2.save()

    # Clear old reviews
    Review.objects.all().delete()

    Review.objects.create(
        movie=m1,
        user=u1,
        rating=5,
        comment="Absolutely mind-bending! Hans Zimmer's score is a masterpiece itself. Highly recommended."
    )
    Review.objects.create(
        movie=m1,
        user=u2,
        rating=4,
        comment="Incredible visuals and emotional weight. A bit long, but completely worth the time."
    )

    Review.objects.create(
        movie=m2,
        user=u1,
        rating=5,
        comment="One of the best movies of all time. The concept of dreams within dreams is executed flawlessly."
    )

    Review.objects.create(
        movie=m3,
        user=u2,
        rating=5,
        comment="Heath Ledger's performance as the Joker is legendary. The dark tone set a new standard for superhero films."
    )

    print("Reviews seeded successfully.")

if __name__ == "__main__":
    seed()
