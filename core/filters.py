import django_filters
from .models import *

class ShortFilter(django_filters.FilterSet):
    qty_gt = django_filters.NumberFilter(
        field_name='views_qty',
        lookup_expr='gt'
    )

    qty_lt = django_filters.NumberFilter(
        field_name='views_qty',
        lookup_expr='lt'
    )

    class Meta:
        model = Short
        fields = ['user']
