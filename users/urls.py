from django.urls import path
from .views import UserListView, UserAddToFavsView, UserAddToFavsView
from django.conf.urls import url, include


urlpatterns = [
    path('', UserListView.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    # path('user_bookmarks/<user_id>', UserAddToFavsView.as_view()),
]
