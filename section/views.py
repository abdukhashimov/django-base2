from rest_framework import viewsets, mixins
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


from core.models import Service
from section.serializers import ServiceSerializer


class ServiceViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin):
    """Manage services in database"""
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (AllowAny, )
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def perform_create(self, serializer):
        """Creates a new service"""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method == 'GET':
            return (AllowAny(), )
        elif self.request.method == "DELETE":
            return (IsAdminUser(), )
        else:
            return (IsAuthenticated(),)
