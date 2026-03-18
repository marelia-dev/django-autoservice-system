from django.contrib import admin
from .models import Car, Service, Order, Order_line

admin.site.register(Car)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Order_line)

