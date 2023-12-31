from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Restaurant, Review, Visit


# user
class RegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


# restaurant
class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'cuisine', 'address']


# review
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'pricing', 'comment']


# visit
class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['date', 'spending']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
