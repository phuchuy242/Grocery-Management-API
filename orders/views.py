from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderListSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho quản lý đơn hàng
    - List: GET /api/orders/
    - Create: POST /api/orders/
    - Retrieve: GET /api/orders/{id}/
    - Update: PUT /api/orders/{id}/
    - Delete: DELETE /api/orders/{id}/
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """User chỉ xem đơn hàng của mình, Admin xem tất cả"""
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        """Tạo đơn hàng mới"""
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """Đánh dấu đơn hàng đã thanh toán"""
        order = self.get_object()
        order.paid = True
        order.status = 'processing'
        order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Hủy đơn hàng"""
        order = self.get_object()

        if order.status == 'completed':
            return Response(
                {"error": "Không thể hủy đơn hàng đã hoàn thành"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = 'cancelled'
        order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        """Lấy danh sách đơn hàng của user hiện tại"""
        orders = Order.objects.filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
