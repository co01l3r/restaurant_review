from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from reviews.models import Customer, Restaurant, Review, Visit


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
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

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


class RestaurantSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    pricing_category_eval = serializers.SerializerMethodField()

    def get_created_by(self, obj: Restaurant) -> str or None:
        return obj.created_by.username if obj.created_by else None

    def get_average_rating(self, obj: Restaurant) -> float:
        return obj.average_rating()

    def get_pricing_category_eval(self, obj: Restaurant) -> str or None:
        return obj.get_restaurant_pricing_category_eval()

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'cuisine', 'address', 'created_by', 'average_rating', 'pricing_category_eval']


class ReviewSerializer(ModelSerializer):
    """
    Serializer for the Review model.

    This serializer extends the ModelSerializer from rest_framework and
    is used to serialize/deserialize Review model instances.

    Attributes:
        customer (CharField): A read-only field representing the username of the
            customer who submitted the review.
        restaurant (CharField): A read-only field representing the name of the
            restaurant being reviewed.

    Methods:
        get_customer(obj: Review) -> str or None:
            Custom method to get the username of the customer who submitted the review.

        get_restaurant(obj: Review) -> str or None:
            Custom method to get the name of the restaurant being reviewed.

    Meta:
        model (type): The model class to be serialized/deserialized.
        fields (list or tuple): The fields to include in the serialization.

    """

    customer = serializers.CharField(source='customer.username', read_only=True)
    restaurant = serializers.CharField(source='restaurant.name', read_only=True)

    def get_customer(self, obj: Review) -> str or None:
        """
        Get the username of the customer who submitted the review.

        Args:
            obj (Review): The Review instance.

        Returns:
            str or None: The username of the customer who submitted the review,
            or None if no customer is associated.

        """
        return obj.customer.username if obj.customer else None

    def get_restaurant(self, obj: Review) -> str or None:
        """
        Get the name of the restaurant being reviewed.

        Args:
            obj (Review): The Review instance.

        Returns:
            str or None: The name of the restaurant being reviewed,
            or None if no restaurant is associated.

        """
        return obj.restaurant.name if obj.restaurant else None

    class Meta:
        """
        Metadata class for the ReviewSerializer.

        Attributes:
            model (type): The model class to be serialized/deserialized.
            fields (list or tuple): The fields to include in the serialization.

        """
        model = Review
        fields = '__all__'


class VisitSerializer(ModelSerializer):
    """
    Serializer for the Visit model.

    This serializer extends the ModelSerializer from rest_framework and
    is used to serialize/deserialize Visit model instances.

    Attributes:
        customer (CharField): A read-only field representing the username of the
            customer associated with the visit.
        restaurant (CharField): A read-only field representing the name of the
            restaurant visited during the visit.

    Methods:
        get_customer(obj: Visit) -> str or None:
            Custom method to get the username of the customer associated with the visit.

        get_restaurant(obj: Visit) -> str or None:
            Custom method to get the name of the restaurant visited during the visit.

    Meta:
        model (type): The model class to be serialized/deserialized.
        fields (list or tuple): The fields to include in the serialization.

    """

    customer = serializers.CharField(source='customer.username', read_only=True)
    restaurant = serializers.CharField(source='restaurant.name', read_only=True)

    def get_customer(self, obj: Visit) -> str or None:
        """
        Get the username of the customer associated with the visit.

        Args:
            obj (Visit): The Visit instance.

        Returns:
            str or None: The username of the customer associated with the visit,
            or None if no customer is associated.

        """
        return obj.customer.username if obj.customer else None

    def get_restaurant(self, obj: Visit) -> str or None:
        """
        Get the name of the restaurant visited during the visit.

        Args:
            obj (Visit): The Visit instance.

        Returns:
            str or None: The name of the restaurant visited during the visit,
            or None if no restaurant is associated.

        """
        return obj.restaurant.name if obj.restaurant else None

    class Meta:
        """
        Metadata class for the VisitSerializer.

        Attributes:
            model (type): The model class to be serialized/deserialized.
            fields (list or tuple): The fields to include in the serialization.

        """
        model = Visit
        fields = ['id', 'date', 'spending', 'restaurant', 'customer']
