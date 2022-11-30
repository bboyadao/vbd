from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from drf_spectacular.views import SpectacularRedocView, SpectacularJSONAPIView
from django.conf.urls.static import static
from user.docs.utils import Spec

urlpatterns = [
	path("", include("user.urls")),
	path("admin/", admin.site.urls),
	path("doc", SpectacularRedocView.as_view(), name="redoc"),
	path("api/schema", Spec.as_view(), name="schema"),
	path("api/schema/json", SpectacularJSONAPIView.as_view(), name="schema_json"),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
