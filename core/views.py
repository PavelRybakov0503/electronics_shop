from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import NetworkNode
from .serializers import NetworkNodeSerializer, NetworkNodeListSerializer
from .filters import NetworkNodeFilter


class IsActiveEmployeePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'employee')
            and request.user.employee.is_active
        )


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all().select_related(
        'contact', 'supplier'
    ).prefetch_related('products')
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployeePermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NetworkNodeFilter
    search_fields = ['name', 'contact__country', 'contact__city']
    ordering_fields = ['created_at', 'debt', 'hierarchy_level']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return NetworkNodeListSerializer
        return NetworkNodeSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        # Убедимся, что debt не обновляется через API
        if 'debt' in serializer.validated_data:
            del serializer.validated_data['debt']
        serializer.save()
