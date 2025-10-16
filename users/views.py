from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer


@api_view(['GET'])
def test_api(request):
    return Response({"message": "Django REST Framework is working!"})


class RegisterView(generics.CreateAPIView):
    """
    API đăng ký tài khoản mới
    POST /api/register/
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Tạo user mới
        user = serializer.save()

        # Tạo JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API xem và cập nhật thông tin user
    GET/PUT /api/profile/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """
    API đổi mật khẩu
    PUT /api/change-password/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        # Kiểm tra mật khẩu cũ
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {"old_password": "Mật khẩu cũ không đúng"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Đặt mật khẩu mới
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response(
            {"message": "Đổi mật khẩu thành công"},
            status=status.HTTP_200_OK
        )
