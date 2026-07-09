from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Review, Booking

class CinemaUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-cinema',
        'placeholder': 'Enter your email'
    }))

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-cinema'
            if 'placeholder' not in field.widget.attrs:
                field.widget.attrs['placeholder'] = f"Enter {field.label}"


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-cinema',
        'placeholder': 'Enter username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-cinema',
        'placeholder': 'Enter password'
    }))


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        widget=forms.RadioSelect(
            choices=[(i, f"{i} Star") for i in range(5, 0, -1)],
            attrs={'class': 'rating-star-radio'}
        ),
        min_value=1,
        max_value=5
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-cinema',
            'rows': 4,
            'placeholder': 'Write your review here...'
        })
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer_name', 'customer_email', 'seats']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control form-control-cinema',
                'placeholder': 'Enter full name'
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control form-control-cinema',
                'placeholder': 'Enter email address'
            }),
            'seats': forms.HiddenInput()  # Populated dynamically via JS
        }
