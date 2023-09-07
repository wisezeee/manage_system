from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from .models import OrderDish, Dish, Table, Order


class OrderDishTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', password='test')
        self.client.force_login(user=self.user)

    def test_create_order_dish(self):
        dish = Dish.objects.create(name='Рыба в мясе', description='Ух какая рыбка')
        table = Table.objects.create(number=1, capacity=2)

        url = reverse('manageSystem_app:order_list_api')
        data = {
            'dish.id': f'{dish.id}',
            'order.table': f'{table.id}',
            'order.quantity': 3
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OrderDish.objects.count(), 1)
        self.assertEqual(OrderDish.objects.get().dish.name, 'Рыба в мясе')

    def test_delete_order_dish(self):
        dish = Dish.objects.create(name='Рыба в мясе', description='Ух какая рыбка')
        table = Table.objects.create(number=1, capacity=2)
        order = Order.objects.create(table=table, quantity=2)
        OrderDish.objects.create(dish=dish, order=order, quantity=2)

        url = reverse('manageSystem_app:order_delete_api', kwargs={'order_id': order.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(OrderDish.objects.count(), 0)

    def test_list_order_dish(self):
        url = reverse('manageSystem_app:order_list_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OrderDish.objects.count(), 0)


def create_view_tests(url, page_name, template):
    class ViewTest(TestCase):

        def setUp(self):
            self.user = User.objects.create_user(username='test', password='test')
            self.client.force_login(user=self.user)

        def test_view_exists_at_url(self):
            self.assertEqual(self.client.get(url).status_code, HTTP_200_OK)

        def test_view_exists_by_name(self):
            self.assertEqual(self.client.get(reverse(page_name)).status_code, HTTP_200_OK)

        def test_view_uses_template(self):
            resp = self.client.get(reverse(page_name))
            self.assertEqual(resp.status_code, HTTP_200_OK)
            self.assertTemplateUsed(resp, template)

    return ViewTest


MainPageViewTest = create_view_tests('', 'manageSystem_app:main_page', 'main_page.html')
MenuPageViewTest = create_view_tests(reverse('manageSystem_app:menu_list'), 'manageSystem_app:menu_list', 'menu_list.html')
OrderCreatePageViewTest = create_view_tests(reverse('manageSystem_app:order_create'), 'manageSystem_app:order_create', 'order_create.html')
