from django.contrib import admin
from .models import Supplier, Ingredient, Menu, Dish, Table, Order, OrderDish, MenuDish, DishIngredient


class MenuDishInline(admin.TabularInline):
    model = MenuDish
    extra = 1


class DishIngredientInline(admin.TabularInline):
    model = DishIngredient
    extra = 1


class OrderDishInline(admin.TabularInline):
    model = OrderDish
    extra = 1


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier', 'quantity')


class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [MenuDishInline]


class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [DishIngredientInline]


class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'get_dishes')
    inlines = [OrderDishInline]

    def get_dishes(self, obj):
        return ", ".join([str(order_dish.dish) for order_dish in obj.orderdish_set.all()])


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Order, OrderAdmin)
