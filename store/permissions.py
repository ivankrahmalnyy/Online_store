from django.contrib.auth import get_user_model
from rest_framework import permissions

from store.models import Store

User = get_user_model()


class ShopPermission(permissions.BasePermission):
    message = 'Отказано в доступе'

    def has_object_permission(self, request, view, obj: Store):

        return request.user in obj.users.filter(company_id=obj.pk)