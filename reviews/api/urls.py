from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views
from reviews.api.views import MyTokenObtainPairView

urlpatterns = [
    path('', views.getRoutes),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenObtainPairView.as_view(), name='token_refresh'),

    path('customers/', views.get_customers, name='customers'),
    path('customers/<str:username>/', views.get_customers, name='customer'),

    path('restaurants/', views.get_restaurants, name='restaurants'),
    path('restaurants/<int:restaurant_id>/', views.get_restaurants, name='restaurant'),
    path('restaurants/create-restaurant', views.create_restaurant, name='create-restaurant'),
    #
    # path('restaurants/', views.getRestaurants, name='restaurant-list'),
    # path('restaurants/<int:restaurant_id>/', views.getRestaurant, name='restaurant-detail'),
    # path('restaurants/create/', views.createRestaurant, name='create-restaurant'),
    # path('restaurants/edit/<int:restaurant_id>/', views.editRestaurant, name='edit-restaurant'),
    # path('restaurants/<int:restaurant_id>/reviews/', views.listReviews, name='list-reviews'),
    # path('restaurants/<int:restaurant_id>/reviews/create/', views.createReview, name='create-review'),
    # path('restaurants/<int:restaurant_id>/reviews/edit/<int:review_id>/', views.editReview, name='edit-review'),
    # path('restaurants/delete/<int:restaurant_id>/', views.deleteRestaurant, name='delete-restaurant'),
    # path('restaurants/<int:restaurant_id>/average-rating/', views.get_average_rating, name='restaurant-average-rating'),
    # path('restaurants/<int:restaurant_id>/pricing-category/', views.get_pricing_category_evaluation, name='restaurant-pricing-category'),
    # path('restaurants/<int:restaurant_id>/visits/create/', views.createVisit, name='create-visit'),
    #
    # path('reviews/', views.getReviews, name='reviews-list'),
    # path('reviews/<int:review_id>/', views.getReview, name='review-detail'),
    #
    # path('visits/', views.getVisits, name='visits-list'),
    # path('visits/<int:visit_id>/', views.getVisit, name='visit-detail'),
    # path('visits/<int:visit_id>/delete/', views.deleteVisit, name='delete-visit'),
]
