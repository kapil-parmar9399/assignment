from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=120)
    length_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    width_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    height_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    weight_kg = models.DecimalField(max_digits=8, decimal_places=3, validators=[MinValueValidator(0.001)])

    class Meta:
        ordering = ["name", "sku"]

    def __str__(self):
        return f"{self.name} ({self.sku})"


class Box(models.Model):
    name = models.CharField(max_length=100, unique=True)
    length_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    width_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    height_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    max_weight_kg = models.DecimalField(max_digits=8, decimal_places=3, validators=[MinValueValidator(0.001)])
    cost = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["cost", "name"]

    def __str__(self):
        return self.name


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through="OrderItem", related_name="orders")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk}" if self.pk else "New order"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=["order", "product"], name="unique_product_per_order")]

    def __str__(self):
        return f"{self.product} x {self.quantity}"
