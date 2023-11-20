from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializers import MyTokenObtainPairSerializer, CustomerSerializer, RestaurantSerializer, ReviewSerializer, VisitSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Customer, Restaurant, Review, Visit
from django.db.models import Q
from django.shortcuts import get_object_or_404
from reviews.forms import RestaurantForm
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework_simplejwt.authentication import JWTAuthentication



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
        '/api/restaurants/create',
        '/api/restaurants/edit/<int:restaurant_id>',
        '/api/restaurants/delete/<int:restaurant_id>',

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


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def createRestaurant(request):
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
def editRestaurant(request, restaurant_id):
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

        form = RestaurantForm(instance=restaurant)

    return render(request, 'reviews/restaurant_form.html', {'form': form})


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def deleteRestaurant(request, restaurant_id):
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