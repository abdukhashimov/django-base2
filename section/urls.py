from django.urls import path, include
from rest_framework.routers import DefaultRouter

from section.views import ServiceViewSet

router = DefaultRouter()
router.register('services', ServiceViewSet)

app_name='section'

urlpatterns = [
    path('', include(router.urls))
]
