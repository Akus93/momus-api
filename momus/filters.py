from django_filters.rest_framework import FilterSet, Filter
from django_filters import CharFilter

from momus.models import Post


class ListFilter(Filter):

    def filter(self, qs, value):
        if not value:
            return qs
        self.lookup_expr = 'contains'
        values = value.split(',')
        return super(ListFilter, self).filter(qs, values)


class PostFilterSet(FilterSet):
    tags = ListFilter(name='tags')
    author = CharFilter(name='author__user__username')

    class Meta:
        model = Post
        fields = ['tags', 'author', 'is_pending']
