from django.contrib.auth import get_user_model
from django.db import models
from fitnessEcommerceApp.products.models import Product

UserModel = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name='cart'
    )

    products = models.ManyToManyField(Product, through='CartItem', related_name='carts')

    def __str__(self):
        return f'User id: {self.user.pk}'


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} - {self.product.name}"


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )

    is_sent = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='orders'
    )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"

