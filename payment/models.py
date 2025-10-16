from django.db import models
from orders.models import Order


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Tiền mặt'),
        ('bank_transfer', 'Chuyển khoản'),
        ('qr_code', 'QR Code'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Chờ thanh toán'),
        ('completed', 'Đã thanh toán'),
        ('failed', 'Thất bại'),
        ('cancelled', 'Đã hủy'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='qr_code')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    qr_code_url = models.URLField(blank=True, null=True)

    # Thông tin ngân hàng
    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    account_name = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment #{self.id} for Order #{self.order.id}"


class PaymentLog(models.Model):
    """Lịch sử các giao dịch thanh toán"""
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='logs')
    status = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Log for Payment #{self.payment.id} - {self.status}"

