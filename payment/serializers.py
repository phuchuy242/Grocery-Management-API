from rest_framework import serializers
from .models import Payment, PaymentLog


class PaymentLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentLog
        fields = ['id', 'status', 'message', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='order.id', read_only=True)
    logs = PaymentLogSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'order_id', 'amount', 'method', 'status',
            'transaction_id', 'qr_code_url', 'bank_name', 'account_number',
            'account_name', 'created_at', 'updated_at', 'paid_at', 'logs'
        ]
        read_only_fields = ['qr_code_url', 'created_at', 'updated_at', 'paid_at']

