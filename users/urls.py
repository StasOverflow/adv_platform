from django.urls import path
from .views import UserListView
# from rest_framework_swagger.views import get_swagger_view
# from django.conf.urls import url, include
#
#
# schema_view = get_swagger_view(title='Announcements API')
#
# router = routers.DefaultRouter()
# router.register(r'announcements', AnnouncementViewset, basename='adv')
# router.register(r'categories', CategoryViewset, basename='category')

urlpatterns = [
    path('', UserListView.as_view()),
]
