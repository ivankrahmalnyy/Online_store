from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from store.models import Store
from store.permissions import ShopPermission
from store.serializers.store_serializers import StoreSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['location__country']

    def perform_destroy(self, instance: Store):
        with transaction.atomic():
            instance.users.update(is_active=False)
            instance.delete()

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [ShopPermission]
        return [permission() for permission in permission_classes]