# import pytest
# from django.contrib.auth import get_user_model
# from rest_framework.test import APIClient

# User = get_user_model()

# @pytest.fixture
# def user(db):
#     return User.objects.create_user(username="alice", email="a@example.com", password="pw")

# @pytest.fixture
# def auth_client(user):
#     client = APIClient()
#     client.force_authenticate(user)
#     return client
