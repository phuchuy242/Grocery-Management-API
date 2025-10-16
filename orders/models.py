from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('processing', 'Đang xử lý'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    def calculate_total(self):
        """Tính tổng tiền từ các OrderItem"""
        total = sum(item.get_total_price() for item in self.items.all())
        self.total_price = total
        self.save()
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá tại thời điểm đặt hàng

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    def get_total_price(self):
        """Tính tổng tiền của item này"""
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        """Tự động lưu giá sản phẩm tại thời điểm đặt hàng"""
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)
