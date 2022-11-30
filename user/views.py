from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from user.docs.utils import mobile_docs
from user.serializers import CallSerializer, BillSerializer
from user.models import User
from drf_spectacular.utils import extend_schema_view


@extend_schema_view(**mobile_docs)
class UserView(GenericViewSet):
	serializer_class = BillSerializer
	queryset = User.objects.all()
	lookup_field = 'username'

	@property
	def get_user(self) -> User:
		username = self.kwargs.get("username")
		return User.objects.get(username=username)

	def get_serializer_context(self):
		context = super().get_serializer_context()
		context.update(user=self.get_user)
		return context

	@action(detail=True, methods=["PUT"], serializer_class=CallSerializer)
	def call(self, *args, **kwargs):
		serializer = self.get_serializer(data=self.request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save(**serializer.validated_data)
			return Response(status=status.HTTP_204_NO_CONTENT)

		raise APIException()

	@action(detail=True, methods=["GET"], serializer_class=BillSerializer)
	def billing(self, *args, **kwargs):
		instance = self.get_object()
		serializer = self.get_serializer(instance)
		return Response(serializer.data)
