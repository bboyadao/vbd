from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularJSONAPIView

from user.docs.utils import get_md_docs, Spec

urlpatterns = [
	path("", include("user.urls")),
	path("admin/", admin.site.urls),
	path("doc", SpectacularRedocView.as_view(), name="redoc"),
	path("api/schema", Spec.as_view(), name="schema"),
	path("api/schema/json", SpectacularJSONAPIView.as_view(), name="schema_json"),
]
