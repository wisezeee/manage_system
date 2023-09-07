from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from .forms import OrderForm
from .forms import RegistrationForm
from .models import Table, Menu, Order, OrderDish, Supplier
from .serializers import MenuSerializer, SupplierSerializer, OrderDishSerializer


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manageSystem_app:login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required()
def main_page(request):
    return render(request, 'main_page.html')


@login_required()
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})


@login_required()
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_dishes = order.orderdish_set.select_related('dish')
    return render(request, 'order_detail.html', {'order': order, 'order_dishes': order_dishes})


@login_required()
def menu_list(request):
    menus = Menu.objects.all()
    return render(request, 'menu_list.html', {'menus': menus})


@login_required()
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier_list.html', {'suppliers': suppliers})


@login_required()
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            table = form.cleaned_data['table']

            # Проверяем существование столика по объекту Table
            table_object = get_object_or_404(Table, id=table.id)

            order.table = table_object
            order.save()

            dish = form.cleaned_data['dish']
            quantity = form.cleaned_data['quantity']
            OrderDish.objects.create(order=order, dish=dish, quantity=quantity)

            return redirect('manageSystem_app:order_detail', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'order_create.html', {'form': form})


class OrderListCreateAPIView(ListCreateAPIView, LoginRequiredMixin):
    queryset = OrderDish.objects.all()
    serializer_class = OrderDishSerializer

    def post(self, request, *args, **kwargs):
        dish_id = request.POST.get('dish.id')
        order_table = request.POST.get('order.table')
        order_quantity = request.POST.get('order.quantity')

        order = Order(table_id=order_table, quantity=order_quantity)
        order.save()
        order_dish = OrderDish(dish_id=dish_id, order_id=order.id)
        order_dish.save()

        return Response(self.serializer_class(order_dish).data)


class OrderDetailAPIView(RetrieveAPIView, LoginRequiredMixin):
    lookup_field = 'order_id'
    queryset = OrderDish.objects.all()
    serializer_class = OrderDishSerializer


class OrderDeleteAPIView(DestroyAPIView, LoginRequiredMixin):
    lookup_field = 'order_id'
    queryset = OrderDish.objects.all()
    serializer_class = OrderDishSerializer


class MenuListAPIView(ListAPIView, LoginRequiredMixin):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class SupplierListAPIView(ListAPIView, LoginRequiredMixin):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
