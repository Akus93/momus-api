from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.compat import is_authenticated


class IsOwnerOrReadOnlyForPost(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author.user == request.user

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user and is_authenticated(request.user)


class IsOwnerOrReadOnlyForUserProfile(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.user == request.user

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user and is_authenticated(request.user)


class IsOwnerForFavorite(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user.userprofile

    def has_permission(self, request, view):
        return request.user and is_authenticated(request.user)


class IsOwnerOrReadOnlyForComment(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user.userprofile

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user and is_authenticated(request.user)


class IsAdminOrCreateOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff or request.method == 'POST'

    def has_permission(self, request, view):
        return request.user and (is_authenticated(request.user) and request.method in ('POST', 'OPTIONS') or
                                 request.user.is_staff)
