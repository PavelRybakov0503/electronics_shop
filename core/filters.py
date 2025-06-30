import django_filters
from .models import NetworkNode


class NetworkNodeFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(
        field_name='contact__country',
        lookup_expr='iexact'
    )
    city = django_filters.CharFilter(
        field_name='contact__city',
        lookup_expr='iexact'
    )
    hierarchy_level = django_filters.NumberFilter(
        method='filter_hierarchy_level'
    )

    class Meta:
        model = NetworkNode
        fields = ['node_type', 'country', 'city']

    def filter_hierarchy_level(self, queryset, name, value):
        return queryset.filter(
            node_type=value if value in [0, 1, 2] else 0
        )
