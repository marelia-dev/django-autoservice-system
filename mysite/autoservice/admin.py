from django.contrib import admin
from .models import Car, Service, Order, OrderLine, OrderReview, CustomUser
from django.utils.html import format_html
from django.utils import timezone
from django.contrib.auth.admin import UserAdmin


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 1
    fields = ('service', 'quantity', 'line_sum')
    readonly_fields = ('line_sum',)

    @admin.display(description="Suma (€)")
    def line_sum(self, obj):
        sum_value = obj.line_sum()
        return f"{sum_value:.2f}" if sum_value > 0 else "-"

class OrderReviewInline(admin.TabularInline):
    model = OrderReview
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('car', 'reader_display', 'reader', 'date', 'due_back', 'is_overdue_colored', 'status_colored', 'total', 'display_services')
    list_filter = ('status', 'date', 'due_back')
    list_editable = ('reader', 'due_back',)
    autocomplete_fields = ('reader',)
    search_fields = ('car__license_plate', 'car__client_name', 'reader__username')
    inlines = [OrderLineInline, OrderReviewInline]

    @admin.display(description="Vartotojas", ordering='reader__username')
    def reader_display(self, obj):
        if obj.reader:
            return obj.reader.username
        return "—"

    @admin.display(description="Terminas praėjęs?", boolean=True)
    def is_overdue_colored(self, obj):
        return obj.is_overdue()

    @admin.display(description="Būsena", ordering='status')
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

    @admin.display(description="Paslaugos")
    def display_services(self, obj):
        services = [line.service.name for line in obj.order_lines.all()]
        return ", ".join(services) if services else "-"

    @admin.display(description="Viso (€)")
    def total(self, obj):
        total_value = obj.total
        return f"{total_value:.2f}" if total_value > 0 else "0.00"

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

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        overdue_ids = Order.objects.filter(
            due_back__lt=timezone.now().date()
        ).values_list('pk', flat=True)

        extra_context['overdue_order_ids'] = list(overdue_ids)

        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'make', 'model', 'client_name', 'vin_code', 'cover')
    search_fields = ('license_plate', 'client_name', 'vin_code')
    list_filter = ('client_name', 'make', 'model')

    def cover(self, obj):
        if obj.cover:
            return format_html('<img src="{}" width="50" height="50" />', obj.cover.url)
        return "-"
    cover.short_description = 'Nuotrauka'

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


@admin.register(OrderReview)
class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ('order', 'date_created', 'reviewer', 'content')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'photo_tag', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    def photo_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.photo.url)
        return "—"

    photo_tag.short_description = 'Nuotrauka'

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personaline informacija', {'fields': ('first_name', 'last_name', 'email', 'photo')}),
        ('Teises', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Svarbios datos', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'photo'),
        }),
    )
