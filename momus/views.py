from django.contrib.auth.models import User
from rest_framework.views import APIView, Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from momus.permissions import IsOwnerOrReadOnlyForPost, IsOwnerOrReadOnlyForUserProfile
from momus.serializers import UserProfileSerializer, PostSerializer
from momus.models import UserProfile, Post
from momus.filters import PostFilterSet


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all().select_related('user')
    serializer_class = UserProfileSerializer
    permission_classes = (IsOwnerOrReadOnlyForUserProfile, )
    http_method_names = ('get', 'options', 'head', 'delete', 'patch')
    lookup_field = 'user__username'
    lookup_value_regex = '[\w.]+'


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().select_related('author')
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnlyForPost, )
    http_method_names = ('get', 'options', 'post', 'head', 'delete')
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend,)
    filter_class = PostFilterSet

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.userprofile)
