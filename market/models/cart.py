from django.db import models
from market.models import Product


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Quantity')

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
