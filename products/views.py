from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from products.models import Product, Order
from products.serializers import ProductSerializer, OrderSerializer


class ProductListView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = PageNumberPagination
    page_size = 5


class OrderCreateListView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = None

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create an Order

        Function overrides create method of CreateApiView and extents its functionality
        by:

        - Checking if the requested product exists
        - Checking if the requested product stock is sufficient
        """
        order_data = request.data
        product_id = order_data.get('product')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the quantity ordered is greater than the quantity in stock
        quantity_ordered = order_data.get('quantity_ordered', 0)
        if quantity_ordered > product.quantity_in_stock:
            return Response({'detail': 'Insufficient stock for the order'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

