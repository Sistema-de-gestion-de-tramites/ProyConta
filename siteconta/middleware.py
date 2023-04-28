from contextlib import suppress

from django.conf import settings
from django.shortcuts import redirect

NONE_AUTH_ACCOUNT_PATHS = [
    settings.STATIC_URL,
    '/accounts/login/',
    '/accounts/password_reset/',
    '/accounts/reset/',
    '/favicon.ico',
    '/terminal/login/',
    '/terminal/login_failed/',
]


class RequireLoginCheck:
    """Middleware to require authentication on all views by default, except when allowed.

    URLS can be opened by adding them to NONE_AUTH_ACCOUNT_PATHS, or by adding
    the @login_not_required decorator.

    Must appear below the sessions middleware because the sessions middleware
    adds the user to the request, which is used by this middleware.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def _is_none_auth_path(self, path):
        for none_auth_path in NONE_AUTH_ACCOUNT_PATHS:
            if path.startswith(none_auth_path):
                return True
        return False

    def _is_login_not_required(self, view_func):
        with suppress(AttributeError):
            # If a class with the @login_not_required decorator, will return True
            return view_func.view_class.login_not_required
        with suppress(AttributeError):
            # If a function with the @login_not_required decorator, will return True
            return view_func.login_not_required
        return False

    def process_view(self, request, view_func, view_args, view_kwargs):
        """https://docs.djangoproject.com/en/stable/topics/http/middleware/#other-middleware-hooks"""
        if not (
            request.user.is_authenticated
            or self._is_login_not_required(view_func)
            or self._is_none_auth_path(request.path)
        ):
            if settings.LOGIN_URL != request.path:
                # if next URL after login is the same login URL, then cyclic loop
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
            else:
                return redirect('%s?next=%s' % (settings.LOGIN_URL, '/'))
        return None