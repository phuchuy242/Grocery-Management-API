from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'total_price']
        read_only_fields = ['price', 'total_price']  # Không cho nhập price

    def get_total_price(self, obj):
        return obj.get_total_price()

    def validate_quantity(self, value):
        """Kiểm tra số lượng hợp lệ"""
        if value <= 0:
            raise serializers.ValidationError("Số lượng phải lớn hơn 0")
        if value > 1000:
            raise serializers.ValidationError("Số lượng tối đa là 1000")
        return value

    def validate(self, data):
        """Tự động lấy giá từ product và kiểm tra tồn kho"""
        product = data.get('product')
        quantity = data.get('quantity')

        if not product:
            raise serializers.ValidationError({"product": "Vui lòng chọn sản phẩm"})

        # ✅ TỰ ĐỘNG LẤY GIÁ TỪ PRODUCT
        data['price'] = product.price

        # Kiểm tra tồn kho (nếu có trường stock)
        if hasattr(product, 'stock'):
            if product.stock < quantity:
                raise serializers.ValidationError({
                    'quantity': f'Chỉ còn {product.stock} sản phẩm trong kho'
                })

        return data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'user_name', 'items', 'total_price', 'paid', 'status', 'created_at', 'updated_at']
        read_only_fields = ['total_price', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        # Tạo OrderItems
        for item_data in items_data:
            # price đã được tự động gán trong validate()
            order_item = OrderItem.objects.create(order=order, **item_data)

            # Trừ tồn kho
            product = item_data['product']
            if hasattr(product, 'stock'):
                product.stock -= item_data['quantity']
                product.save()

        # Tự động tính tổng tiền
        order.calculate_total()
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        # Cập nhật thông tin order
        instance.paid = validated_data.get('paid', instance.paid)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        # Cập nhật items nếu có
        if items_data:
            instance.items.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)
            instance.calculate_total()

        return instance


class OrderListSerializer(serializers.ModelSerializer):
    """Serializer đơn giản cho danh sách đơn hàng"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user_name', 'total_price', 'paid', 'status', 'items_count', 'created_at']

    def get_items_count(self, obj):
        return obj.items.count()
