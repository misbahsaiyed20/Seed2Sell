from django.db import models
from django.conf import settings


class FarmerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='farmer_profile'
    )
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):

    # ADD THESE 👇
    UNIT_CHOICES = (
        ('kg', 'Kilogram (kg)'),
        ('litre', 'Litre (L)'),
        ('piece', 'Piece'),
        ('packet', 'Packet'),
        ('dozen', 'Dozen'),
        ('gram', 'Gram (g)'),
    )

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=200)
    cost_price = models.DecimalField(max_digits=8, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_bestseller = models.BooleanField(default=False)

    # ADD THIS 👇
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='kg')

    def __str__(self):
        return self.name


class Order(models.Model):

    PAYMENT_METHOD_CHOICES = (
        ('COD', 'Cash on Delivery'),
        ('UPI', 'UPI'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        default='COD'
    )
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='PENDING'
    )
    upi_reference = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} (Order #{self.order.id})"