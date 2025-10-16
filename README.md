# 🛒 Grocery Store Management API

API quản lý cửa hàng tạp hóa được xây dựng bằng Django REST Framework với đầy đủ các chức năng CRUD, xác thực JWT, và tích hợp thanh toán QR Code.

## 📋 Mục lục

- [Tính năng](#tính-năng)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Cài đặt](#cài-đặt)
- [Cấu hình Database](#cấu-hình-database)
- [Chạy Project](#chạy-project)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)

---

## ✨ Tính năng

### 1️⃣ **Quản lý sản phẩm (Product Management - CRUD)**
- ✅ Thêm sản phẩm mới
- ✅ Xem danh sách sản phẩm
- ✅ Cập nhật thông tin sản phẩm
- ✅ Xóa sản phẩm
- ✅ Tìm kiếm, lọc sản phẩm theo category
- ✅ Cảnh báo sản phẩm sắp hết hàng

### 2️⃣ **Quản lý đơn hàng (Order Management)**
- ✅ Tạo đơn hàng từ danh sách sản phẩm
- ✅ Tự động tính tổng tiền
- ✅ Cập nhật trạng thái thanh toán
- ✅ Xem danh sách đơn hàng của user
- ✅ Xem chi tiết đơn hàng
- ✅ Hủy đơn hàng

### 3️⃣ **Quản lý người dùng (User & Authentication)**
- ✅ Đăng ký tài khoản
- ✅ Đăng nhập với JWT Token
- ✅ Xem và cập nhật profile
- ✅ Đổi mật khẩu
- ✅ Phân quyền User/Admin

### 4️⃣ **Thanh toán QR Code (Payment Integration)**
- ✅ Sinh mã QR thanh toán tự động (VietQR)
- ✅ Hiển thị thông tin: số tiền, nội dung, tài khoản
- ✅ Xác nhận thanh toán
- ✅ Lịch sử giao dịch

---

## 🛠 Công nghệ sử dụng

- **Backend Framework**: Django 5.2.7
- **API Framework**: Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: MySQL
- **Documentation**: Swagger (drf-yasg)
- **QR Payment**: VietQR API
- **Image Processing**: Pillow

---

## 📦 Cài đặt

### 1. Clone repository

```bash
git clone <repository-url>
cd grocery_store
```

### 2. Tạo môi trường ảo (Virtual Environment)

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄 Cấu hình Database

### 1. Tạo database trong MySQL

Mở MySQL Workbench hoặc MySQL CLI và chạy:

```sql
CREATE DATABASE grocery_store CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Cấu hình thông tin database

Mở file `grocery_store/settings.py` và cập nhật:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'grocery_store',
        'USER': 'your_mysql_username',      # Thay bằng username của bạn
        'PASSWORD': 'your_mysql_password',   # Thay bằng password của bạn
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

### 3. Chạy migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Tạo superuser

```bash
python manage.py createsuperuser
```

---

## 🚀 Chạy Project

### 1. Khởi động server

```bash
python manage.py runserver
```

### 2. Truy cập ứng dụng

- **Django Admin**: http://127.0.0.1:8000/admin/
- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/

---

## 📚 API Documentation

API documentation được tự động sinh bằng Swagger. Truy cập:

**Swagger UI**: http://127.0.0.1:8000/swagger/

Tại đây bạn có thể:
- Xem tất cả API endpoints
- Test API trực tiếp trên trình duyệt
- Xem request/response schema

---

## 🔗 API Endpoints

### **Authentication**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Đăng ký tài khoản | ❌ |
| POST | `/api/auth/login/` | Đăng nhập (lấy JWT token) | ❌ |
| POST | `/api/auth/token/refresh/` | Refresh access token | ❌ |
| GET | `/api/auth/profile/` | Xem thông tin user | ✅ |
| PUT | `/api/auth/profile/` | Cập nhật thông tin user | ✅ |
| PUT | `/api/auth/change-password/` | Đổi mật khẩu | ✅ |

### **Products (Sản phẩm)**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/products/` | Danh sách sản phẩm | ❌ |
| POST | `/api/products/` | Thêm sản phẩm mới | ✅ |
| GET | `/api/products/{id}/` | Chi tiết sản phẩm | ❌ |
| PUT | `/api/products/{id}/` | Cập nhật sản phẩm | ✅ |
| DELETE | `/api/products/{id}/` | Xóa sản phẩm | ✅ |
| GET | `/api/products/low_stock/` | Sản phẩm sắp hết hàng | ✅ |
| POST | `/api/products/{id}/update_stock/` | Cập nhật số lượng tồn kho | ✅ |

### **Categories (Danh mục)**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/categories/` | Danh sách danh mục | ❌ |
| POST | `/api/categories/` | Thêm danh mục | ✅ |
| GET | `/api/categories/{id}/` | Chi tiết danh mục | ❌ |
| PUT | `/api/categories/{id}/` | Cập nhật danh mục | ✅ |
| DELETE | `/api/categories/{id}/` | Xóa danh mục | ✅ |

### **Orders (Đơn hàng)**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/orders/` | Danh sách đơn hàng | ✅ |
| POST | `/api/orders/` | Tạo đơn hàng mới | ✅ |
| GET | `/api/orders/{id}/` | Chi tiết đơn hàng | ✅ |
| PUT | `/api/orders/{id}/` | Cập nhật đơn hàng | ✅ |
| DELETE | `/api/orders/{id}/` | Xóa đơn hàng | ✅ |
| POST | `/api/orders/{id}/mark_paid/` | Đánh dấu đã thanh toán | ✅ |
| POST | `/api/orders/{id}/cancel/` | Hủy đơn hàng | ✅ |
| GET | `/api/orders/my_orders/` | Đơn hàng của tôi | ✅ |

### **Payment (Thanh toán)**

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/payment/` | Danh sách thanh toán | ✅ |
| POST | `/api/payment/create_qr_payment/` | Tạo mã QR thanh toán | ✅ |
| GET | `/api/payment/{id}/get_qr_code/` | Lấy mã QR | ✅ |
| POST | `/api/payment/{id}/confirm_payment/` | Xác nhận đã thanh toán | ✅ |
| POST | `/api/payment/{id}/cancel_payment/` | Hủy thanh toán | ✅ |

---

## 🧪 Testing với Postman

### 1. Đăng ký tài khoản

```
POST http://127.0.0.1:8000/api/auth/register/
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "strongpassword123",
  "password2": "strongpassword123"
}
```

### 2. Đăng nhập và lấy token

```
POST http://127.0.0.1:8000/api/auth/login/
Content-Type: application/json

{
  "username": "testuser",
  "password": "strongpassword123"
}
```

Response:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJh...",
  "access": "eyJ0eXAiOiJKV1QiLCJh..."
}
```

### 3. Sử dụng token để gọi API

```
GET http://127.0.0.1:8000/api/products/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJh...
```

### 4. Tạo đơn hàng

```
POST http://127.0.0.1:8000/api/orders/
Authorization: Bearer <your-token>
Content-Type: application/json

{
  "items": [
    {
      "product": 1,
      "quantity": 2
    },
    {
      "product": 2,
      "quantity": 1
    }
  ]
}
```

### 5. Tạo mã QR thanh toán

```
POST http://127.0.0.1:8000/api/payment/create_qr_payment/
Authorization: Bearer <your-token>
Content-Type: application/json

{
  "order_id": 1
}
```

Response sẽ chứa `qr_code_url` - link ảnh QR để thanh toán.

---

## 📁 Cấu trúc Project

```
grocery_store/
├── grocery_store/          # Cấu hình project
│   ├── settings.py         # Cấu hình chính
│   ├── urls.py             # URL routing chính
│   └── wsgi.py             # WSGI config
├── products/               # App quản lý sản phẩm
│   ├── models.py           # Product, Category models
│   ├── serializers.py      # Serializers
│   ├── views.py            # API views
│   ├── urls.py             # URL routing
│   └── admin.py            # Django admin
├── orders/                 # App quản lý đơn hàng
│   ├── models.py           # Order, OrderItem models
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── payment/                # App thanh toán
│   ├── models.py           # Payment, PaymentLog models
│   ├── serializers.py
│   ├── views.py            # VietQR integration
│   ├── urls.py
│   └── admin.py
├── users/                  # App xác thực
│   ├── serializers.py      # User serializers
│   ├── views.py            # Auth views
│   └── urls.py
├── manage.py               # Django CLI
├── requirements.txt        # Dependencies
└── README.md               # Documentation
```

---

## 🔐 Phân quyền

- **Admin**: Toàn quyền CRUD trên tất cả models
- **User**: Chỉ xem và tạo đơn hàng của mình

---

## 🌐 Deploy

### Deploy lên Render.com hoặc Railway.app

1. Tạo file `Procfile`:
```
web: gunicorn grocery_store.wsgi
```

2. Cài đặt gunicorn:
```bash
pip install gunicorn
pip freeze > requirements.txt
```

3. Cập nhật `settings.py`:
```python
ALLOWED_HOSTS = ['*']  # Hoặc domain cụ thể
```

4. Push lên GitHub và kết nối với Render/Railway

---

## 📝 Notes

- Database username và password trong `settings.py` cần được cập nhật theo môi trường của bạn
- Thông tin ngân hàng trong Payment models chỉ là demo, cần thay bằng thông tin thật khi deploy
- JWT token có thời hạn 1 ngày, có thể thay đổi trong `settings.py`

---

## 👤 Author

Phúc Huy - Grocery Management API

---

## 📄 License

MIT License - Tự do sử dụng và chỉnh sửa

