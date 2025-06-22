import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import IntegrityError
from django.utils import timezone
from finance.models import Category

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="alice", email="a@example.com", password="pw")


@pytest.mark.django_db
def test_str_returns_name_with_trailing_spaces(user):
    cat = Category.objects.create(user=user, name="Rent")
    assert str(cat) == "Rent  "


@pytest.mark.django_db
def test_unique_together_constraint_db_level(user):
    Category.objects.create(user=user, name="Rent")
    with pytest.raises(IntegrityError):
        Category.objects.create(user=user, name="Rent")


@pytest.mark.django_db
def test_full_clean_duplicate_name_raises_validation_error(user):
    Category.objects.create(user=user, name="Rent")
    dup = Category(user=user, name="Rent")
    with pytest.raises(ValidationError) as exc:
        dup.full_clean()
    errors = exc.value.message_dict
    # There should be at least one validation error raised
    assert errors, "Expected full_clean() to produce validation errors"
    # And it should be either a non‐field (__all__) error or attached to 'name'
    assert NON_FIELD_ERRORS in errors or 'name' in errors


@pytest.mark.django_db
def test_related_name_on_user(user):
    cat = Category.objects.create(user=user, name="Budget")
    assert cat in user.categories.all()


@pytest.mark.django_db
def test_timestamps_auto_set(user):
    before = timezone.now()
    cat = Category.objects.create(user=user, name="Travel")
    after = timezone.now()
    assert before <= cat.created_at <= after
    assert before <= cat.updated_at <= after


def test_name_field_max_length():
    field = Category._meta.get_field("name")
    assert field.max_length == 100
