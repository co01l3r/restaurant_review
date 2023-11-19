from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer
from reviews.models import Customer, Restaurant, Review, Visit


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class VisitSerializer(ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'
