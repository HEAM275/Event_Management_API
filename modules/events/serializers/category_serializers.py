from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from modules.common.serializer import AuditableSerializerMixin
from modules.events.models.models import Category, Event


# Serializadores para Category
class CategoryListSerializer(AuditableSerializerMixin):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description',
                  'created_date', 'updated_date', 'is_active']


class CategoryCreateSerializer(AuditableSerializerMixin):
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_active']

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError(
                _("El nombre de la categoría es obligatorio."))
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                _("El nombre debe tener al menos 3 caracteres."))
        return value.strip()

    def validate_description(self, value):
        if value and len(value.strip()) < 10:
            raise serializers.ValidationError(
                _("La descripción debe tener al menos 10 caracteres."))
        return value.strip() if value else value

    def validate(self, attrs):
        name = attrs.get('name')
        if Category.objects.filter(name__iexact=name).exists():
            raise serializers.ValidationError({
                'name': _("Ya existe una categoría con este nombre.")
            })
        return attrs


class CategoryUpdateSerializer(AuditableSerializerMixin):
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_active']

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError(
                _("El nombre de la categoría es obligatorio."))
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                _("El nombre debe tener al menos 3 caracteres."))

        # Verificar unicidad excluyendo el objeto actual
        instance = self.instance
        if Category.objects.filter(name__iexact=value).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError(
                _("Ya existe una categoría con este nombre."))
        return value.strip()

    def validate_description(self, value):
        if value and len(value.strip()) < 10:
            raise serializers.ValidationError(
                _("La descripción debe tener al menos 10 caracteres."))
        return value.strip() if value else value

# Serializadores para detalles (opcional)


class CategoryDetailSerializer(AuditableSerializerMixin):
    events_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'events_count',
            'created_date', 'updated_date', 'is_active'
        ]

    def get_events_count(self, obj):
        return obj.events.count()
