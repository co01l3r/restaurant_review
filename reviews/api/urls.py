from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views
from reviews.api.views import MyTokenObtainPairView

urlpatterns = [
    path('', views.getRoutes),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenObtainPairView.as_view(), name='token_refresh'),

    path('customers/', views.getCustomers, name='customers'),
    path('customers/<str:username>/', views.getCustomer, name='customer'),

    path('restaurants/', views.getRestaurants, name='restaurant-list'),
    path('restaurants/<int:restaurant_id>/', views.getRestaurant, name='restaurant-detail'),

    path('reviews/', views.getReviews, name='reviews-list'),
]
