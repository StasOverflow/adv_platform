from rest_framework.reverse import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from ..models import Announcement, Category, ImagePath
from ..serializers import CategorySerializer, AnnouncementSerializer
from django.db.models import F
import json

from .test_utils import SAMPLE_FILE_LIST, LOREM_CONTENT, create_adv, SAMPLE_FILE_LIST_MODIFIED
from users.tests.test_utils import create_user
import collections


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
        self.base_category = Category.objects.filter(lft=F('rght')-1).first()
        self.test_adv_name = 'Torpedo velosipedo'
        self.leaf_category = Category.objects.create(name='Vintage Bikes', parent=self.base_category)
        self.adv = create_adv(title=self.test_adv_name, category=self.leaf_category,
                              bargain=False, price=5551.55)


class GetAnnouncementsTest(BaseViewTest):
    """
    /api/announcements/     adv_board.views.AnnouncementViewset     adv-list
    /api/announcements/<pk>/        adv_board.views.AnnouncementViewset     adv-detail
    /api/announcements/<pk>/images/ adv_board.views.AnnouncementViewset     adv-images
    /api/announcements/<pk>/images\.<format>/       adv_board.views.AnnouncementViewset     adv-images
    /api/announcements/<pk>\.<format>/      adv_board.views.AnnouncementViewset     adv-detail
    /api/announcements/all_admin    adv_board.views.AnnouncementListView
    /api/announcements\.<format>/   adv_board.views.AnnouncementViewset     adv-list
    """
    def test_get_adv_invalid(self):
        response = self.client.get(
            reverse('adv-detail', kwargs={'pk': self.adv.id+300}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_announcement_parent_categories(self):
        """
        Ensure that we can access a single announcement via its category,
        as well as via parent categories of its category
        """
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

    def test_announcements_get_by_category(self):
        """
        Test category filter
        """
        # create one more leaf category and add an adv to it
        one_more_leaf_category = Category.objects.create(name='Not Bikes', parent=self.base_category)
        not_bikes_adv = create_adv(title=self.test_adv_name, category=one_more_leaf_category,
                                   bargain=False, price=5551.55)
        not_at_all_bikes_adv = create_adv(title='one more', category=one_more_leaf_category,
                                          bargain=False, price=5551.55)
        count_total = Announcement.objects.count()

        # now send get request to filter via certain category
        response = self.client.get(
            reverse('adv-list'),
            data={'category': 'Not Bikes'},
        )
        self.assertNotEqual(count_total, response.data['count'])
        self.assertEqual(count_total, response.data['count'] + 1)
        for item in response.data['results']:
            self.assertIn(item['title'], (self.test_adv_name, 'one more'))
            self.assertEqual(item['category'], one_more_leaf_category.name)

    def test_announcements_get_by_price(self):
        """
        Text max price_limit filter
        """
        # create one more leaf category and add an adv to it
        adv1 = create_adv(title=self.test_adv_name, category=self.leaf_category,
                          bargain=False, price=2000)
        adv2 = create_adv(title='one more', category=self.leaf_category,
                          bargain=False, price=9000)
        adv3 = create_adv(title='one more', category=self.leaf_category,
                          bargain=False, price=6000)

        count_total = Announcement.objects.count()

        # now send get request to filter via price
        response = self.client.get(
            reverse('adv-list'),
            data={'price_limit': 6000.00},
        )

        self.assertNotEqual(count_total, response.data['count'])
        for item in response.data['results']:
            self.assertLessEqual(float(item['price']), 6000.00)


class CRUDAnnouncement(APITestCase):
    """
    Ensure that all crud operations for announcement works
    """

    def setUp(self):
        self.user = create_user(username='Stas', password='ffaass123123g')
        self.another_user = create_user(username='Vyacheslav', password='ffaass123123g')
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
            "title": "mooooody",
            "content": "impossibly dumb content, but modified",
            "price": 2005,
            "bargain": True,
            "category": self.leaf_category.name,
            "images": self.image_list_modified
        }

        self.invalid_payload = {
            "title": "",
            "content": "impossibly dumb content x2",
            "price": 0,
            "bargain": False,
            "category": self.leaf_category.name,
            "images": self.image_list
        }

    def test_create_adv_authenticated(self):
        self.client.force_authenticate(user=self.user)

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

    def test_create_adv_unauth(self):

        ad_num = Announcement.objects.all().count()
        response = self.client.post(
            reverse('adv-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        ad_num_after = Announcement.objects.all().count()
        self.assertEqual(ad_num, ad_num_after)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_adv(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('adv-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        ad_num = Announcement.objects.count()
        ad = Announcement.objects.get(title=self.valid_payload['title'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(
            reverse('adv-detail', kwargs={'pk': ad.id}),
            content_type='application/json'
        )
        self.assertEqual(ad_num, Announcement.objects.count() + 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_adv_unauth_or_not_author(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('adv-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        ad_num = Announcement.objects.count()
        ad = Announcement.objects.get(title=self.valid_payload['title'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.logout()

        response = self.client.delete(
            reverse('adv-detail', kwargs={'pk': ad.id}),
            content_type='application/json'
        )
        self.assertEqual(ad_num, Announcement.objects.count())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.another_user)

        response = self.client.delete(
            reverse('adv-detail', kwargs={'pk': ad.id}),
            content_type='application/json'
        )
        self.assertEqual(ad_num, Announcement.objects.count())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauth_get_announcement(self):
        not_bikes_adv = create_adv(title=self.ad_title, category=self.leaf_category,
                                   bargain=False, price=5551.55)
        response = self.client.get(
            reverse('adv-list'),
        )
        self.assertEqual(response.data['count'], Announcement.objects.filter(is_active=True).count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse('adv-detail', kwargs={'pk': not_bikes_adv.id}),
        )

        expected = Announcement.objects.get(title=not_bikes_adv.title)
        serialized = AnnouncementSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check if authentication doesnt prevent getting an adv
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('adv-detail', kwargs={'pk': not_bikes_adv.id}),
        )

        expected = Announcement.objects.get(title=not_bikes_adv.title)
        serialized = AnnouncementSerializer(expected)
        self.assertNotEqual(response.data['author_id'], self.another_user.id)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_modify_adv(self):
        # as always, create post at first
        self.client.force_authenticate(user=self.user)

        self.client.post(
            reverse('adv-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        created_adv = Announcement.objects.get(title=self.valid_payload['title'])

        # Get a list of images, from the object newly created
        unmodified_paths_list = [image.path for image in created_adv.images.all()]
        response = self.client.put(
            reverse('adv-detail', kwargs={'pk': created_adv.id}),
            data=json.dumps(self.modified_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        image_path_list = [image['path'] for image in response.data['images']]

        self.assertNotEqual(unmodified_paths_list, image_path_list)
        self.assertEqual(collections.Counter(image_path_list),
                         collections.Counter(SAMPLE_FILE_LIST_MODIFIED))
        self.assertEqual(response.data['title'], self.modified_payload['title'])

    def test_modify_adv_unauthenticated(self):
        self.client.force_authenticate(user=self.user)

        self.client.post(
            reverse('adv-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.client.logout()

        # check if unathenticated user cannot modify ad
        created_adv = Announcement.objects.get(title=self.valid_payload['title'])
        response = self.client.put(
            reverse('adv-detail', kwargs={'pk': created_adv.id}),
            data=json.dumps(self.modified_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # also check if another author cant modify adv
        self.client.force_authenticate(user=self.another_user)

        created_adv = Announcement.objects.get(title=self.valid_payload['title'])

        response = self.client.put(
            reverse('adv-detail', kwargs={'pk': created_adv.id}),
            data=json.dumps(self.modified_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

