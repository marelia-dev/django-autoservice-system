from django.contrib import admin
from .models import Car, Service, Order, OrderLine
from django.utils.html import format_html


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 1
    fields = ('service', 'quantity', 'line_sum')
    readonly_fields = ('line_sum',)

    @admin.display(description="Suma (€)")
    def line_sum(self, obj):
        sum_value = obj.line_sum()
        return f"{sum_value:.2f}" if sum_value > 0 else "-"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('car', 'date', 'display_services', 'total', 'status_colored')
    list_filter = ('date', 'status')
    search_fields = ('car__license_plate', 'car__client_name')

    inlines = [OrderLineInline]

    @admin.display(description="Paslaugos")
    def display_services(self, obj):
        services = [line.service.name for line in obj.order_lines.all()]
        return ", ".join(services) if services else "-"

    @admin.display(description="Viso (€)")
    def total(self, obj):
        total = obj.total()
        return f"{total:.2f}" if total > 0 else "0"

    @admin.display(description="Busena", ordering='status')
    def status_colored(self, obj):
        colors = {
            'new': 'blue',
            'in_progress': 'orange',
            'done': 'green',
            'cancelled': 'red',
            'waiting': 'gray',
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'make', 'model', 'client_name', 'vin_code')
    search_fields = ('license_plate', 'client_name', 'vin_code')
    list_filter = ('client_name', 'make', 'model')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('price',)

@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('order', 'service', 'quantity', 'line_sum_display')
    list_filter = ('order__date', 'service')
    search_fields = ('order__car__license_plate', 'service__name')

    readonly_fields = ('line_sum_display',)

    @admin.display(description="Suma (€)")
    def line_sum(self, obj):
        sum_value = obj.line_sum()
        return f"{sum_value:.2f}" if sum_value > 0 else "0"

    @admin.display(description="Suma (€)")
    def line_sum_display(self, obj):
        sum_value = obj.line_sum()
        return f"{sum_value:.2f}" if sum_value > 0 else "0"


# admin.site.register(Car, CarAdmin)
# admin.site.register(Service)
# admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderLine)

