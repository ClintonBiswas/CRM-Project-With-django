from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class OrganisoAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organisor:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)