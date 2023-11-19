from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import MyTokenObtainPairSerializer, CustomerSerializer, RestaurantSerializer, ReviewSerializer, VisitSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Customer, Restaurant, Review, Visit
from django.db.models import Q
from django.shortcuts import get_object_or_404


# jwt
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# customer
@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',

        '/api/customers',
        '/api/customers/<str:username>',

        '/api/restaurants',
        '/api/restaurants/<int:restaurant_id>',
    ]
    return Response(routes)


@api_view(['GET'])
def getCustomers(request):
    # /api/customers/?query=
    query = request.GET.get('query', '')

    customers = Customer.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))
    serializer = CustomerSerializer(customers, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def getCustomer(request, username):
    customer = Customer.objects.get(username=username)
    serializer = CustomerSerializer(customer, many=False)

    return Response(serializer.data)


# restaurant
@api_view(['GET'])
def getRestaurants(request):
    # /api/restaurants/?query=
    query = request.GET.get('query', '')

    restaurants = Restaurant.objects.filter(Q(name__icontains=query) | Q(address__icontains=query))
    serializer = RestaurantSerializer(restaurants, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def getRestaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    serializer = RestaurantSerializer(restaurant, many=False)

    return Response(serializer.data)


# review
@api_view(['GET'])
def getReviews(request):
    # /api/reviews/?query=
    query = request.GET.get('query', '')

    reviews = Review.objects.filter(
        Q(restaurant__name__icontains=query) |
        Q(customer__username__icontains=query) |
        Q(rating__icontains=query)
    )
    serializer = RestaurantSerializer(reviews, many=True)

    return Response(serializer.data)


# visit