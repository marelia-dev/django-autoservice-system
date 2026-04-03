from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField


class CustomUser(AbstractUser):
    """Custom user for AutoService project"""

    photo = models.ImageField(
        upload_to="profile_pics/",
        null=True,
        blank=True,
        verbose_name=_("Profile photo")
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        db_table = 'auth_user'

    def __str__(self):
        return self.username


class Service(models.Model):
    """Auto service offered services"""

    name = models.CharField(max_length=150, verbose_name=_("Service name"))
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_("Price (€)"))

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Car(models.Model):
    """Customer's car"""

    make = models.CharField(max_length=100, verbose_name=_("Make"))
    model = models.CharField(max_length=100, verbose_name=_("Model"))
    license_plate = models.CharField(max_length=50, verbose_name=_("License plate"), unique=True)
    vin_code = models.CharField(max_length=17, verbose_name=_("VIN code"), unique=True, blank=True, null=True)
    client_name = models.CharField(max_length=150, verbose_name=_("Client"))
    cover = models.ImageField(_("Photo"), upload_to="covers/", null=True, blank=True)
    description = HTMLField(verbose_name=_("Description"), max_length=3000, default="")

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")
        ordering = ["license_plate"]

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"


class Order(models.Model):
    """Service order"""

    car = models.ForeignKey(Car, on_delete=models.PROTECT, verbose_name=_("Car"))
    date = models.DateTimeField(default=timezone.now, verbose_name=_("Order date and time"))
    reader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                               verbose_name=_("User"), null=True, blank=True)
    due_back = models.DateField(verbose_name=_("Due back date"), null=True, blank=True)

    STATUS_CHOICES = (
        ('new', _('New')),
        ('in_progress', _('In progress')),
        ('done', _('Completed')),
        ('cancelled', _('Cancelled')),
        ('waiting', _('Waiting')),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name=_("Order status")
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ["-date"]

    def __str__(self):
        return f"Order {self.car.license_plate} - {self.date}"

    @property
    def total(self):
        return sum(line.line_sum() for line in self.order_lines.all())

    def is_overdue(self):
        if self.due_back and timezone.now().date() > self.due_back:
            return True
        return False


class OrderLine(models.Model):
    """Order line (service + quantity)"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_lines",
                              verbose_name=_("Order"))
    service = models.ForeignKey(Service, on_delete=models.PROTECT, verbose_name=_("Service"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"))

    class Meta:
        verbose_name = _("Order line")
        verbose_name_plural = _("Order lines")

    def __str__(self):
        return f"{self.service.name} x {self.quantity}"

    def line_sum(self):
        if self.service and self.quantity:
            return self.service.price * self.quantity
        return 0


class OrderReview(models.Model):
    """Review for the order"""

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, verbose_name=_("Order"),
                              null=True, blank=True, related_name="reviews")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                 verbose_name=_("Reviewer"), null=True, blank=True)
    date_created = models.DateTimeField(verbose_name=_("Date created"), auto_now_add=True)
    content = models.TextField(verbose_name=_("Content"), max_length=2000)

    class Meta:
        verbose_name = _("Order review")
        verbose_name_plural = _("Order reviews")
        ordering = ["-date_created"]