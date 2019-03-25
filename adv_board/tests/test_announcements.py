from rest_framework.reverse import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from ..models import Announcement, Category
from ..serializers import CategorySerializer, AnnouncementSerializer
from django.db.models import F


def create_adv(title='Test', category=None,
               bargain=False, price=5551.55,
               content=None,):

    if content is None:
        content = '''Lorem ipsum dolor sit amet, consectetur adipiscing 
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

    return Announcement.objects.create(title=title, category_id=category.id,
                                       bargain=bargain, price=price, content=content, )


class BaseViewTest(APITestCase):
    client = APIClient()
    fixtures = ('category.json', )

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
            reverse('adv-detail', kwargs={'pk': 1}),
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


