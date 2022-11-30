from django.conf import settings
from django.db.models import Sum, F, Case, When, Value, IntegerField
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from django.db.models.functions import Ceil
from user.models import Call
from django.utils.translation import gettext_lazy as _
from user.docs.utils import call_doc_serializer


@call_doc_serializer()
class CallSerializer(serializers.ModelSerializer):
	call_duration = serializers.IntegerField(
		source='duration',
		min_value=0,
		help_text=_("một số nguyên mô tả thời gian cuộc gọi tính bằng millisecond")
	)

	class Meta:
		model = Call
		fields = ["call_duration"]

	def validate_call_duration(self, val):  # noqa
		return Call.milli_to_second(val)

	def create(self, validated_data):
		user = self.context.get("user")
		validated_data.update(user=user)
		return super().create(validated_data)


class BillSerializer(serializers.Serializer):
	call_count = serializers.SerializerMethodField(help_text=_("tổng số cuộc gọi user đã có"))
	block_count = serializers.SerializerMethodField(help_text=_("tổng số block của user"))

	class Meta:
		fields = ["call_count", "block_count"]

	@staticmethod
	@extend_schema_field(OpenApiTypes.NUMBER)
	def get_call_count(instance) -> int:
		return instance.call_set.count()

	@staticmethod
	@extend_schema_field(OpenApiTypes.NUMBER)
	def get_block_count(instance) -> int:
		return instance.call_set.annotate(dur=F('duration')).annotate(
			blocks=Case(
				When(dur__lte=settings.SECS_PER_BLOCK, then=Value(1)),
				When(dur__gt=settings.SECS_PER_BLOCK, then=Ceil(F('dur') / settings.SECS_PER_BLOCK)),
				output_field=IntegerField()
			)
		).aggregate(Sum('blocks')).get("blocks__sum") or 0
