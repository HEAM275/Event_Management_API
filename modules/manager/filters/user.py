from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters
from modules.manager.models.user import User


class UserFilter(filters.FilterSet):
    """Filter for User model."""
    username = filters.CharFilter(field_name='username', lookup_expr='icontains')
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    is_staff = filters.BooleanFilter(field_name='is_staff')
    is_superuser = filters.BooleanFilter(field_name='is_superuser')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser']
