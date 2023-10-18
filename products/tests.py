from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from products.models import Product, Order
from products.serializers import OrderSerializer
from django.test import TestCase


class TestViews(TestCase):
    def setUp(self):
        # Create a test user and authenticate them
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create some sample products
        self.product1 = Product.objects.create(name='Product 1', price=10.99, quantity_in_stock=100)
        self.product2 = Product.objects.create(name='Product 2', price=19.99, quantity_in_stock=50)

    def test_product_list_view(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_list_view_pagination(self):
        for i in range(10):
            Product.objects.create(name=f'Product {i + 3}', price=9.99, quantity_in_stock=20)

        response = self.client.get("/api/products/", {"page": 1, "page_size": 5})  # Use reverse to get the URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 5)  # Assuming only one order is created

    def test_order_create_view(self):
        # Test case for creating an order with sufficient stock
        order_data = {
            'product': self.product1.id,
            'quantity_ordered': 5,
        }
        response = self.client.post('/api/orders/', order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the order was created
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.get()
        self.assertEqual(order.product, self.product1)
        self.assertEqual(order.quantity_ordered, 5)
        # Reassure that the order quantity is substructed from the product stock
        self.assertEqual(order.product.quantity_in_stock, 95)

    def test_order_insufficient_quantity(self):
        # Test case for creating an order with insufficient stock
        order_data = {
            'product': self.product1.id,
            'quantity_ordered': 200,  # Assuming there are only 100 in stock
        }
        response = self.client.post("/api/orders/", order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)  # No new order should be created

    def test_order_non_existing_product(self):
        # Test case for creating an order with a non-existing product
        order_data = {
            'product': 9999,  # Non-existing product ID
            'quantity_ordered': 5,
        }
        response = self.client.post("/api/orders/", order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)  # No new order should be created

    def test_order_history_view(self):
        # Create an order for the test user
        order_data = {
            'product': self.product1.id,
            'quantity_ordered': 3,
        }
        self.client.post("/api/orders/", order_data, format='json')  # Create an order

        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the response contains the expected order data
        expected_data = OrderSerializer(Order.objects.filter(user=self.user), many=True).data
        self.assertEqual(response.data, expected_data)
