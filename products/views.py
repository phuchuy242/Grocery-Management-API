from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, ProductListSerializer, CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho quản lý categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho quản lý products (CRUD)
    - List: GET /api/products/
    - Create: POST /api/products/
    - Retrieve: GET /api/products/{id}/
    - Update: PUT /api/products/{id}/
    - Partial Update: PATCH /api/products/{id}/
    - Delete: DELETE /api/products/{id}/
    """
    queryset = Product.objects.select_related('category').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_available']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'quantity', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Sử dụng serializer khác nhau cho list và detail"""
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    def create(self, request, *args, **kwargs):
        """Thêm sản phẩm mới"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Cập nhật sản phẩm"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Xóa sản phẩm"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Sản phẩm đã được xóa thành công"},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Lấy danh sách sản phẩm sắp hết hàng"""
        threshold = int(request.query_params.get('threshold', 10))
        products = self.queryset.filter(quantity__lte=threshold, is_available=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        """Cập nhật số lượng tồn kho"""
        product = self.get_object()
        quantity = request.data.get('quantity')

        if quantity is None:
            return Response(
                {"error": "Vui lòng cung cấp số lượng"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity = int(quantity)
            if quantity < 0:
                return Response(
                    {"error": "Số lượng không thể âm"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            product.quantity = quantity
            product.stock = quantity
            product.save()

            serializer = self.get_serializer(product)
            return Response(serializer.data)
        except ValueError:
            return Response(
                {"error": "Số lượng không hợp lệ"},
                status=status.HTTP_400_BAD_REQUEST
            )
