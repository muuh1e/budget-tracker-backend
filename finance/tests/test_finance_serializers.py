import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from finance.models import Category
from finance.serializers import CategorySerializer

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="alice", email="a@example.com", password="pw")


@pytest.fixture
def factory():
    return APIRequestFactory()


def make_serializer(data, user, factory):
    request = factory.post("/fake-url/", data)
    request.user = user
    return CategorySerializer(data=data, context={"request": request})


@pytest.mark.django_db
def test_creates_category_and_assigns_user(user, factory):
    data = {"name": "Groceries"}
    serializer = make_serializer(data, user, factory)
    assert serializer.is_valid(), serializer.errors
    category = serializer.save()
    assert category.name == "Groceries"
    assert category.user == user


@pytest.mark.django_db
def test_trims_whitespace_from_name(user, factory):
    data = {"name": "  Utilities  "}
    serializer = make_serializer(data, user, factory)
    assert serializer.is_valid(), serializer.errors
    category = serializer.save()
    assert category.name == "Utilities"


@pytest.mark.django_db
def test_blank_name_not_allowed(user, factory):
    serializer = make_serializer({"name": ""}, user, factory)
    assert not serializer.is_valid()
    assert "name" in serializer.errors
    # DRF default message for blank field
    assert any("blank" in msg.lower() for msg in serializer.errors["name"])


@pytest.mark.django_db
def test_name_max_length(user, factory):
    long_name = "x" * 101
    serializer = make_serializer({"name": long_name}, user, factory)
    assert not serializer.is_valid()
    assert "name" in serializer.errors
    assert any("no more than 100 characters" in msg for msg in serializer.errors["name"])


@pytest.mark.django_db
def test_prevents_duplicate_names_for_same_user(user, factory):
    # pre-create a category with this name
    Category.objects.create(user=user, name="Rent")
    serializer = make_serializer({"name": "Rent"}, user, factory)
    assert not serializer.is_valid()

    # collect all error messages, regardless of field
    all_errors = []
    for field_errors in serializer.errors.values():
        all_errors.extend(field_errors)

    assert "You already have a category with this name." in all_errors

@pytest.mark.django_db
def test_allows_same_name_for_different_users(user, factory):
    other = User.objects.create_user(username="bob", email="b@b.com", password="pw")
    Category.objects.create(user=other, name="Rent")
    # our user can still create "Rent"
    serializer = make_serializer({"name": "Rent"}, user, factory)
    assert serializer.is_valid(), serializer.errors
