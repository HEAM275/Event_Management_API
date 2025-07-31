from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from modules.common.models import AuditableMixins


class Category(AuditableMixins):
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_("Nombre de la categoría")
    )
    description = models.TextField(
        blank=True,
        help_text=_("Descripción detallada de la categoría")
    )
    is_active = models.BooleanField(default=True, help_text=_(
        "Indica si la categoría está activa"), null=False, blank=False)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(AuditableMixins):
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_("Nombre del evento")
    )
    description = models.TextField(
        blank=True,
        help_text=_("Descripción detallada del evento")
    )
    capacity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("Capacidad máxima de asistentes")
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='events',
        help_text=_("Categoría a la que pertenece el evento")
    )
    start_date = models.DateField(help_text=_("Fecha de inicio del evento"))
    end_date = models.DateField(help_text=_(
        "Fecha de finalización del evento"))
    start_time = models.TimeField(help_text=_("Hora de inicio del evento"))
    end_time = models.TimeField(help_text=_("Hora de finalización del evento"))
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Ubicación del evento")
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_("Precio del evento en la moneda local")
    )
    is_active = models.BooleanField(default=True, help_text=_(
        "Indica si la categoría está activa"), null=False, blank=False)

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['name']
        indexes = [
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f'{self.name} ({self.start_date})'

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError({
                'end_date': _('La fecha de inicio no puede ser posterior a la fecha de fin.')
            })

        if (self.start_time and self.end_time and
            self.start_date == self.end_date and
                self.start_time > self.end_time):
            raise ValidationError({
                'end_time': _('La hora de inicio no puede ser posterior a la hora de fin.')
            })
