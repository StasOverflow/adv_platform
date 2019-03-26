from rest_framework.reverse import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from ..models import Announcement, Category, ImagePath
from ..serializers import CategorySerializer, AnnouncementSerializer
from django.db.models import F
import json

from .test_utils import SAMPLE_FILE_LIST, LOREM_CONTENT, create_adv, SAMPLE_FILE_LIST_MODIFIED


class BaseViewTest(APITestCase):
    client = APIClient()
    fixtures = ('category.json', )

    additional_images = (
        'https://homepages.cae.wisc.edu/~ece533/images/tulips.png',
        'https://homepages.cae.wisc.edu/~ece533/images/watch.png',
        'https://cdn.arstechnica.net/wp-content/uploads/2017/03/GettyImages-461246108-1-800x941.jpg'
    )

    non_image_url = (
        'https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html',
    )

    def setUp(self):
        # create a new leaf category
        base_category = Category.objects.filter(lft=F('rght')-1).first()
        self.test_adv_name = 'Torpedo velosipedo'
        self.leaf_category = Category.objects.create(name='Vintage Bikes', parent=base_category)
        self.adv = create_adv(title=self.test_adv_name, category=self.leaf_category,
                              bargain=False, price=5551.55)


class GetAnnouncementsTest(BaseViewTest):
    """
    Ensure that we can access a single announcement via its category,
    as well as via parent categories of its category
    """
    def test_announcement_parent_categories(self):
        response = self.client.get(
            reverse('adv-detail', kwargs={'pk': self.adv.id}),
        )
        expected = Announcement.objects.get(title=self.test_adv_name)
        serialized = AnnouncementSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # First get all ancestors of a category
        category_ancestors = Category.objects.get(name=response.data['category']).get_ancestors(include_self=True)

        # Then iterate through all categories, checking if object is accessible
        for category in category_ancestors:
            ad = Announcement.objects.get(category__in=category.get_descendants(include_self=True),
                                          title=self.adv.title)
            self.assertEqual(ad, self.adv)


class CreateNewAnnouncement(APITestCase):
    """
    Ensure that all crud operations for announcement works
    """

    def setUp(self):
        self.client = APIClient()
        base_category = Category.objects.filter(lft=F('rght')-1).first()
        self.leaf_category = Category.objects.create(name='brand new category', parent=base_category)

        self.image_list = list()
        for image in SAMPLE_FILE_LIST:
            self.image_list.append({'path': image})

        self.image_list_modified = list()
        for image in SAMPLE_FILE_LIST_MODIFIED:
            self.image_list_modified.append({'path': image})

        self.ad_title = "gourge lukas"

        self.valid_payload = {
            "title": self.ad_title,
            "content": "impossibly dumb content",
            "price": 200,
            "bargain": True,
            "category": self.leaf_category.name,
            "images": self.image_list
        }

        self.modified_payload = {
            "title": self.ad_title,
            "content": "impossibly dumb content, but modified",
            "price": 2005,
            "bargain": True,
            "category": self.leaf_category.name,
            "images": self.image_list
        }

        self.invalid_payload = {
            "title": "",
            "content": "impossibly dumb contentx2",
            "price": 0,
            "bargain": False,
            "category": self.leaf_category.name,
            "images": self.image_list
        }

    def test_create_adv(self):
        ad_num = Announcement.objects.all().count()
        response = self.client.post(
            reverse('adv-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected = Announcement.objects.get(title=self.ad_title)
        serialized = AnnouncementSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(ad_num + 1, Announcement.objects.all().count())

    def test_create_invalid_adv(self):
        response = self.client.post(
            reverse('adv-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_modify_adv(self):
        adv = create_adv(title=self.ad_title, category=self.leaf_category,
                         bargain=False, price=5551.55)
        expected = Announcement.objects.get(title=self.ad_title)
        ad_num = Announcement.objects.all().count()
        response = self.client.put(
            reverse('adv-detail', kwargs={'pk': adv.id}),
            data=json.dumps(self.modified_payload),
            content_type='application/json'
        )
        self.assertEqual(ad_num, Announcement.objects.all().count())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # serialized = AnnouncementSerializer(expected)
        # self.assertEqual(response.data, serialized.data)
        # print(Announcement.objects.get(title=self.ad_title))

    # def test_create_new_adv_successful(self):
    #     ad_num = Announcement.objects.all().count()
    #     test_ad = create_adv(category=self.leaf_category)
    #     # {
    #     #     "title": "string",
    #     #     "content": "string",
    #     #     "price": 0,
    #     #     "bargain": true,
    #     #     "category": "string",
    #     #     "images": [
    #     #         "string"
    #     #     ]
    #     # }
    #     response = self.client.post(
    #         reverse('adv-list', kwargs={'title': 'crud added'})
    #     )
    #
    #     print(response.data)
    #     self.assertEqual(ad_num + 1, Announcement.objects.all().count())
    #
    #     response = self.client.post
    # pass
