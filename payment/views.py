from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Payment, PaymentLog
from .serializers import PaymentSerializer
from orders.models import Order
import urllib.parse


class PaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho quản lý thanh toán
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """User chỉ xem payment của đơn hàng mình, Admin xem tất cả"""
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(order__user=user)

    @action(detail=False, methods=['post'])
    def create_qr_payment(self, request):
        """
        Tạo thanh toán QR cho đơn hàng
        POST /api/payment/create_qr_payment/
        Body: {"order_id": 1}
        """
        order_id = request.data.get('order_id')

        if not order_id:
            return Response(
                {"error": "Vui lòng cung cấp order_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {"error": "Đơn hàng không tồn tại"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Kiểm tra đã có payment chưa
        if hasattr(order, 'payment'):
            payment = order.payment
        else:
            # Tạo payment mới
            payment = Payment.objects.create(
                order=order,
                amount=order.total_price,
                method='qr_code',
                status='pending',
                bank_name='MB Bank',  # Thay bằng thông tin ngân hàng thật
                account_number='0796791500',
                account_name='TRAN NGOC PHUC HUY'
            )

        # Tạo QR Code URL sử dụng VietQR API
        qr_url = self.generate_vietqr_url(payment)
        payment.qr_code_url = qr_url
        payment.save()

        # Log
        PaymentLog.objects.create(
            payment=payment,
            status='pending',
            message='Tạo mã QR thanh toán'
        )

        serializer = self.get_serializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def generate_vietqr_url(self, payment):
        """
        Tạo URL mã QR thanh toán sử dụng VietQR API
        https://api.vietqr.io/
        """
        # Thông tin ngân hàng
        bank_id = "970422"  # MB Bank code
        account_no = payment.account_number or "0123456789"
        account_name = payment.account_name or "GROCERY STORE"
        amount = int(payment.amount)

        # Nội dung chuyển khoản
        add_info = f"Order {payment.order.id}"

        # Tạo URL QR Code
        # Format: https://img.vietqr.io/image/{BANK_ID}-{ACCOUNT_NO}-{TEMPLATE}.png?amount={AMOUNT}&addInfo={INFO}&accountName={NAME}
        base_url = f"https://img.vietqr.io/image/{bank_id}-{account_no}-compact2.png"
        params = {
            'amount': amount,
            'addInfo': add_info,
            'accountName': account_name
        }

        qr_url = f"{base_url}?{urllib.parse.urlencode(params)}"
        return qr_url

    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        """
        Xác nhận thanh toán đã hoàn tất
        POST /api/payment/{id}/confirm_payment/
        """
        payment = self.get_object()

        if payment.status == 'completed':
            return Response(
                {"error": "Thanh toán đã được xác nhận trước đó"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Cập nhật trạng thái
        payment.status = 'completed'
        payment.paid_at = timezone.now()
        payment.save()

        # Cập nhật đơn hàng
        order = payment.order
        order.paid = True
        order.status = 'processing'
        order.save()

        # Log
        PaymentLog.objects.create(
            payment=payment,
            status='completed',
            message='Thanh toán đã được xác nhận'
        )

        serializer = self.get_serializer(payment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel_payment(self, request, pk=None):
        """
        Hủy thanh toán
        POST /api/payment/{id}/cancel_payment/
        """
        payment = self.get_object()

        if payment.status == 'completed':
            return Response(
                {"error": "Không thể hủy thanh toán đã hoàn tất"},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment.status = 'cancelled'
        payment.save()

        # Log
        PaymentLog.objects.create(
            payment=payment,
            status='cancelled',
            message='Thanh toán đã bị hủy'
        )

        serializer = self.get_serializer(payment)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_qr_code(self, request, pk=None):
        """
        Lấy URL mã QR
        GET /api/payment/{id}/get_qr_code/
        """
        payment = self.get_object()

        if not payment.qr_code_url:
            qr_url = self.generate_vietqr_url(payment)
            payment.qr_code_url = qr_url
            payment.save()

        return Response({
            'qr_code_url': payment.qr_code_url,
            'amount': payment.amount,
            'bank_name': payment.bank_name,
            'account_number': payment.account_number,
            'account_name': payment.account_name,
            'order_id': payment.order.id
        })

