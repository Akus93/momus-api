from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from momus.views import UserProfileViewSet, PostViewSet, FavoriteViewSet, CommentViewSet, MessageViewSet,\
                        UnreadMessagesViewSet, ReportedPostViewSet, ReportedCommentViewSet


router = DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'posts', PostViewSet)
router.register(r'favorites', FavoriteViewSet, 'Favorite')
router.register(r'comments', CommentViewSet)
router.register(r'messages/unread', UnreadMessagesViewSet, 'UnreadMessage')
router.register(r'messages', MessageViewSet, 'Message')
router.register(r'reported-posts', ReportedPostViewSet)
router.register(r'reported-comment', ReportedCommentViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
