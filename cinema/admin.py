from django.contrib import admin
from .models import Movie, Showtime, Booking, Review

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'duration', 'certificate', 'language', 'genre', 'get_average_rating', 'get_vote_count')
    search_fields = ('title', 'genre', 'language')
    list_filter = ('certificate', 'language', 'genre')

    def get_average_rating(self, obj):
        return obj.average_rating
    get_average_rating.short_description = 'Avg Rating'

    def get_vote_count(self, obj):
        return obj.vote_count
    get_vote_count.short_description = 'Votes'


@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'start_time', 'ticket_price')
    list_filter = ('movie', 'start_time')
    ordering = ('start_time',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'showtime', 'customer_name', 'customer_email', 'seats', 'total_price', 'created_at')
    search_fields = ('booking_reference', 'customer_name', 'customer_email', 'seats')
    list_filter = ('created_at', 'showtime__movie')
    readonly_fields = ('booking_reference', 'created_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'movie')
    search_fields = ('user__username', 'comment', 'movie__title')
