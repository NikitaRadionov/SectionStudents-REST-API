from rest_framework import permissions

class IsModeratorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'MODERATOR')
    

class IsTeacherPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'TEACHER')


class IsStudentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'STUDENT')