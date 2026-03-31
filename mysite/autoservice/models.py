from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
from tinymce.models import HTMLField
from django.conf import settings


class CustomUser(AbstractUser):
    """Kastomizuotas vartotojas AutoService projektui"""

    photo = models.ImageField(
        upload_to="profile_pics/",
        null=True,
        blank=True,
        verbose_name="Profilio nuotrauka"
    )

    class Meta:
        verbose_name = "Vartotojas"
        verbose_name_plural = "Vartotojai"
        db_table = 'auth_user'

    def __str__(self):
        return self.username

class Service(models.Model):
    # Autoserviso paslaugos
    name = models.CharField(max_length=150, verbose_name="Paslaugos pavadinimas")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Kaina (€)")

    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Car(models.Model):
    # Uzsakovo automobilis
    make = models.CharField(max_length=100, verbose_name="Marke")
    model = models.CharField(max_length=100, verbose_name="Modelis")
    license_plate = models.CharField(max_length=50, verbose_name="Valstybinis nr.", unique=True)
    vin_code = models.CharField(max_length=17, verbose_name="Kebulo numeris", unique=True, blank=True, null=True)
    client_name = models.CharField(max_length=150, verbose_name="Klijentas")
    cover = models.ImageField('Nuotrauka', upload_to="covers/", null=True, blank=True)
    description = HTMLField(verbose_name="Aprasymas", max_length=3000, default="")

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"
        ordering = ["license_plate"]

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

class Order(models.Model):
    # Uzsakymas i autoservisa
    car = models.ForeignKey(Car, on_delete=models.PROTECT, verbose_name="Automobilis")
    date = models.DateTimeField(default=timezone.now, verbose_name="Uzsakymo data ir laikas")
    reader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="Vartotojas", null=True, blank=True)
    due_back = models.DateField(verbose_name="Grazinimo terminas", null=True, blank=True)

    def is_overdue(self):
        if self.due_back and timezone.now().date() > self.due_back:
            return True
        return False


    STATUS_CHOICES = ()

    # Naujas laukas: statusas
    STATUS_CHOICES = (
        ('new', 'Naujas'),
        ('in_progress', 'Vykdomas'),
        ('done', 'Baigtas'),
        ('cancelled', 'Atsauktas'),
        ('waiting', 'Laukiantis'),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Uzsakymo busena"
    )

    def display_order_line(self):
        return ", ".join(order.car for order in self.order.all())

    display_order_line.short_description = "Uzsakymo eilute"


    class Meta:
        verbose_name = "Uzsakymas"
        verbose_name_plural = "Uzsakymai"
        ordering = ["-date"]

    def __str__(self):
        return f"Uzsakymas {self.car.license_plate} - {self.date}"

    @property
    def total(self):
        return sum(line.line_sum() for line in self.order_lines.all())

class OrderLine(models.Model):
    # Uzsakymo eilute
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_lines", verbose_name="Uzsakymas")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, verbose_name="Paslauga")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Kiekis")

    class Meta:
        verbose_name = "Usakymo eilute"
        verbose_name_plural = "Uzsakymo eilutes"

    def __str__(self):
        return f"{self.service.name} x {self.quantity}"

    # Automatiskai apskaiciuota eilutes suma
    def line_sum(self):
        if self.service and self.quantity:
            return self.service.price * self.quantity
        return 0


class OrderReview(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.SET_NULL, verbose_name="Uzsakymas",
                              null=True, blank=True, related_name="reviews")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="Reviewer",
                                 null=True, blank=True)
    date_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    content = models.TextField(verbose_name="Content", max_length=2000)

    class Meta:
        verbose_name = "Uzsakymo atsiliepimas"
        verbose_name_plural = "Uzsakymo atsiliepimai"
        ordering = ["-date_created"]

