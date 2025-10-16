from django.contrib import admin
from .models import Payment, PaymentLog


class PaymentLogInline(admin.TabularInline):
    model = PaymentLog
    extra = 0
    readonly_fields = ['status', 'message', 'created_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'amount', 'method', 'status', 'created_at', 'paid_at']
    list_filter = ['method', 'status', 'created_at']
    search_fields = ['order__id', 'transaction_id']
    readonly_fields = ['amount', 'qr_code_url', 'created_at', 'updated_at', 'paid_at']  # ✅ Thêm amount vào readonly
    inlines = [PaymentLogInline]

    actions = ['mark_as_completed']

    def mark_as_completed(self, request, queryset):
        for payment in queryset:
            payment.status = 'completed'
            payment.save()
            payment.order.paid = True
            payment.order.save()
    mark_as_completed.short_description = "Đánh dấu đã thanh toán"

    def save_model(self, request, obj, form, change):
        """Tự động lấy số tiền từ Order"""
        if obj.order and not obj.amount:
            obj.amount = obj.order.total_price
        super().save_model(request, obj, form, change)


@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ['payment', 'status', 'message', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['payment__id', 'message']
