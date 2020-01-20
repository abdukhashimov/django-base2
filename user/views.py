from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from user.serializers import UserSerializer, UserCreateSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class CreateUserView(generics.CreateAPIView):
    """Creates a new user in the system"""
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )



class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage authenticated user"""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, )

    def get_object(self):
        """retrive and return authenticated user"""
        return self.request.user
