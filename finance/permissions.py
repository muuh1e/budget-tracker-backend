# transactions/permissions.py

from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # for categories: obj.user; for transactions: obj.category.user
        owner = getattr(obj, 'user', None) or getattr(obj, 'category', None).user
        return owner == request.user
