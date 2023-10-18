from rest_framework import serializers
from products.models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity_in_stock']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    def to_internal_value(self, data):
        data["user"] = self.context["request"].user.id
        return super().to_internal_value(data)
