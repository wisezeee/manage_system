from rest_framework import serializers

from .models import Order, Menu, Supplier, Dish, OrderDish


class DishSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all())

    class Meta:
        model = Dish
        fields = ['id', 'name', ]
        read_only_fields = ['name', ]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'table', 'quantity', ]


class OrderDishSerializer(serializers.ModelSerializer):
    dish = DishSerializer()
    order = OrderSerializer()

    class Meta:
        model = OrderDish
        fields = ['dish', 'order']


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
