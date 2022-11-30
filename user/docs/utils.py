import os

from django.conf import settings
from drf_spectacular.utils import extend_schema, OpenApiExample, extend_schema_serializer
from django.utils.translation import gettext_lazy as _
from drf_spectacular.views import SpectacularAPIView

EXCLUDE_PATH = settings.SPECTACULAR_SETTINGS["EXCLUDE_PATH"]
ignores = []


def preprocessing_filter_spec(endpoints):
	filtered = []
	for (path, path_regex, method, callback) in endpoints:
		a = ".".join([callback.cls.__module__, callback.cls.__name__])
		if a not in ignores and path not in EXCLUDE_PATH:
			filtered.append((path, path_regex, method, callback))
	return filtered


TAG = "mobile"
mobile_docs = {
	"call": extend_schema(
		tags=[TAG],
		operation_id=_("Call".title()),
		responses={204: None},
		description="API ghi nhận cuộc gọi",
	),

	"billing": extend_schema(
		tags=[TAG],
		operation_id=_("billing".title()),
		description="API hóa đơn (billing)",
		examples=[
			OpenApiExample(
				'Example 1',
				value={"call_count": 3000, "block_count": 10000}
			),
		],
	),

}


def get_md_docs(name):
	path = os.path.join(settings.BASE_DIR, "user", "docs", "md", name)
	with open(path, "r") as f:
		data = f.read()
	return data


def call_doc_serializer():
	return extend_schema_serializer(
		exclude_fields=('single',),  # schema ignore these fields
		examples=[
			OpenApiExample(
				'Call example',
				value={
					"call_duration": 3000
				}
			),
		])


class Spec(SpectacularAPIView):
	doc_page = {
		"REQUIREMENTS": ["Overview"],
		"SPEC": [TAG]
	}

	INSTRUCTION = "REQUIREMENTS"
	sub_instruction = ["Overview"]
	custom_settings = {
		"EXTENSIONS_ROOT": {
			"x-tagGroups": [{"name": INSTRUCTION, "tags": sub_instruction}, {"name": "SPEC", "tags": [TAG]}],
		},
		"TAGS": [
			{"name": sub_instruction[0], "description": get_md_docs("req.md"), "x-traitTag": True},
		]
	}
