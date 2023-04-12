from django.db import models
from store.models import Products


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6)
    phone = models.CharField(max_length=13, default="")
    country = models.CharField(max_length=13, default="")
    razor_pay_order_id = models.CharField(max_length=1000, null=True, blank=True)
    razor_pay_payment_id = models.CharField(max_length=1000, null=True, blank=True)
    razor_pay_payment_signature = models.CharField(max_length=1000, null=True, blank=True)
    is_paid = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Orders,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Products,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)