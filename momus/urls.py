from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from momus.views import UserProfileViewSet, PostViewSet, FavoriteViewSet, CommentViewSet


router = DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'posts', PostViewSet)
router.register(r'favorites', FavoriteViewSet, 'Favorite')
router.register(r'comments', CommentViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
