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

    path('restaurants/', views.restaurants_view, name='restaurants'),
    path('restaurants/<int:restaurant_id>/', views.restaurant_detail_view, name='restaurant'),

    path('reviews/', views.reviews_view, name='reviews'),
    path('reviews/<int:review_id>', views.review_detail_view, name='review'),

    path('visits/', views.visits_view, name='visits'),
    path('visits/<int:visit_id>', views.visit_detail_view, name='visit'),
]
