from rest_framework.throttling import UserRateThrottle


class UserProfileThrottle(UserRateThrottle):

    rate = '10/h'
    scope = 'userprofile'

    def allow_request(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return super(UserProfileThrottle, self).allow_request(request, view)


class PostThrottle(UserRateThrottle):

    rate = '5/h'
    scope = 'post'

    def allow_request(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return super(PostThrottle, self).allow_request(request, view)


class FavoriteThrottle(UserRateThrottle):

    rate = '25/h'
    scope = 'favorite'

    def allow_request(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return super(FavoriteThrottle, self).allow_request(request, view)


class MessageThrottle(UserRateThrottle):

    rate = '100/h'
    scope = 'message'

    def allow_request(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return super(MessageThrottle, self).allow_request(request, view)
