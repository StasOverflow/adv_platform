from rest_framework.reverse import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from ..models import Category
from ..serializers import CategorySerializer
from django.db.models import F
from users.tests.test_utils import create_user


class BaseViewTest(APITestCase):
    client = APIClient()
    fixtures = ('category.json', )

    def setUp(self):
        self.user = create_user(username='Stas', password='ffaass123123g')


class GetCategoriesTest(BaseViewTest):

    def test_get_all_categories(self):
        """
        This test ensures that all categories imported via fixtures
        exist when we make a GET request to the category/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("category-list", kwargs={})
        )
        # fetch the data from db
        expected = Category.objects.all()
        serialized = CategorySerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_leaf_categories(self):
        """
        This test ensures that all leaf-categories imported via fixtures
        exist when we make a GET request to the category/leaves/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("category-leaves", kwargs={})
        )
        # leaf node can be reckognized as left == right - 1
        expected = Category.objects.filter(lft=F('rght')-1)
        serialized = CategorySerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # leaf node should have parent and shouldn't have any children
        for category in response.data:
            self.assertNotEqual(category['parent'], None)
            self.assertEqual(category['children'], [])

    def test_unsupported_methods(self):
        """
        Hit category-related API endpoints one by one, each time using a next
        unsupported method
        """
        self.user = create_user(username='StanislawOverflow', password='ffaass123123g')
        self.client = APIClient()

        endpoints = (
            reverse("category-leaves", kwargs={}),
            reverse("category-list", kwargs={}),
            reverse("category-detail", kwargs={'pk': 1}),
        )

        unsupported_methods = (
            self.client.post,
            self.client.put,
            self.client.patch,
            self.client.delete,
        )

        self.client.force_authenticate(user=self.user)
        for endpoint in endpoints:
            for method in unsupported_methods:
                response = method(endpoint)
                self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
