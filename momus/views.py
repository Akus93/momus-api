from django.contrib.auth.models import User
from rest_framework.views import APIView, Response, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from momus.permissions import IsOwnerOrReadOnlyForPost, IsOwnerOrReadOnlyForUserProfile, IsOwnerForFavorite,\
                              IsOwnerOrReadOnlyForComment
from momus.serializers import UserProfileSerializer, PostSerializer, FavoriteSerializer, CommentSerializer
from momus.models import UserProfile, Post, Favorite, Comment
from momus.filters import PostFilterSet, CommentFilterSet, UserProfileFilter
from momus.throttles import UserProfileThrottle, PostThrottle, FavoriteThrottle
from momus.paginations import LargeResultsSetPagination, StandardResultsSetPagination


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all().select_related('user')
    serializer_class = UserProfileSerializer
    permission_classes = (IsOwnerOrReadOnlyForUserProfile, )
    throttle_classes = (UserProfileThrottle,)
    http_method_names = ('get', 'options', 'head', 'delete', 'patch')
    lookup_field = 'user__username'
    lookup_value_regex = '[\w.]+'
    filter_backends = (DjangoFilterBackend, )
    filter_class = UserProfileFilter
    pagination_class = LargeResultsSetPagination


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().select_related('author')
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnlyForPost, )
    throttle_classes = (PostThrottle, )
    http_method_names = ('get', 'options', 'post', 'head', 'delete')
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, )
    filter_class = PostFilterSet
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.userprofile)


class FavoriteViewSet(ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = (IsOwnerForFavorite, )
    throttle_classes = (FavoriteThrottle, )
    http_method_names = ('get', 'options', 'post', 'delete', 'head')
    lookup_field = 'post__slug'
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile)

    def get_queryset(self):
        return Favorite.objects.filter(user__user=self.request.user).select_related('post')


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.filter(is_active=True)
    permission_classes = (IsOwnerOrReadOnlyForComment, )
    serializer_class = CommentSerializer
    http_method_names = ('get', 'options', 'post', 'delete', 'head')
    filter_backends = (DjangoFilterBackend, )
    filter_class = CommentFilterSet

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.userprofile)
