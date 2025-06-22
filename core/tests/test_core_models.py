# import pytest
# from core.models import Category

# @pytest.mark.django_db
# def test_category_str_and_user_relation(user):
#     cat = Category.objects.create(user=user, name="Rent")
#     assert str(cat) == "Rent"
#     assert cat.user == user
