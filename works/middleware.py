from uuid import uuid4

from django.utils import timezone

from .models import SiteVisitor


class VisitorTrackingMiddleware:
    """Tracks browser sessions and their latest activity, without IP storage."""

    EXCLUDED_PREFIXES = ("/static/", "/media/", "/admin/")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path
        if not path.startswith(self.EXCLUDED_PREFIXES):
            visitor_key = request.session.get("site_visitor_key")
            if not visitor_key:
                visitor_key = uuid4().hex
                request.session["site_visitor_key"] = visitor_key
            SiteVisitor.objects.update_or_create(
                visitor_key=visitor_key,
                defaults={"last_seen": timezone.now()},
            )
        return response
