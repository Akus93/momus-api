from django_filters.rest_framework import FilterSet, Filter
from django_filters import CharFilter, BooleanFilter

from momus.models import Post, Comment, UserProfile, Message


class ListFilter(Filter):

    def filter(self, qs, value):
        if not value:
            return qs
        self.lookup_expr = 'contains'
        values = value.split(',')
        return super(ListFilter, self).filter(qs, values)


class StartswithFilter(Filter):

    def filter(self, qs, value):
        if not value:
            return qs
        self.lookup_expr = 'startswith'
        return super(StartswithFilter, self).filter(qs, value)


class UserProfileFilter(FilterSet):
    startswith = StartswithFilter(name='user__username')

    class Meta:
        model = UserProfile
        fields = ('startswith', )


class PostFilterSet(FilterSet):
    tags = ListFilter(name='tags')
    author = CharFilter(name='author__user__username')

    class Meta:
        model = Post
        fields = ('tags', 'author', 'is_pending')


class CommentFilterSet(FilterSet):
    author = CharFilter(name='author__user__username')
    post = CharFilter(name='post__slug')

    class Meta:
        model = Comment
        fields = ('author', 'post')

