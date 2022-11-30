import json
import math

from django.conf import settings
from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.core.management import call_command

from user.models import Call, User


class UserViewTests(TestCase):

	def setUp(self):
		self.client = APIClient()
		call_command('mock_user', len=5)
		self.username_test = "test_user_1"
		self.time_dur = 1000

	def test_success_call(self):
		url = reverse("user-call", kwargs={"username": self.username_test})
		data = {
			"call_duration": 1000
		}
		res = self.client.put(url, data=data)
		self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
		call = Call.objects.filter(user=User.objects.get(username=self.username_test)).first()
		self.assertEqual(call.duration, Call.milli_to_second(self.time_dur))

	def test_success_billing(self):
		block = settings.SECS_PER_BLOCK
		user = User.objects.get(username=self.username_test)
		l_dur = [10, 100, 1000, 10000, 100000]
		total_blocks = sum(
			list(
				map(
					lambda x: math.ceil(x / block) if x > block else 1,
					l_dur)
			)
		)

		call = [Call(**{"user": user, "duration": i}) for i in l_dur]
		Call.objects.bulk_create(call)
		self.assertEqual(l_dur.__len__(), Call.objects.count())
		url = reverse("user-billing", kwargs={"username": self.username_test})
		res = self.client.get(url)
		self.assertEqual(json.loads(res.content), {"call_count": l_dur.__len__(), "block_count": total_blocks})
		self.assertEqual(res.status_code, status.HTTP_200_OK)

	def test_success_non_billing(self):
		block = settings.SECS_PER_BLOCK
		user = User.objects.get(username=self.username_test)
		l_dur = [10, 100, 1000, 10000, 100000]
		total_blocks = sum(
			list(
				map(
					lambda x: math.ceil(x / block) if x > block else 1,
					l_dur)
			)
		)
		call = [Call(**{"user": user, "duration": i}) for i in l_dur]
		Call.objects.bulk_create(call)
		self.assertEqual(l_dur.__len__(), Call.objects.count())
		url = reverse("user-billing", kwargs={"username": self.username_test.replace("1", "2")})
		res = self.client.get(url)
		self.assertEqual(json.loads(res.content), {"call_count": 0, "block_count": 0})
		self.assertEqual(res.status_code, status.HTTP_200_OK)
