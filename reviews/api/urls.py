from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views
from reviews.api.views import MyTokenObtainPairView

urlpatterns = [
    path('', views.getRoutes),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenObtainPairView.as_view(), name='token_refresh'),

    path('customers/', views.getCustomers, name='customer-list'),
    path('customers/<str:username>/', views.getCustomer, name='customer-detail'),

    path('restaurants/', views.getRestaurants, name='restaurant-list'),
    path('restaurants/<int:restaurant_id>/', views.getRestaurant, name='restaurant-detail'),
    path('restaurants/create/', views.createRestaurant, name='create-restaurant'),
    path('restaurants/edit/<int:restaurant_id>/', views.editRestaurant, name='edit-restaurant'),
    path('restaurants/delete/<int:restaurant_id>/', views.deleteRestaurant, name='delete-restaurant'),

    path('reviews/', views.getReviews, name='reviews-list'),
    path('reviews/<int:review_id>/', views.getReview, name='review-detail'),
    path('restaurants/<int:restaurant_id>/reviews/create/', views.createReview, name='create-review'),

    path('visits/', views.getVisits, name='visits-list'),
    path('visits/<int:visit_id>/', views.getVisit, name='visit-detail'),
]
