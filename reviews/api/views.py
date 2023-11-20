from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.forms import RestaurantForm, ReviewForm, VisitForm
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
    # /api/token
    # /api/token/refresh
    serializer_class = MyTokenObtainPairSerializer


# all endpoints
@api_view(['GET'])
def getRoutes(request):
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
        '/api/restaurants/create',
        '/api/restaurants/edit/<int:restaurant_id>',
        '/api/restaurants/delete/<int:restaurant_id>',
        '/api/restaurants/<int:restaurant_id>/reviews',
        '/api/restaurants/<int:restaurant_id>/reviews/create',
        '/api/restaurants/<int:restaurant_id>/reviews/edit'
        '/api/restaurants/<int:restaurant_id>/reviews',
        '/api/restaurants/<int:restaurant_id>/average-rating',
        '/api/restaurants/<int:restaurant_id>/pricing-category',

        '/api/reviews',
        '/api/reviews/<int:review_id>',

        '/api/visits',
        '/api/visits/<int:visit_id>',
        '/api/visits/<int:visit_id>/delete',
    ]
    return Response(routes)


# customer
@api_view(['GET'])
def getCustomers(request):
    """
    Get a list of customers based on the provided query.

    This function accepts a query parameter and filters customers based on
    the provided query, considering both username and email.

    Parameters:
        request (Request): The HTTP request object.
        query (str, optional): The query string for filtering customers.

    Returns:
        Response: A JSON response containing the serialized list of customers.

    Example:
        To get customers based on a query, make a GET request to this endpoint:

        ```http
        GET /api/customers?query=<your_query_here>
        ```

    """
    query = request.GET.get('query', '')

    customers = Customer.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))
    serializer = CustomerSerializer(customers, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def getCustomer(request, username: str):
    """
    Get details of a specific customer.

    This function retrieves details of a specific customer identified by the
    provided username.

    Parameters:
        request (Request): The HTTP request object.
        username (str): The username of the customer to retrieve.

    Returns:
        Response: A JSON response containing the serialized details of the customer.

    Example:
        To get details of a specific customer, make a GET request to this endpoint:

        ```http
        GET /api/customers/<username>
        ```

    """
    customer = get_object_or_404(Customer, username=username)
    serializer = CustomerSerializer(customer, many=False)

    return Response(serializer.data)


# restaurant
@api_view(['GET'])
def getRestaurants(request):
    """
    Get a list of restaurants based on the provided query.

    This function accepts a query parameter for the restaurant name and
    filters restaurants based on the provided query.

    Parameters:
        request (Request): The HTTP request object.
            restaurant_name (str, optional): The query string for filtering restaurants by name.

    Returns:
        Response: A JSON response containing the serialized list of restaurants.

    Example:
        To get restaurants based on a query, make a GET request to this endpoint:

        ```http
        GET /api/restaurants?restaurant_name=<your_query_here>
        ```

    """
    restaurant_name = request.GET.get('restaurant_name', '')

    query_params = {}

    if restaurant_name:
        query_params['restaurant__name__icontains'] = restaurant_name

    restaurants = Restaurant.objects.filter(**query_params)
    serializer = RestaurantSerializer(restaurants, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def getRestaurant(request, restaurant_id: int):
    """
    Get details of a specific restaurant.

    This function retrieves details of a specific restaurant identified by the
    provided restaurant_id.

    Parameters:
        request (Request): The HTTP request object.
        restaurant_id (int): The ID of the restaurant to retrieve.

    Returns:
        Response: A JSON response containing the serialized details of the restaurant.

    Example:
        To get details of a specific restaurant, make a GET request to this endpoint:

        ```http
        GET /api/restaurants/<restaurant_id>
        ```

    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    serializer = RestaurantSerializer(restaurant, many=False)

    return Response(serializer.data)


# review
@api_view(['GET'])
def getReviews(request):
    """
    Get a list of reviews based on the provided query.

    This function accepts query parameters for the customer username and
    restaurant name, and filters reviews based on the provided queries.

    Parameters:
        request (Request): The HTTP request object.
            username (str, optional): The query string for filtering reviews by customer username.
            restaurant_name (str, optional): The query string for filtering reviews by restaurant name.

    Returns:
        Response: A JSON response containing the serialized list of reviews.

    Example:
        To get reviews based on queries, make a GET request to this endpoint:

        ```http
        GET /api/reviews?username=<customer_username>&restaurant_name=<restaurant_name>
        ```

    """
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
def getReview(request, review_id: int):
    """
    Get details of a specific review.

    This function retrieves details of a specific review identified by the
    provided review_id.

    Parameters:
        request (Request): The HTTP request object.
        review_id (int): The ID of the review to retrieve.

    Returns:
        Response: A JSON response containing the serialized details of the review.

    Example:
        To get details of a specific review, make a GET request to this endpoint:

        ```http
        GET /api/reviews/<review_id>
        ```

    """
    review = get_object_or_404(Review, id=review_id)
    serializer = ReviewSerializer(review, many=False)

    return Response(serializer.data)


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def createReview(request, restaurant_id: int):
    """
    Create or retrieve reviews for a specific restaurant.

    This function allows users to create a new review for a specific restaurant
    or retrieve the existing reviews for that restaurant.

    Parameters:
        request (Request): The HTTP request object.
        restaurant_id (int): The ID of the restaurant for which the review is created or retrieved.

    Returns:
        Response: A JSON response containing the serialized review data if created,
        or the HTML response for rendering the review creation form.

    Example:
        To create a new review, make a POST request to this endpoint:

        ```http
        POST /api/reviews/create/<restaurant_id>
        ```

    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        customer, created = Customer.objects.get_or_create(username=request.user.username)

        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.customer = customer
            review.restaurant = restaurant
            review.save()
            serializer = ReviewSerializer(review)
            messages.success(request, 'Review added successfully.')
            return Response(serializer.data)
        else:
            messages.error(request, 'Error in form submission.')
            print(f"Form errors: {form.errors}")

    else:
        form = ReviewForm()

    return render(request, 'reviews/create_review.html', {'form': form, 'restaurant': restaurant})


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def editReview(request, restaurant_id: int, review_id: int):
    """
    Edit an existing review for a specific restaurant.

    This function allows users to edit an existing review for a specific restaurant.

    Parameters:
        request (Request): The HTTP request object.
        restaurant_id (int): The ID of the restaurant for which the review is edited.
        review_id (int): The ID of the review to be edited.

    Returns:
        Response: A JSON response containing the serialized review data if updated,
        or the HTML response for rendering the review edit form.

    Example:
        To edit an existing review, make a POST request to this endpoint:

        ```http
        POST /api/reviews/edit/<restaurant_id>/<review_id>
        ```

    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':
        customer, created = Customer.objects.get_or_create(username=request.user.username)

        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            review = form.save(commit=False)
            review.customer = customer
            review.restaurant = restaurant
            review.save()
            serializer = ReviewSerializer(review)
            messages.success(request, 'Review updated successfully.')
            return Response(serializer.data)
        else:
            messages.error(request, 'Error in form submission.')
            print(f"Form errors: {form.errors}")

    else:
        form = ReviewForm(instance=review)

    return render(request, 'reviews/create_review.html', {'form': form, 'restaurant': restaurant, 'review': review})


# restaurant
@api_view(['GET'])
def get_average_rating(request, restaurant_id: int):
    """
    Get the average rating for a specific restaurant.

    This function retrieves the average rating for a specific restaurant
    identified by the provided restaurant_id.

    Parameters:
        request (Request): The HTTP request object.
        restaurant_id (int): The ID of the restaurant for which the average rating is calculated.

    Returns:
        Response: A JSON response containing the average rating.

    Example:
        To get the average rating for a specific restaurant, make a GET request to this endpoint:

        ```http
        GET /api/restaurants/<restaurant_id>/average-rating
        ```

    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    average_rating = restaurant.average_rating()

    return Response({'average_rating': average_rating})


@api_view(['GET'])
def get_pricing_category_evaluation(request, restaurant_id: int):
    """
    Get the pricing category evaluation for a specific restaurant.

    This function retrieves the pricing category evaluation for a specific restaurant
    identified by the provided restaurant_id.

    Parameters:
        request (Request): The HTTP request object.
        restaurant_id (int): The ID of the restaurant for which the pricing category evaluation is calculated.

    Returns:
        Response: A JSON response containing the pricing category evaluation.

    Example:
        To get the pricing category evaluation for a specific restaurant, make a GET request to this endpoint:

        ```http
        GET /api/restaurants/<restaurant_id>/pricing-category
        ```

    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    pricing_category_eval = restaurant.get_restaurant_pricing_category_eval()

    return Response({'pricing_category_evaluation': pricing_category_eval})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def listReviews(request, restaurant_id: int):
    """
    List reviews for a specific restaurant.

    This function retrieves and lists reviews for a specific restaurant
    identified by the provided restaurant_id.

    Parameters:
        request (Request): The HTTP request object.
        restaurant_id (int): The ID of the restaurant for which the reviews are listed.

    Returns:
        Response: An HTML response for rendering the list of reviews.

    Example:
        To list reviews for a specific restaurant, make a GET request to this endpoint:

        ```http
        GET /api/restaurants/<restaurant_id>/list-reviews
        ```

    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    reviews = Review.objects.filter(restaurant=restaurant)
    serializer = ReviewSerializer(reviews, many=True)

    return render(request, 'reviews/list_reviews.html', {'reviews': serializer.data, 'restaurant': restaurant})


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def createRestaurant(request):
    """
    Create a new restaurant.

    This function allows users to create a new restaurant by providing the
    necessary information in the form.

    Parameters:
        request (Request): The HTTP request object.

    Returns:
        Response: An HTML response for rendering the restaurant creation form or
        a JSON response containing the serialized restaurant data if created.

    Example:
        To create a new restaurant, make a POST request to this endpoint:

        ```http
        POST /api/restaurants/create
        ```

    """
    if request.method == 'POST':
        form = RestaurantForm(request.POST)

        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.created_by = request.user
            restaurant.save()
            serializer = RestaurantSerializer(restaurant)
            messages.success(request, 'Restaurant added successfully.')
            return Response(serializer.data)
        else:
            messages.error(request, 'Error in form submission.')

    else:
        form = RestaurantForm()

    return render(request, 'reviews/restaurant_form.html', {'form': form})


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def editRestaurant(request, restaurant_id: int):
    """
    Edit an existing restaurant.

    This function allows users to edit an existing restaurant by providing the
    necessary information in the form.

    Parameters:
        request (Request): The HTTP request object.
        restaurant_id (int): The ID of the restaurant to be edited.

    Returns:
        Response: An HTML response for rendering the restaurant edit form or
        a JSON response containing the serialized restaurant data if updated.

    Example:
        To edit an existing restaurant, make a POST request to this endpoint:

        ```http
        POST /api/restaurants/edit/<restaurant_id>
        ```

    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=restaurant)

        if form.is_valid():
            updated_restaurant = form.save()
            serializer = RestaurantSerializer(updated_restaurant)
            messages.success(request, 'Restaurant updated successfully.')
            return Response(serializer.data)
        else:
            messages.error(request, 'Error in form submission.')

    else:
        form = RestaurantForm(instance=restaurant)

    return render(request, 'reviews/restaurant_form.html', {'form': form})


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def deleteRestaurant(request, restaurant_id: int):
    """
    Delete an existing restaurant.

    This function allows users to delete an existing restaurant.

    Parameters:
        request (Request): The HTTP request object.
        restaurant_id (int): The ID of the restaurant to be deleted.

    Returns:
        Response: An HTML response for rendering the restaurant deletion confirmation page or
        a redirect to the list of restaurants if the restaurant is deleted.

    Example:
        To delete an existing restaurant, make a POST request to this endpoint:

        ```http
        POST /api/restaurants/delete/<restaurant_id>
        ```

    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        restaurant.delete()
        messages.success(request, 'Restaurant deleted successfully.')
        return redirect('list-restaurants')
    else:
        return render(request, 'reviews/delete_restaurant.html', {'restaurant': restaurant})


# visit
@api_view(['GET'])
def getVisits(request):
    """
    Get a list of visits based on the provided query.

    This function accepts query parameters for the customer username and
    restaurant name, and filters visits based on the provided queries.

    Parameters:
        request (Request): The HTTP request object.
            username (str, optional): The query string for filtering visits by customer username.
            restaurant_name (str, optional): The query string for filtering visits by restaurant name.

    Returns:
        Response: A JSON response containing the serialized list of visits.

    Example:
        To get visits based on queries, make a GET request to this endpoint:

        ```http
        GET /api/visits?username=<customer_username>&restaurant_name=<restaurant_name>
        ```

    """
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
def getVisit(request, visit_id: int):
    """
    Get details of a specific visit.

    This function retrieves details of a specific visit identified by the
    provided visit_id.

    Parameters:
        request (Request): The HTTP request object.
        visit_id (int): The ID of the visit to retrieve.

    Returns:
        Response: A JSON response containing the serialized details of the visit.

    Example:
        To get details of a specific visit, make a GET request to this endpoint:

        ```http
        GET /api/visits/<visit_id>
        ```

    """
    visit = get_object_or_404(Visit, id=visit_id)
    serializer = VisitSerializer(visit, many=False)

    return Response(serializer.data)


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def createVisit(request, restaurant_id: int):
    """
    Create a new visit to a specific restaurant.

    This function allows users to create a new visit to a specific restaurant
    by providing the necessary information in the form.

    Parameters:
        request (Request): The HTTP request object.
        restaurant_id (int): The ID of the restaurant for which the visit is created.

    Returns:
        Response: An HTML response for rendering the visit creation form or
        a JSON response containing the serialized visit data if created.

    Example:
        To create a new visit, make a POST request to this endpoint:

        ```http
        POST /api/visits/create/<restaurant_id>
        ```

    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        customer, created = Customer.objects.get_or_create(username=request.user.username)

        form = VisitForm(request.POST)

        if form.is_valid():
            visit = form.save(commit=False)
            visit.customer = customer
            visit.restaurant = restaurant
            visit.save()
            serializer = VisitSerializer(visit)
            messages.success(request, 'Visit added successfully.')
            return Response(serializer.data)
        else:
            messages.error(request, 'Error in form submission.')
            print(f"Form errors: {form.errors}")
            return Response({'detail': 'Error in form submission.'}, status=400)

    else:
        form = VisitForm()

    return render(request, 'reviews/add_visit.html', {'form': form, 'restaurant': restaurant})


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def deleteVisit(request, visit_id: int):
    """
    Delete a visit.

    This function allows users to delete a visit.

    Parameters:
        request (Request): The HTTP request object.
        visit_id (int): The ID of the visit to be deleted.

    Returns:
        Response: An HTML response for rendering the user visits page after deleting the visit.

    Example:
        To delete a visit, make a POST request to this endpoint:

        ```http
        POST /api/visits/delete/<visit_id>
        ```

    """
    visit = get_object_or_404(Visit, id=visit_id)

    visit.delete()
    messages.success(request, 'Visit deleted successfully.')
    return render(request, 'reviews/user_visits.html')
