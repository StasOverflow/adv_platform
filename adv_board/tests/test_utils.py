from ..models import Announcement, Category, ImagePath
from ..serializers import CategorySerializer, AnnouncementSerializer


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

SAMPLE_FILE_LIST_MODIFIED = (
    'https://farm3.staticflickr.com/2912/12312313981352255_fc59cfdba2_b.jpg',
    'https://homepages.cae.wisc.edu/~ece533/123123images/airplane.png',
    'https://homepages.cae.wisc.edu/~ece533/12images/arctichare.png',
    'https://homepages.cae.wisc.edu/~ece533/1imaggges/baboon.png',
    'https://homepages.cae.wisc.edu/~ece533/123123imagbaaes/boat.png',
    'https://homepages.cae.wisc.edu/~ece533/12imhhages/sails.png',
    'https://homepages.cae.wisc.edu/~ece533/1imagves/monarch.png',
    'https://homepages.cae.wisc.edu/~ece533/gggimag1es/peppers.png'
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

