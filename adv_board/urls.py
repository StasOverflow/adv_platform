from django.urls import path
from .views import AnnouncementViewset, CategoryViewset, AnnouncementListView
# from .views import UserListView
from rest_framework_swagger.views import get_swagger_view
from rest_framework import routers
from django.conf.urls import url, include


schema_view = get_swagger_view(title='Announcements API')

router = routers.DefaultRouter()
router.register(r'announcements', AnnouncementViewset, basename='adv')
router.register(r'categories', CategoryViewset, basename='category')

urlpatterns = [
    path('docs/', schema_view),
    path('', include(router.urls), name='announcements'),
    path('announcements/all_admin', AnnouncementListView.as_view()),
    path('users/', include('users.urls')),
]
