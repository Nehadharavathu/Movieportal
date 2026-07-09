from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('booking/<int:showtime_id>/', views.booking_view, name='booking_view'),
    path('booking/success/<str:booking_reference>/', views.booking_success, name='booking_success'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-bookings/', views.user_bookings, name='user_bookings'),
]
