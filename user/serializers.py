from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField
)


class UserCreateSerializer(ModelSerializer):
    """Serializer for only create"""
    token = SerializerMethodField('get_auth_token')

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'token')
        extra_kwargs = {'password': {'write_only': True,
                                     'min_length': 5,
                                     'style': {
                                         'input_type': 'password'
                                     }}}

    def create(self, validated_data):
        """Create a new user with encrypter password"""
        user = get_user_model().objects.create_user(**validated_data)
        return user

    def get_auth_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token


class UserSerializer(ModelSerializer):
    """Serilizers for User objects"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True,
                                     'min_length': 5,
                                     'style': {
                                         'input_type': 'password'
                                     }}}

    def update(self, instance, validated_data):
        """Update a user setting the password correctly"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user
