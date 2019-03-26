from rest_framework.reverse import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from ..models import Announcement, Category, ImagePath
from ..serializers import CategorySerializer, AnnouncementSerializer
from django.db.models import F
import json


SAMPLE_FILE_LIST = (
    'https://farm3.staticflickr.com/2912/13981352255_fc59cfdba2_b.jpg',
    'https://homepages.cae.wisc.edu/~ece533/images/airplane.png',
    'https://homepages.cae.wisc.edu/~ece533/images/arctichare.png',
    'https://homepages.cae.wisc.edu/~ece533/images/baboon.png',
    'https://homepages.cae.wisc.edu/~ece533/images/boat.png',
    'https://homepages.cae.wisc.edu/~ece533/images/sails.png',
    'https://homepages.cae.wisc.edu/~ece533/images/monarch.png',
    'https://homepages.cae.wisc.edu/~ece533/images/peppers.png'
)


LOREM_CONTENT = '''Lorem ipsum dolor sit amet, consectetur adipiscing 
                     elit. Quisque accumsan ullamcorper leo. Nullam malesuada 
                     elit et laoreet consectetur. Proin sodales ullamcorper 
                     laoreet. Mauris magna ligula, volutpat non est in, sodales 
                     porta mauris. Fusce a convallis mi. Quisque rutrum nisl 
                     quis imperdiet consequat. Nunc efficitur metus sed faucibus 
                     dignissim. Donec pulvinar iaculis pharetra. Pellentesque habitant
                     morbi tristique senectus et netus et malesuada fames ac turpis 
                     egestas. Cras mauris lorem, tempus vitae metus nec, imperdiet 
                     hendrerit nisi. Ut posuere cursus accumsan. Sed eget euismod tellus
                     '''


def create_adv(title='Test', category=None,
               bargain=False, price=5551.55,
               content=None, file_list=None, commit=True):

    if file_list is None:
        file_list = SAMPLE_FILE_LIST

    if content is None:
        content = LOREM_CONTENT

    new_ann = Announcement.objects.create(title=title, category_id=category.id,
                                          bargain=bargain, price=price, content=content)

    image_list = list()
    for path in file_list:
        image_list.append(ImagePath(path=path, announcement_id=new_ann.id))

    ImagePath.objects.bulk_create(image_list)

    return new_ann


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
    """ Test module for inserting a new puppy """

    def setUp(self):
        self.client = APIClient()
        base_category = Category.objects.filter(lft=F('rght')-1).first()
        self.leaf_category = Category.objects.create(name='brand new category', parent=base_category)

        self.image_list = list()
        for image in SAMPLE_FILE_LIST:
            self.image_list.append({'path': image})
        print(self.image_list)

        self.valid_payload = {
            "title": "george lukas",
            "content": "impossibly dumb content",
            "price": 200,
            "bargain": True,
            "category": self.leaf_category.name,
            "images": self.image_list
        }
        # self.invalid_payload = {
        #     'name': '',
        #     'age': 4,
        #     'breed': 'Pamerion',
        #     'color': 'White'
        # }
    """
    Ensure that all crud operations for announcement works
    """
    def test_create_valid_puppy(self):
        response = self.client.post(
            reverse('adv-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        print(json.dumps(self.valid_payload))
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


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
