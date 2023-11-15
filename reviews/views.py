from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, LoginForm, RestaurantForm
from .models import Restaurant
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


# user
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'reviews/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('restaurant_list')
    else:
        form = LoginForm()

    return render(request, 'reviews/login.html', {'form': form})


# restaurant
@login_required
def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)

        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.created_by = request.user
            restaurant.save()
            return redirect('restaurant_list')
    else:
        form = RestaurantForm()

    return render(request, 'reviews/restaurant_form.html', {'form': form})


@login_required
def edit_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.user != restaurant.created_by:
        raise PermissionDenied("You don't have permission to edit this restaurant.")

    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('restaurant_list')
    else:
        form = RestaurantForm(instance=restaurant)

    return render(request, 'reviews/restaurant_form.html', {'form': form, 'restaurant': restaurant})


@login_required
def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.user != restaurant.created_by:
        raise PermissionDenied("You don't have permission to delete this restaurant.")

    if request.method == 'POST':
        restaurant.delete()
        return redirect('restaurant_list')

    return render(request, 'delete_confirmation.html', {'restaurant': restaurant})


def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'reviews/restaurant_list.html', {'restaurants': restaurants})
