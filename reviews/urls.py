from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    register,
    login_view,
    add_restaurant,
    edit_restaurant,
    restaurant_list,
    delete_restaurant,
    restaurant_detail,
    create_review,
    user_reviews,
    add_visit,
    user_visits,
    delete_visit,
)

urlpatterns = [
    path('', login_view, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('restaurants/add/', add_restaurant, name='add_restaurant'),
    path('restaurants/edit/<int:restaurant_id>/', edit_restaurant, name='edit_restaurant'),
    path('restaurants/delete/<int:restaurant_id>/', delete_restaurant, name='delete_restaurant'),
    path('restaurants/', restaurant_list, name='restaurant_list'),
    path('restaurants/<int:restaurant_id>/', restaurant_detail, name='restaurant_detail'),

    path('restaurants/<int:restaurant_id>/reviews/create/', create_review, name='create_review'),
    path('user-reviews/', user_reviews, name='user_reviews'),

    path('restaurants/<int:restaurant_id>/visits/add/', add_visit, name='add_visit'),
    path('user-visits/', user_visits, name='user_visits'),
    path('user-visits/delete_visit/<int:visit_id>/', delete_visit, name='delete_visit'),

    path(
        'reset-password/',
        auth_views.PasswordResetView.as_view(
            template_name='reviews/reset_password.html',
            email_template_name='reviews/reset_password.html',
        ),
        name='reset_password'
    ),
    path(
        'reset-password-done/',
        auth_views.PasswordResetDoneView.as_view(template_name='reviews/reset_password_sent.html'),
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
