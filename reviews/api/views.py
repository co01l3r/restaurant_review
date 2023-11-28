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
def get_customers(request, username=None):
    if username:
        customer = get_object_or_404(Customer, username=username)
        serializer = CustomerSerializer(customer, many=False)
    else:
        query = request.GET.get('query', '')
        customers = Customer.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))
        serializer = CustomerSerializer(customers, many=True)

    return Response(serializer.data)


# restaurant
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_restaurant(request):
    if request.method == 'POST':
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)



    # restaurant_name = request.GET.get('restaurant_name', '')
#
#     query_params = {}
#
#     if restaurant_name:
#         query_params['restaurant__name__icontains'] = restaurant_name
#
#     restaurants = Restaurant.objects.filter(**query_params)
#     serializer = RestaurantSerializer(restaurants, many=True)
#
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def getRestaurant(request, restaurant_id: int):
#     restaurant = get_object_or_404(Restaurant, id=restaurant_id)
#     serializer = RestaurantSerializer(restaurant, many=False)
#
#     return Response(serializer.data)
#
#
# # review
# @api_view(['GET'])
# def getReviews(request):
#     username = request.GET.get('username', '')
#     restaurant_name = request.GET.get('restaurant_name', '')
#
#     query_params = {}
#
#     if username:
#         query_params['customer__username__icontains'] = username
#
#     if restaurant_name:
#         query_params['restaurant__name__icontains'] = restaurant_name
#
#     reviews = Review.objects.filter(**query_params)
#     serializer = ReviewSerializer(reviews, many=True)
#
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def getReview(request, review_id: int):
#     review = get_object_or_404(Review, id=review_id)
#     serializer = ReviewSerializer(review, many=False)
#
#     return Response(serializer.data)
#
#
# @api_view(['GET', 'POST'])
# @authentication_classes([JWTAuthentication])
# def createReview(request, restaurant_id: int):
#     restaurant = get_object_or_404(Restaurant, id=restaurant_id)
#
#     if request.method == 'POST':
#         customer, created = Customer.objects.get_or_create(username=request.user.username)
#
#         form = ReviewForm(request.POST)
#
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.customer = customer
#             review.restaurant = restaurant
#             review.save()
#             serializer = ReviewSerializer(review)
#             messages.success(request, 'Review added successfully.')
#             return Response(serializer.data)
#         else:
#             messages.error(request, 'Error in form submission.')
#             print(f"Form errors: {form.errors}")
#
#     else:
#         form = ReviewForm()
#
#     return render(request, 'reviews/create_review.html', {'form': form, 'restaurant': restaurant})
#
#
# @api_view(['GET', 'POST'])
# @authentication_classes([JWTAuthentication])
# def editReview(request, restaurant_id: int, review_id: int):
#     restaurant = get_object_or_404(Restaurant, id=restaurant_id)
#     review = get_object_or_404(Review, id=review_id)
#
#     if request.method == 'POST':
#         customer, created = Customer.objects.get_or_create(username=request.user.username)
#
#         form = ReviewForm(request.POST, instance=review)
#
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.customer = customer
#             review.restaurant = restaurant
#             review.save()
#             serializer = ReviewSerializer(review)
#             messages.success(request, 'Review updated successfully.')
#             return Response(serializer.data)
#         else:
#             messages.error(request, 'Error in form submission.')
#             print(f"Form errors: {form.errors}")
#
#     else:
#         form = ReviewForm(instance=review)
#
#     return render(request, 'reviews/create_review.html', {'form': form, 'restaurant': restaurant, 'review': review})
#
#
# # restaurant
# @api_view(['GET'])
# def get_average_rating(request, restaurant_id: int):
#     restaurant = get_object_or_404(Restaurant, id=restaurant_id)
#     average_rating = restaurant.average_rating()
#
#     return Response({'average_rating': average_rating})
#
#
# @api_view(['GET'])
# def get_pricing_category_evaluation(request, restaurant_id: int):
#     restaurant = get_object_or_404(Restaurant, id=restaurant_id)
#     pricing_category_eval = restaurant.get_restaurant_pricing_category_eval()
#
#     return Response({'pricing_category_evaluation': pricing_category_eval})
#
#
# @api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# def listReviews(request, restaurant_id: int):
#     restaurant = get_object_or_404(Restaurant, id=restaurant_id)
#     reviews = Review.objects.filter(restaurant=restaurant)
#     serializer = ReviewSerializer(reviews, many=True)
#
#     return render(request, 'reviews/list_reviews.html', {'reviews': serializer.data, 'restaurant': restaurant})
#
#
# @api_view(['GET', 'POST'])
# @authentication_classes([JWTAuthentication])
# def createRestaurant(request):
#     if request.method == 'POST':
#         form = RestaurantForm(request.POST)
#
#         if form.is_valid():
#             restaurant = form.save(commit=False)
#             restaurant.created_by = request.user
#             restaurant.save()
#             serializer = RestaurantSerializer(restaurant)
#             messages.success(request, 'Restaurant added successfully.')
#             return Response(serializer.data)
#         else:
#             messages.error(request, 'Error in form submission.')
#
#     else:
#         form = RestaurantForm()
#
#     return render(request, 'reviews/restaurant_form.html', {'form': form})
#
#
# @api_view(['GET', 'POST'])
# @authentication_classes([JWTAuthentication])
# def editRestaurant(request, restaurant_id: int):
#     restaurant = get_object_or_404(Restaurant, id=restaurant_id)
#
#     if request.method == 'POST':
#         form = RestaurantForm(request.POST, instance=restaurant)
#
#         if form.is_valid():
#             updated_restaurant = form.save()
#             serializer = RestaurantSerializer(updated_restaurant)
#             messages.success(request, 'Restaurant updated successfully.')
#             return Response(serializer.data)
#         else:
#             messages.error(request, 'Error in form submission.')
#
#     else:
#         form = RestaurantForm(instance=restaurant)
#
#     return render(request, 'reviews/restaurant_form.html', {'form': form})
#
#
# @api_view(['GET', 'POST'])
# @authentication_classes([JWTAuthentication])
# def deleteRestaurant(request, restaurant_id: int):
#     restaurant = get_object_or_404(Restaurant, id=restaurant_id)
#
#     if request.method == 'POST':
#         restaurant.delete()
#         messages.success(request, 'Restaurant deleted successfully.')
#         return redirect('list-restaurants')
#     else:
#         return render(request, 'reviews/delete_restaurant.html', {'restaurant': restaurant})
#
#
# # visit
# @api_view(['GET'])
# def getVisits(request):
#     username = request.GET.get('username', '')
#     restaurant_name = request.GET.get('restaurant_name', '')
#
#     query_params = {}
#
#     if username:
#         query_params['customer__username__icontains'] = username
#
#     if restaurant_name:
#         query_params['restaurant__name__icontains'] = restaurant_name
#
#     visits = Visit.objects.filter(**query_params)
#     serializer = VisitSerializer(visits, many=True)
#
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def getVisit(request, visit_id: int):
#     visit = get_object_or_404(Visit, id=visit_id)
#     serializer = VisitSerializer(visit, many=False)
#
#     return Response(serializer.data)
#
#
# @api_view(['GET', 'POST'])
# @authentication_classes([JWTAuthentication])
# def createVisit(request, restaurant_id: int):
#     restaurant = get_object_or_404(Restaurant, id=restaurant_id)
#
#     if request.method == 'POST':
#         customer, created = Customer.objects.get_or_create(username=request.user.username)
#
#         form = VisitForm(request.POST)
#
#         if form.is_valid():
#             visit = form.save(commit=False)
#             visit.customer = customer
#             visit.restaurant = restaurant
#             visit.save()
#             serializer = VisitSerializer(visit)
#             messages.success(request, 'Visit added successfully.')
#             return Response(serializer.data)
#         else:
#             messages.error(request, 'Error in form submission.')
#             print(f"Form errors: {form.errors}")
#             return Response({'detail': 'Error in form submission.'}, status=400)
#
#     else:
#         form = VisitForm()
#
#     return render(request, 'reviews/add_visit.html', {'form': form, 'restaurant': restaurant})
#
#
# @api_view(['GET', 'POST'])
# @authentication_classes([JWTAuthentication])
# def deleteVisit(request, visit_id: int):
#     visit = get_object_or_404(Visit, id=visit_id)
#
#     visit.delete()
#     messages.success(request, 'Visit deleted successfully.')
#     return render(request, 'reviews/user_visits.html')
