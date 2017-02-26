from django.db.models import Q
from rest_framework.views import Response, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from momus.permissions import IsOwnerOrReadOnlyForPost, IsOwnerOrReadOnlyForUserProfile, IsOwnerForFavorite,\
                              IsOwnerOrReadOnlyForComment, IsAdminOrCreateOnly
from momus.serializers import UserProfileSerializer, PostSerializer, FavoriteSerializer, CommentSerializer,\
                              MessageSerializer, ReportedPostSerializer, ReportedCommentSerializer,\
                              NotificationSerializer
from momus.models import UserProfile, Post, Favorite, Comment, Message, ReportedPost, ReportedComment, Notification
from momus.filters import PostFilterSet, CommentFilterSet, UserProfileFilter
from momus.throttles import UserProfileThrottle, PostThrottle, FavoriteThrottle, MessageThrottle, CommentThrottle,\
                            ReportedPostThrottle, ReportedCommentThrottle
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
    throttle_classes = (CommentThrottle, )
    http_method_names = ('get', 'options', 'post', 'delete', 'head')
    filter_backends = (DjangoFilterBackend, )
    filter_class = CommentFilterSet

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.userprofile)


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ('get', 'options', 'post', 'head')
    throttle_classes = (MessageThrottle, )
    lookup_field = 'username'
    lookup_value_regex = '[\w.]+'

    def get_queryset(self):
        return Message.objects.filter(Q(sender__user=self.request.user) |
                                      Q(reciver__user=self.request.user)).select_related('sender', 'reciver')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user.userprofile)

    def list(self, request, *args, **kwargs):
        """Lista osób z którymi prowadzono konwersajcę"""
        current_user = request.user.userprofile
        users = UserProfile.objects.filter(Q(sender__reciver=current_user) | Q(reciver__sender=current_user))\
                                   .select_related('user').distinct().order_by('user__first_name')
        return Response(UserProfileSerializer(users, many=True).data)

    def retrieve(self, request, *args, **kwargs):
        """Lista wiadomości z konkretnym użytkownikiem"""
        username = self.kwargs[self.lookup_field]
        current_user = request.user.userprofile
        try:
            other_user = UserProfile.objects.select_related('user').get(user__username=username)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        messages = Message.objects.filter(Q(sender=current_user) | Q(reciver=current_user),
                                          Q(sender=other_user) | Q(reciver=other_user))
        return Response(MessageSerializer(messages, many=True).data)


class UnreadMessagesViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ('get', 'options', 'patch')

    def get_queryset(self):
        return Message.objects.filter(reciver__user=self.request.user, is_read=False).select_related('reciver__user',
                                                                                                     'sender__user')


class ReportedPostViewSet(ModelViewSet):
    queryset = ReportedPost.objects.all()
    serializer_class = ReportedPostSerializer
    permission_classes = (IsAdminOrCreateOnly, )
    http_method_names = ('get', 'options', 'post')
    throttle_classes = (ReportedPostThrottle, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.userprofile)


class ReportedCommentViewSet(ModelViewSet):
    queryset = ReportedComment.objects.all()
    serializer_class = ReportedCommentSerializer
    permission_classes = (IsAdminOrCreateOnly, )
    http_method_names = ('get', 'options', 'post')
    throttle_classes = (ReportedCommentThrottle, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.userprofile)


class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ('get', 'options')

    def get_queryset(self):
        return Notification.objects.filter(user__user=self.request.user)
