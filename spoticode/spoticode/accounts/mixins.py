from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class AdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.groups.filter(name='Admin').exists():
            return redirect('unauthorized_access')
        return super().dispatch(request, *args, **kwargs)


class UserCheckMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj == request.user:
            return redirect('unauthorized_access')
        return super().dispatch(request, *args, **kwargs)
