from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

from reviews.models import Customer, Restaurant, Review, Visit
from .serializers import (
    MyTokenObtainPairSerializer,
    CustomerSerializer,
    RestaurantSerializer,
    ReviewSerializer,
    VisitSerializer,
)


# jwt
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# all endpoints
@api_view(['GET'])
def get_routes(request):
    """
    Get a list of available API endpoints.

    Returns:
        Response: A JSON response containing a list of available API endpoints.
    """
    routes = [
        '/api/token',
        '/api/token/refresh',

        '/api/customers',
        '/api/customers/<str:username>',

        '/api/restaurants',
        '/api/restaurants/<int:restaurant_id>',

        '/api/reviews/',
        '/api/reviews/<int:review_id>',

        '/api/visits/',
        '/api/visits/<int:visit_id>',
    ]
    return Response(routes)


# customers
@api_view(['GET'])
def get_customers(request, username=None):
    """
    Retrieve customer information.

    Returns:
    - Response: JSON response containing customer information.
    """
    if username:
        customer = get_object_or_404(Customer, username=username)
        serializer = CustomerSerializer(customer, many=False)
    else:
        query = request.GET.get('query', '')
        customers = Customer.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))
        serializer = CustomerSerializer(customers, many=True)

    return Response(serializer.data)


# restaurant
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def restaurants_view(request):
    """
    API endpoint for managing restaurants.

    GET:
        List all restaurants based on optional query parameter 'restaurant_name'.

    POST:
        Create a new restaurant with the provided data.

    Query Parameters:
    - restaurant_name (optional): Filters restaurants by name using case-insensitive partial matching.

    Note:
    - 'average_rating' set to 0 for new restaurants.
    - 'created_by' set to the user making the request for new restaurants.
    """
    restaurant_name = request.GET.get('restaurant_name', '')
    query_params = {}

    if restaurant_name:
        query_params['name__icontains'] = restaurant_name

    # GET (list all)
    if request.method == 'GET':
        restaurants = Restaurant.objects.filter(**query_params)
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST (create new)
    if request.method == 'POST':
        data = {**request.data, 'average_rating': 0, 'created_by': request.user}
        serializer = RestaurantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
def restaurant_detail_view(request, restaurant_id=None):
    """
    API endpoint for managing a specific restaurant.

    GET:
        Retrieve details of a specific restaurant.

    PUT:
        Update the details of a specific restaurant.

    DELETE:
        Delete a specific restaurant.

    Parameters:
    - restaurant_id: ID of the restaurant to be retrieved, updated, or deleted.

    Note:
    - Ensure the provided 'restaurant_id' corresponds to an existing restaurant.
    - PUT request updates fields provided in the request body.
    - DELETE request returns a success message upon successful deletion.
    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    # GET
    if request.method == 'GET':
        serializer = RestaurantSerializer(restaurant, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT
    if request.method == 'PUT':
        serializer = RestaurantSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    if request.method == 'DELETE':
        restaurant.delete()
        return Response({"detail": "Restaurant successfully deleted."}, status=status.HTTP_204_NO_CONTENT)


# review
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def reviews_view(request):
    """
    API endpoint for managing reviews.

    GET:
        List all reviews based on optional query parameter 'username'.

    POST:
        Create a new review with the provided data.

    Query Parameters:
    - username (optional): Filters reviews by the username of the customer.

    Note:
    - 'customer' field automatically set to the authenticated user for new reviews.
    - Ensure 'rating' and 'comment' are provided in the request body for POST requests.
    - Returns a success message upon successful review creation (POST).
    """
    username = request.GET.get('username', '')

    query_params = {}

    if username:
        query_params['customer__username__icontains'] = username

    # GET (list all)
    if request.method == 'GET':
        reviews = Review.objects.filter(**query_params)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    # POST (create new)
    if request.method == 'POST':
        data = {**request.data, 'customer': request.user}
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
def review_detail_view(request, review_id=None):
    """
    API endpoint for managing a specific review.

    GET:
        Retrieve details of a specific review.

    PUT:
        Update the details of a specific review.

    DELETE:
        Delete a specific review.

    Parameters:
    - review_id: ID of the review to be retrieved, updated, or deleted.

    Note:
    - Ensure the provided 'review_id' corresponds to an existing review.
    - PUT request updates fields provided in the request body.
    - DELETE request returns a success message upon successful deletion.
    """
    review = get_object_or_404(Review, id=review_id)

    # GET
    if request.method == 'GET':
        serializer = ReviewSerializer(review, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT
    if request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    if request.method == 'DELETE':
        review.delete()
        return Response({"detail": "Restaurant review successfully deleted."}, status=status.HTTP_204_NO_CONTENT)


# visit
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def visits_view(request):
    """
    API endpoint for managing customer visits.

    GET:
        List all customer visits.

    POST:
        Create a new visit record for the authenticated customer.

    Note:
    - 'customer' field automatically set to the authenticated user for new visits.
    - Ensure 'date' and 'restaurant' are provided in the request body for POST requests.
    - Returns a success message upon successful visit creation (POST).
    """
    # GET (list all)
    if request.method == 'GET':
        visits = Visit.objects.all()
        serializer = VisitSerializer(visits, many=True)
        return Response(serializer.data)

    # POST (create new)
    if request.method == 'POST':
        data = {**request.data, 'customer': request.user}
        serializer = VisitSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
def visit_detail_view(request, visit_id=None):
    """
    API endpoint for managing a specific customer visit.

    GET:
        Retrieve details of a specific customer visit.

    PUT:
        Update the details of a specific customer visit.

    DELETE:
        Delete a specific customer visit.

    Parameters:
    - visit_id: ID of the visit to be retrieved, updated, or deleted.

    Note:
    - Ensure the provided 'visit_id' corresponds to an existing visit.
    - PUT request updates fields provided in the request body.
    - DELETE request returns a success message upon successful deletion.
    """
    visit = get_object_or_404(Visit, id=visit_id)

    # GET
    if request.method == 'GET':
        serializer = VisitSerializer(visit, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT
    if request.method == 'PUT':
        serializer = VisitSerializer(visit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    if request.method == 'DELETE':
        visit.delete()
        return Response({"detail": "Restaurant visit successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
