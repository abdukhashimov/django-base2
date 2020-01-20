from rest_framework.serializers import ModelSerializer


from core.models import Service


class ServiceSerializer(ModelSerializer):
    """Serializer for service obejcts"""

    class Meta:
        model = Service
        fields = ('id','name', 'title', 'body')
        read_only_fields = ('id', )
