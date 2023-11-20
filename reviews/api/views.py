from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import MyTokenObtainPairSerializer, CustomerSerializer, RestaurantSerializer, ReviewSerializer, VisitSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Customer, Restaurant, Review, Visit
from django.db.models import Q
from django.shortcuts import get_object_or_404


# jwt
class MyTokenObtainPairView(TokenObtainPairView):
    # /api/token
    # /api/token/refresh
    serializer_class = MyTokenObtainPairSerializer


# all endpoints
@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',

        '/api/customers',
        '/api/customers/<str:username>',

        '/api/restaurants',
        '/api/restaurants/<int:restaurant_id>',

        '/api/reviews',
        '/api/reviews/<int:review_id>',

        '/api/visits',
        '/api/visits/<int:visit_id>',
    ]
    return Response(routes)


# customer
@api_view(['GET'])
def getCustomers(request):
    query = request.GET.get('query', '')

    customers = Customer.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))
    serializer = CustomerSerializer(customers, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def getCustomer(request, username):
    customer = get_object_or_404(Customer, username=username)
    serializer = CustomerSerializer(customer, many=False)

    return Response(serializer.data)


# restaurant
@api_view(['GET'])
def getRestaurants(request):
    restaurant_name = request.GET.get('restaurant_name', '')

    query_params = {}

    if restaurant_name:
        query_params['restaurant__name__icontains'] = restaurant_name

    restaurants = Restaurant.objects.filter(**query_params)
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
    username = request.GET.get('username', '')
    restaurant_name = request.GET.get('restaurant_name', '')

    query_params = {}

    if username:
        query_params['customer__username__icontains'] = username

    if restaurant_name:
        query_params['restaurant__name__icontains'] = restaurant_name

    reviews = Review.objects.filter(**query_params)
    serializer = ReviewSerializer(reviews, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def getReview(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    serializer = ReviewSerializer(review, many=False)

    return Response(serializer.data)


# visit
@api_view(['GET'])
def getVisits(request):
    username = request.GET.get('username', '')
    restaurant_name = request.GET.get('restaurant_name', '')

    query_params = {}

    if username:
        query_params['customer__username__icontains'] = username

    if restaurant_name:
        query_params['restaurant__name__icontains'] = restaurant_name

    visits = Visit.objects.filter(**query_params)
    serializer = VisitSerializer(visits, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def getVisit(request, visit_id):
    # /api/visits/<int:visit_id>
    visit = get_object_or_404(Visit, id=visit_id)
    serializer = VisitSerializer(visit, many=False)

    return Response(serializer.data)
