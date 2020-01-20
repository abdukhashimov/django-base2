from rest_framework import viewsets, mixins
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated


from core.models import Service
from section.serializers import ServiceSerializer


class ServiceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage services in database"""
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (AllowAny, )
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
