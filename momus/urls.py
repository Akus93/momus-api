from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from momus.views import UserProfileViewSet, PostViewSet


router = DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
