from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_products_count(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'category_name', 'description',
            'price', 'quantity', 'stock', 'image', 'is_available',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'stock']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Giá sản phẩm phải lớn hơn 0")
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Số lượng không thể âm")
        return value


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer đơn giản cho danh sách sản phẩm"""
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category_name', 'price', 'quantity', 'is_available']

