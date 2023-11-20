from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from reviews.models import Customer, Restaurant, Review, Visit


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token


class BaseSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.username', read_only=True)
    restaurant = serializers.CharField(source='restaurant.name', read_only=True)

    class Meta:
        abstract = True


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        return obj.created_by.username if obj.created_by else None

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'cuisine', 'address', 'created_by']


class ReviewSerializer(ModelSerializer):
    customer = serializers.CharField(source='customer.username', read_only=True)
    restaurant = serializers.CharField(source='restaurant.name', read_only=True)

    def get_customer(self, obj):
        return obj.customer.username if obj.customer else None

    def get_restaurant(self, obj):
        return obj.restaurant.name if obj.restaurant else None

    class Meta:
        model = Review
        fields = '__all__'


class VisitSerializer(ModelSerializer):
    customer = serializers.CharField(source='customer.username', read_only=True)
    restaurant = serializers.CharField(source='restaurant.name', read_only=True)

    def get_customer(self, obj):
        return obj.customer.username if obj.customer else None

    def get_restaurant(self, obj):
        return obj.restaurant.name if obj.restaurant else None

    class Meta:
        model = Visit
        fields = ['id', 'date', 'spending', 'restaurant', 'customer']
