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
