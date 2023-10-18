from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import Order


@receiver(post_save, sender=Order)
def update_product_quantity(sender, instance, created, **kwargs):
    """
    Signal responsible to update the product stock after each order
    """
    if created:
        product = instance.product
        product.quantity_in_stock -= instance.quantity_ordered
        product.save()
