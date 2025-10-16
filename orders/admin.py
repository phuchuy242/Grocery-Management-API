from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['price', 'get_total_price']  # ✅ Thêm price vào readonly
    fields = ['product', 'quantity', 'price', 'get_total_price']  # Thứ tự hiển thị

    def get_total_price(self, obj):
        return obj.get_total_price() if obj.id else 0
    get_total_price.short_description = 'Tổng tiền'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'paid', 'status', 'created_at']
    list_filter = ['paid', 'status', 'created_at']
    search_fields = ['user__username', 'id']
    readonly_fields = ['total_price', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    actions = ['mark_as_paid', 'mark_as_completed']

    def mark_as_paid(self, request, queryset):
        queryset.update(paid=True, status='processing')
    mark_as_paid.short_description = "Đánh dấu đã thanh toán"

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Đánh dấu hoàn thành"

    def save_formset(self, request, form, formset, change):
        """Tự động tính tổng tiền khi lưu OrderItems"""
        instances = formset.save(commit=False)
        for instance in instances:
            # ✅ Tự động lấy giá từ product
            if instance.product and not instance.price:
                instance.price = instance.product.price
            instance.save()
        formset.save_m2m()

        # Tính lại tổng tiền cho order
        if form.instance:
            form.instance.calculate_total()


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'get_total_price']
    list_filter = ['order__status']
    search_fields = ['product__name', 'order__id']
    readonly_fields = ['price']  # ✅ Không cho sửa price thủ công

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Tổng tiền'

    def save_model(self, request, obj, form, change):
        """Tự động lấy giá khi lưu"""
        if obj.product and not obj.price:
            obj.price = obj.product.price
        super().save_model(request, obj, form, change)
