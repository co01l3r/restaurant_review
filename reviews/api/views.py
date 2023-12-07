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
        '/api/restaurants/create-restaurant',

        '/api/reviews/',
        '/api/reviews/<int:review_id>',
        '/api/reviews/create-review',

        '/api/visits/',
        '/api/visits/<int:visit_id>',
        '/api/visits/create-visit',
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
@api_view(['GET'])
def get_restaurants(request):
    """
    Retrieve restaurant information.

    Returns:
    - Response: JSON response containing restaurant information.
    """
    restaurant_name = request.GET.get('restaurant_name', '')
    query_params = {}

    if restaurant_name:
        query_params['name__icontains'] = restaurant_name

    restaurants = Restaurant.objects.filter(**query_params)
    serializer = RestaurantSerializer(restaurants, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
def restaurant_view(request, restaurant_id=None):
    """
    Perform operations on a specific restaurant.

    Parameters:
        - request (Request): The HTTP request object.
        - restaurant_id (int, optional): The ID of the restaurant.

    Methods:
        - GET: Retrieve details of a restaurant.
        - PUT: Update an existing restaurant.
        - DELETE: Delete a restaurant.

    Returns:
        Response: JSON response containing restaurant information or operation result.
    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    # GET
    if request.method == 'GET':
        serializer = RestaurantSerializer(restaurant, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT
    if request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        # Data from the request
        data = request.data

        # Validate the data
        required_fields = ['name', 'cuisine', 'address']
        for field in required_fields:
            if field not in data:
                return Response({"detail": f"Missing required field '{field}' in the request data."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the restaurant
        restaurant.name = data['name']
        restaurant.cuisine = data['cuisine']
        restaurant.address = data['address']
        restaurant.created_by = request.user

        restaurant.save()

        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # DELETE
    if request.method == 'DELETE':
        restaurant.delete()
        return Response({"detail": "Restaurant successfully deleted."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_restaurant(request):
    """
    Create a new restaurant.

    Parameters:
    - request (Request): The HTTP request object.

    Returns:
    - Response: JSON response containing information about the created restaurant.
    """
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        # Data from the request
        data = request.data

        # Validate the data
        required_fields = ['name', 'cuisine', 'address']
        for field in required_fields:
            if field not in data:
                return Response({"detail": f"Missing required field '{field}' in the request data."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new restaurant
        restaurant = Restaurant(
            name=data['name'],
            cuisine=data['cuisine'],
            address=data['address'],
            created_by=request.user
        )
        restaurant.save()

        serializer = RestaurantSerializer(restaurant)
        response_data = serializer.data

        return Response(response_data, status=status.HTTP_201_CREATED)


# review
@api_view(['GET'])
def get_reviews(request):
    """
    Get a list of reviews based on an optional username filter.

    Parameters:
        - request (Request): The HTTP GET request object.

    Returns:
        Response: A JSON response with a list of serialized reviews.

    Example:
        To get reviews for a specific user:
        GET /api/reviews?username=johndoe
    """
    username = request.GET.get('username', '')

    query_params = {}

    if username:
        query_params['customer__username__icontains'] = username

    reviews = Review.objects.filter(**query_params)
    serializer = ReviewSerializer(reviews, many=True)

    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
def review_view(request, review_id=None):
    """
    Manage a single review.

    Parameters:
        - request (Request): The HTTP request object.
        - review_id (int, optional): The ID of the review.

    Methods:
        - GET: Retrieve details of a review.
        - PUT: Update an existing review.
        - DELETE: Delete a review.

    Returns:
        Response: JSON response with review details or status messages.
    """
    review = get_object_or_404(Review, id=review_id)

    # GET
    if request.method == 'GET':
        serializer = ReviewSerializer(review, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT
    if request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        # Data from the request
        data = request.data

        # Validate the data
        if 'rating' not in data or not isinstance(data['rating'], int):
            return Response({"detail": "Invalid or missing 'rating' in the request data."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the review
        review.rating = data['rating']
        review.save()

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # DELETE
    if request.method == 'DELETE':
        review.delete()
        return Response({"detail": "Restaurant review successfully deleted."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_review(request):
    """
    Create a new review.

    Parameters:
        - request (Request): The HTTP POST request object.

    Returns:
        Response: JSON response with the newly created review details or validation errors.
    """
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        # Data from the request
        data = request.data

        # Validate the data
        required_fields = ['restaurant', 'rating', 'pricing', 'comment']
        for field in required_fields:
            if field not in data:
                return Response({"detail": f"Missing required field '{field}' in the request data."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new review
        review = Review(
            restaurant=data['restaurant'],
            rating=data['rating'],
            pricing=data['pricing'],
            comment=data['comment'],
            customer=request.user
        )
        review.save()

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# visit
@api_view(['GET'])
def get_visits(request):
    """
    Retrieve a list of visits.

    Parameters:
        - request (Request): The HTTP GET request object.

    Returns:
        Response: JSON response with a list of serialized visits.
    """
    visits = Visit.objects.all()
    serializer = VisitSerializer(visits, many=True)

    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
def visit_view(request, visit_id=None):
    """
    Manage a single restaurant visit.

    Parameters:
        - request (Request): The HTTP request object.
        - visit_id (int, optional): The ID of the visit.

    Methods:
        - GET: Retrieve details of a visit.
        - PUT: Update an existing visit.
        - DELETE: Delete a visit.

    Returns:
        Response: JSON response with visit details or status messages.
    """
    visit = get_object_or_404(Visit, id=visit_id)

    # GET
    if request.method == 'GET':
        serializer = VisitSerializer(visit, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT
    if request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        # Data from the request
        data = request.data

        # Validate the data
        required_fields = ['restaurant', 'date', 'spending']
        for field in required_fields:
            if field not in data:
                return Response({"detail": f"Missing required field '{field}' in the request data."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the visit
        visit.customer = request.user
        visit.restaurant = data['restaurant']
        visit.date = data['date']
        visit.spending = data['spending']

        visit.save()

        serializer = VisitSerializer(visit)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # DELETE
    if request.method == 'DELETE':
        visit.delete()
        return Response({"detail": "Restaurant visit successfully deleted."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_visit(request):
    """
    Create a new restaurant visit.

    Parameters:
        - request (Request): The HTTP POST request object.

    Returns:
        Response: JSON response with the newly created visit details or validation errors.
    """
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        # Data from the request
        data = request.data

        # Validate the data
        required_fields = ['restaurant', 'date', 'spending']
        for field in required_fields:
            if field not in data:
                return Response({"detail": f"Missing required field '{field}' in the request data."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new visit
        visit = Visit(
            customer=request.user,
            restaurant=data['restaurant'],
            date=data['date'],
            spending=data['spending']
        )
        visit.save()

        serializer = VisitSerializer(visit)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
