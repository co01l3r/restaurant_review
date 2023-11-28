from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views
from reviews.api.views import MyTokenObtainPairView

urlpatterns = [
    path('', views.get_routes),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenObtainPairView.as_view(), name='token_refresh'),

    path('customers/', views.get_customers, name='customers'),
    path('customers/<str:username>/', views.get_customers, name='customer'),

    path('restaurants/', views.get_restaurants, name='restaurants'),
    path('restaurants/<int:restaurant_id>/', views.restaurant_view, name='restaurant'),
    path('restaurants/create-restaurant', views.create_restaurant, name='create-restaurant'),

    path('reviews/', views.get_reviews, name='reviews'),
    path('reviews/<int:review_id>', views.review_view, name='review'),
    path('reviews/create-review', views.create_review, name='create-review'),

    path('visits/', views.get_visits, name='visits'),
    path('visits/<int:visit_id>', views.visit_view, name='visit'),
    path('visits/create-visit', views.create_visit, name='create-visit'),
]
