from rest_framework.reverse import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.tests.test_utils import create_user

from ..models import AdvSiteUser
import json


from adv_platform.urls import urlpatterns


class BaseViewTest(APITestCase):
    """
    /api/users/rest-auth/login/     rest_auth.views.LoginView       rest_login
    /api/users/rest-auth/logout/    rest_auth.views.LogoutView      rest_logout
    /api/users/rest-auth/registration/      rest_auth.registration.views.RegisterView       rest_register
    """
    client = APIClient()
    fixtures = ('category.json', )

    def setUp(self):
        self.user = create_user(username='Stas', password='ffaass123123g')
        self.client = APIClient()

    valid_user_creation_credentials = {
        "username": 'Vitalik',
        "password": "cool_pass",
    }

    valid_user_creation_json = {
        "username": 'Vitalik',
        "password1": valid_user_creation_credentials['password'],
        "password2": valid_user_creation_credentials['password'],
    }


class UserTest(BaseViewTest):

    def test_register_plus_login_plus_logout(self):
        object_num = AdvSiteUser.objects.count()

        response = self.client.post(
            reverse('rest_register'),
            data=json.dumps(self.valid_user_creation_json),
            content_type='application/json'
        )
        object_num_after = AdvSiteUser.objects.count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(object_num + 1, object_num_after)

        response = self.client.post(
            reverse('rest_login'),
            data=json.dumps(self.valid_user_creation_credentials),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            reverse('rest_logout'),
            data="",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_unregistered(self):
        response = self.client.post(
            reverse('rest_login'),
            data=json.dumps(self.valid_user_creation_credentials),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
