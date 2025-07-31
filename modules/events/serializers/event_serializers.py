from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from modules.common.serializer import AuditableSerializerMixin
from modules.events.models.models import Event


class EventListSerializer(AuditableSerializerMixin):
    category_name = serializers.CharField(
        source='category.name', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'description', 'start_date', 'end_date',
            'location', 'price', 'category', 'category_name',
            'created_date', 'updated_date', 'is_active'
        ]


class EventDetailSerializer(AuditableSerializerMixin):
    category_name = serializers.CharField(
        source='category.name', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'description', 'capacity', 'category', 'category_name',
            'start_date', 'end_date', 'start_time', 'end_time',
            'location', 'price', 'created_date', 'updated_date', 'is_active'
        ]


class EventCreateSerializer(AuditableSerializerMixin):
    class Meta:
        model = Event
        fields = [
            'name', 'description', 'capacity', 'category',
            'start_date', 'end_date', 'start_time', 'end_time',
            'location', 'price', 'is_active'
        ]

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError(
                _("El nombre del evento es obligatorio."))
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                _("El nombre debe tener al menos 5 caracteres."))
        return value.strip()

    def validate_description(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError(
                _("La descripción del evento es obligatoria."))
        if len(value.strip()) < 20:
            raise serializers.ValidationError(
                _("La descripción debe tener al menos 20 caracteres."))
        return value.strip()

    def validate_capacity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                _("La capacidad no puede ser negativa."))
        if value == 0:
            raise serializers.ValidationError(
                _("La capacidad debe ser mayor que 0."))
        return value

    def validate_category(self, value):
        if not value:
            raise serializers.ValidationError(
                _("Debe seleccionar una categoría."))
        return value

    def validate_start_date(self, value):
        if not value:
            raise serializers.ValidationError(
                _("La fecha de inicio es obligatoria."))
        return value

    def validate_end_date(self, value):
        if not value:
            raise serializers.ValidationError(
                _("La fecha de finalización es obligatoria."))
        return value

    def validate_start_time(self, value):
        if not value:
            raise serializers.ValidationError(
                _("La hora de inicio es obligatoria."))
        return value

    def validate_end_time(self, value):
        if not value:
            raise serializers.ValidationError(
                _("La hora de finalización es obligatoria."))
        return value

    def validate_price(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                _("El precio no puede ser negativo."))
        return value

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        name = attrs.get('name')

        # Validar fechas
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({
                'end_date': _("La fecha de inicio no puede ser posterior a la fecha de finalización.")
            })

        # Validar horas si las fechas son iguales
        if (start_date and end_date and start_time and end_time and
                start_date == end_date and start_time > end_time):
            raise serializers.ValidationError({
                'end_time': _("La hora de inicio no puede ser posterior a la hora de finalización.")
            })

        # Validar unicidad del nombre
        if Event.objects.filter(name__iexact=name).exists():
            raise serializers.ValidationError({
                'name': _("Ya existe un evento con este nombre.")
            })

        return attrs


class EventUpdateSerializer(AuditableSerializerMixin):
    class Meta:
        model = Event
        fields = [
            'name', 'description', 'capacity', 'category',
            'start_date', 'end_date', 'start_time', 'end_time',
            'location', 'price', 'is_active'
        ]

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError(
                _("El nombre del evento es obligatorio."))
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                _("El nombre debe tener al menos 5 caracteres."))

        # Verificar unicidad excluyendo el objeto actual
        instance = self.instance
        if Event.objects.filter(name__iexact=value).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError(
                _("Ya existe un evento con este nombre."))
        return value.strip()

    def validate_description(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError(
                _("La descripción del evento es obligatoria."))
        if len(value.strip()) < 20:
            raise serializers.ValidationError(
                _("La descripción debe tener al menos 20 caracteres."))
        return value.strip()

    def validate_capacity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                _("La capacidad no puede ser negativa."))
        if value == 0:
            raise serializers.ValidationError(
                _("La capacidad debe ser mayor que 0."))
        return value

    def validate_category(self, value):
        if not value:
            raise serializers.ValidationError(
                _("Debe seleccionar una categoría."))
        return value

    def validate_start_date(self, value):
        if not value:
            raise serializers.ValidationError(
                _("La fecha de inicio es obligatoria."))
        return value

    def validate_end_date(self, value):
        if not value:
            raise serializers.ValidationError(
                _("La fecha de finalización es obligatoria."))
        return value

    def validate_start_time(self, value):
        if not value:
            raise serializers.ValidationError(
                _("La hora de inicio es obligatoria."))
        return value

    def validate_end_time(self, value):
        if not value:
            raise serializers.ValidationError(
                _("La hora de finalización es obligatoria."))
        return value

    def validate_price(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                _("El precio no puede ser negativo."))
        return value

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        name = attrs.get('name')
        instance = self.instance

        # Validar fechas
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({
                'end_date': _("La fecha de inicio no puede ser posterior a la fecha de finalización.")
            })

        # Validar horas si las fechas son iguales
        if (start_date and end_date and start_time and end_time and
                start_date == end_date and start_time > end_time):
            raise serializers.ValidationError({
                'end_time': _("La hora de inicio no puede ser posterior a la hora de finalización.")
            })

        # Validar unicidad del nombre excluyendo el objeto actual
        if Event.objects.filter(name__iexact=name).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError({
                'name': _("Ya existe un evento con este nombre.")
            })

        return attrs
