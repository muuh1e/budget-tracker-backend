# import pytest
# from core.serializers import CategorySerializer

# @pytest.mark.django_db
# def test_category_serializer_validation(user):
#     data = {"name": "Groceries"}
#     serializer = CategorySerializer(data=data, context={"request": None})
#     assert serializer.is_valid()
#     instance = serializer.save(user=user)
#     assert instance.name == "Groceries"
#     # user must be assigned in save()
#     assert instance.user == user
# #