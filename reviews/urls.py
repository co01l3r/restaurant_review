from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import register, login_view, add_restaurant, edit_restaurant, restaurant_list, delete_restaurant

urlpatterns = [
    path('', register, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('add-restaurant/', add_restaurant, name='add_restaurant'),
    path('edit-restaurant/<int:restaurant_id>/', edit_restaurant, name='edit_restaurant'),
    path('delete-confirmation/<int:restaurant_id>/', delete_restaurant, name='delete_restaurant'),
    path('restaurant-list/', restaurant_list, name='restaurant_list'),
]
