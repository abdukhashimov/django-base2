from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Service
from section.serializers import ServiceSerializer

SERIVICES_URL = reverse('section:service-list')


class PublicServicesAPITests(TestCase):
    """Test the publicly available services API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@greatsoft.uz',
            password='password',
        )
    def test_login_is_not_required(self):
        res = self.client.get(SERIVICES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrive_services(self):
        """Test retriving tags"""
        Service.objects.create(
            user=self.user, name='some name', title='some title',
            body='some body')
        Service.objects.create(
            user=self.user, name='some name1', title='some title1',
            body='some body1',)
        Service.objects.create(
            user=self.user, name='some name2', title='some title2',
            body='some body2')

        res = self.client.get(SERIVICES_URL)
        services = Service.objects.all()
        service_serialized = ServiceSerializer(services, many=True)
        self.assertEqual(res.data, service_serialized.data)


class PrivateServicesAPITests(TestCase):
    """Test the authenticated available services API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@greatsoft.uz',
            password='password',
        )
        self.client = APIClient()
        self.client.force_authenticate(user)
