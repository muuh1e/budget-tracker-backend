from rest_framework import permissions 
from .models import User
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Safe methods:
        if request.method in permissions.SAFE_METHODS:
            return True
        # Admin users can modify dataa
        return bool(request.user and request.user.is_staff)
    
class IsNotBlocked(permissions.BasePermission):
    """
    Custom permission to only allow non-blocked users to access the view.
    """
    def has_permission(self, request, view):
        # Allow access if the user is not blocked
        return request.user and not request.user.is_blocked
    
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.ROLE_ADMIN

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.ROLE_MANAGER

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.ROLE_USER
    
class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow access if the user is the owner of the object OR admin
        if request.user.is_staff or request.user.role == User.ROLE_ADMIN:
            return True
        return obj == request.user
