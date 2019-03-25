from django.urls import path
from .views import AnnouncementViewset, CategoryView
from rest_framework_swagger.views import get_swagger_view
from rest_framework import routers
from django.conf.urls import url, include


schema_view = get_swagger_view(title='Announcements API')

router = routers.DefaultRouter()
router.register(r'announcements', AnnouncementViewset)
router.register(r'categories', CategoryView, basename='category')

urlpatterns = router.urls
urlpatterns = [
    path('docs/', schema_view),
    path('', include(router.urls), name='announcements'),
]
