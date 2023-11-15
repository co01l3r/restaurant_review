from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import register, login_view, add_restaurant, restaurant_list

urlpatterns = [
    path('', register, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('add-restaurant/', add_restaurant, name='add_restaurant'),
    path('edit-restaurant/', add_restaurant, name='edit_restaurant'),
    path('restaurant-list/', restaurant_list, name='restaurant_list'),
]
