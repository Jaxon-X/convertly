from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.models import CustomUser


class AuthFlowTests(APITestCase):
    def test_register_returns_tokens_and_verification_state(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "Jaxon",
                "email": "jaxon@example.com",
                "password": "secret123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertFalse(response.data["is_email_verified"])

    def test_login_returns_tokens_for_existing_user(self):
        CustomUser.objects.create_user(
            username="Jaxon",
            email="jaxon@example.com",
            password="secret123",
        )

        response = self.client.post(
            reverse("login"),
            {
                "email": "jaxon@example.com",
                "password": "secret123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
