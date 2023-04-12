from django.contrib import admin

from .models import Orders,OrderItem


admin.site.register(Orders)
admin.site.register(OrderItem)
