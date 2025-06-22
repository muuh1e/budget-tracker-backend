import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from finance.models import Category

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="alice", email="alice@example.com", password="password")


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="bob", email="bob@example.com", password="password")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.fixture
def other_auth_client(other_user):
    client = APIClient()
    client.force_authenticate(other_user)
    return client


def category_list_url():
    return reverse('finance:category-list')


def category_detail_url(pk):
    return reverse('finance:category-detail', args=[pk])


@pytest.mark.django_db
def test_unauthenticated_list_categories_returns_401(api_client):
    url = category_list_url()
    res = api_client.get(url)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_list_categories_only_returns_user(auth_client, user, other_user):
    Category.objects.create(user=user, name="Groceries")
    Category.objects.create(user=other_user, name="Rent")

    url = category_list_url()
    res = auth_client.get(url)

    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['name'] == 'Groceries'
    # 'user' field is hidden in the serializer output
    assert 'user' not in data[0]


@pytest.mark.django_db
def test_create_category(auth_client, user):
    url = category_list_url()
    payload = { 'name': ' utilities ' }
    res = auth_client.post(url, payload)

    assert res.status_code == status.HTTP_201_CREATED
    created = Category.objects.get(user=user, name='utilities')
    assert created.name == 'utilities'
    assert created.user == user
    resp_data = res.json()
    assert resp_data['name'] == 'utilities'
    assert 'user' not in resp_data


@pytest.mark.django_db
def test_duplicate_category_returns_400(auth_client, user):
    Category.objects.create(user=user, name="Bills")
    url = category_list_url()
    payload = { 'name': 'Bills' }
    res = auth_client.post(url, payload)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    errors = res.json()
    all_msgs = []
    for v in errors.values():
        all_msgs.extend(v)
    assert any('already have a category' in msg for msg in all_msgs)


@pytest.mark.django_db
def test_retrieve_category(auth_client, user):
    cat = Category.objects.create(user=user, name="Travel")
    url = category_detail_url(cat.id)
    res = auth_client.get(url)

    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert data['id'] == cat.id
    assert data['name'] == 'Travel'
    # HiddenField 'user' is not returned in representation
    assert 'user' not in data


@pytest.mark.django_db
def test_cannot_retrieve_others_category(auth_client, other_user):
    other_cat = Category.objects.create(user=other_user, name="Other")
    url = category_detail_url(other_cat.id)
    res = auth_client.get(url)
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_category(auth_client, user):
    cat = Category.objects.create(user=user, name="OldName")
    url = category_detail_url(cat.id)
    payload = { 'name': 'NewName' }
    res = auth_client.put(url, payload)

    assert res.status_code == status.HTTP_200_OK
    cat.refresh_from_db()
    assert cat.name == 'NewName'


@pytest.mark.django_db
def test_cannot_update_others_category(auth_client, other_user):
    other_cat = Category.objects.create(user=other_user, name="OtherName")
    url = category_detail_url(other_cat.id)
    payload = { 'name': 'Attempt' }
    res = auth_client.patch(url, payload)
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_category(auth_client, user):
    cat = Category.objects.create(user=user, name="DeleteMe")
    url = category_detail_url(cat.id)
    res = auth_client.delete(url)

    assert res.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(Category.DoesNotExist):
        Category.objects.get(id=cat.id)


@pytest.mark.django_db
def test_cannot_delete_others_category(auth_client, other_user):
    other_cat = Category.objects.create(user=other_user, name="OtherDelete")
    url = category_detail_url(other_cat.id)
    res = auth_client.delete(url)
    assert res.status_code == status.HTTP_404_NOT_FOUND
