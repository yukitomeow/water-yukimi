from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest
from water.views import top
from django.contrib.auth import get_user_model

from water.models import WaterConsumption


UserModel=get_user_model()

class TopPageRenderWaterTest(TestCase):
    def setUp(self):
        self.user=UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="meowmoewmeow",
        )
        self.water=WaterConsumption.objects.create(
            user=self.user,
            amount_drank=200.1,
        )
    def test_should_return_water_amount_drank(self):
        request=RequestFactory().get("/")
        request.user=self.user
        response=top(request)
        self.assertContains(response, self.water.amount_drank)
    def test_should_return_username(self):
        request=RequestFactory().get("/")
        request.user=self.user
        response=top(request)
        self.assertContains(response, self.user.username)




class TopPageViewTest(TestCase):
    def test_top_returns_200(self):
        response = self.client.get("/")
        self.assertContains(response, "Water log", status_code=200)

    def test_top_returns_expected_content(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "water/top.html")
class TopNewViewTest(TestCase):
    def test_top_returns_200(self):
        response = self.client.get("/water/new/")
        self.assertEqual(response.status_code, 200)

    def test_top_returns_expected_content(self):
        response = self.client.get("/water/new/")
        self.assertEqual(response.content, b"top new")