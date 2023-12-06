from decimal import Decimal
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from reviews.models import Customer, Restaurant, Review, Visit
from reviews.utils import calculate_user_total_spending_at_restaurant


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom Token Obtain Pair Serializer with additional custom claims.

    This serializer extends the default TokenObtainPairSerializer from
    rest_framework_simplejwt and adds custom claims to the token.

    Attributes:
        user (AbstractUser): The user for whom the token is obtained.

    Methods:
        get_token(user: AbstractUser) -> AccessToken:
            Override the parent class method to add custom claims to the token.
    """
    @classmethod
    def get_token(cls, user):
        """
        Override the parent class method to add custom claims to the token.

        Args:
            user (AbstractUser): The user for whom the token is obtained.

        Returns:
            AccessToken: The token with additional custom claims.

        """
        token = super().get_token(user)

        return token


class CustomerSerializer(ModelSerializer):
    """
    Serializer for the Customer model.

    This serializer extends the ModelSerializer from rest_framework and
    is used to serialize/deserialize Customer model instances.

    Attributes:
        Meta:
            model (type): The model class to be serialized/deserialized.
            fields (list or tuple): The fields to include in the serialization.

    """

    class Meta:
        """
        Metadata class for the CustomerSerializer.

        Attributes:
            model (type): The model class to be serialized/deserialized.
            fields (list or tuple): The fields to include in the serialization.

        """
        model = Customer
        fields = '__all__'


class RestaurantSerializer(ModelSerializer):
    """
    Serializer for the Restaurant model.

    Attributes:
        - created_by (int or None): The ID of the user who created the restaurant.
        - average_rating (float): The average rating of the restaurant.
        - pricing_category_eval (str or None): The evaluation of the pricing category for the restaurant.

    Meta:
        - model (Restaurant): The Restaurant model.
        - fields (list): List of fields to include in the serialized output.
    """
    created_by = serializers.SerializerMethodField()
    pricing_category_eval = serializers.SerializerMethodField()
    average_rating = serializers.FloatField(read_only=True)

    def get_created_by(self, obj: Restaurant) -> int or None:
        return obj.created_by.id if obj.created_by else None

    def get_pricing_category_eval(self, obj: Restaurant) -> str or None:
        return obj.get_restaurant_pricing_category_eval()

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'cuisine', 'address', 'created_by', 'average_rating', 'pricing_category_eval']


class ReviewSerializer(ModelSerializer):
    """
    Serializer for the Review model.

    Meta:
        - model (Review): The Review model.
        - fields (str or list): Fields to include in the serialized output. Use '__all__' to include all fields.
    """
    class Meta:
        model = Review
        fields = ['id', 'restaurant', 'customer', 'created', 'rating', 'pricing', 'comment']


class VisitSerializer(ModelSerializer):
    """
    Serializer for the Visit model.

    Attributes:
        - total_spending_at_restaurant (float): The total spending of the customer at the visited restaurant.

    Methods:
        - get_total_spending_at_restaurant(obj: Visit) -> float: Returns the total spending at the visited restaurant.

    Meta:
        - model (Visit): The Visit model.
        - fields (list): List of fields to include in the serialized output.
    """
    total_spending_at_restaurant = serializers.SerializerMethodField()

    def get_total_spending_at_restaurant(self, obj: Visit) -> Decimal:
        user = obj.customer
        restaurant = obj.restaurant
        total_spending = calculate_user_total_spending_at_restaurant(user, restaurant)
        return total_spending

    class Meta:
        """
        Metadata class for the VisitSerializer.

        Attributes:
            model (type): The model class to be serialized/deserialized.
            fields (list or tuple): The fields to include in the serialization.

        """
        model = Visit
        fields = ['id', 'date', 'spending', 'restaurant', 'customer', 'total_spending_at_restaurant']
