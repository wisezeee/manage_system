from datetime import datetime, timezone
from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


def get_datetime():
    return datetime.now(timezone.utc)


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class CreatedMixin(models.Model):
    created = models.DateTimeField(_('created'), default=get_datetime, blank=True, null=False)

    class Meta:
        abstract = True


class ModifiedMixin(models.Model):
    modified = models.DateTimeField(_('modified'), default=get_datetime, blank=True, null=False)

    class Meta:
        abstract = True


class Supplier(UUIDMixin, CreatedMixin, ModifiedMixin):
    name = models.CharField(_('name'), max_length=255)
    address = models.CharField(_('address'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('supplier')
        verbose_name_plural = _('suppliers')


class Ingredient(UUIDMixin, CreatedMixin, ModifiedMixin):
    name = models.CharField(_('name'), max_length=255)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(_('quantity'), default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')


class Menu(UUIDMixin, CreatedMixin, ModifiedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    picture = models.ImageField(_('picture'), upload_to='menu_pictures/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('menu')
        verbose_name_plural = _('menus')


class Dish(UUIDMixin, CreatedMixin, ModifiedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, verbose_name=_('ingredients'), through='DishIngredient')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('dish')
        verbose_name_plural = _('dishes')


class DishIngredient(UUIDMixin, CreatedMixin):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, blank=True, null=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(_('quantity'), default=0)

    class Meta:
        unique_together = (('dish', 'ingredient'),)


class Table(UUIDMixin, CreatedMixin):
    number = models.IntegerField(_('number'))
    capacity = models.PositiveIntegerField(_('capacity'))

    def __str__(self):
        return f'Table {self.number}'

    class Meta:
        ordering = ['number']
        verbose_name = _('table')
        verbose_name_plural = _('tables')


class Order(UUIDMixin, CreatedMixin):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(_('quantity'), default=1)  # Добавлено поле quantity

    def __str__(self):
        return f'Order {self.id}'

    class Meta:
        ordering = ['-created']
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class OrderDish(UUIDMixin, CreatedMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(_('quantity'), default=1)

    class Meta:
        ordering = ['order', 'id']
        unique_together = (('order', 'dish'),)


class MenuDish(UUIDMixin, CreatedMixin):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, blank=True, null=True)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        unique_together = (('menu', 'dish'),)
