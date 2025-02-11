# Nền tảng Học Trực Tuyến

Nền tảng học trực tuyến được xây dựng bằng Django với các tính năng tương tự như Unica.vn.

## Yêu cầu hệ thống

- Python 3.8+
- PostgreSQL 12+
- Node.js 14+ (cho TailwindCSS)

## Công nghệ sử dụng

- Backend: Django 5.0
- Frontend: TailwindCSS
- Database: PostgreSQL + SQLAlchemy
- Payment: Stripe

## Tính năng chính

- Đăng ký/Đăng nhập tài khoản
- Danh sách và tìm kiếm khóa học
- Chi tiết khóa học
- Thanh toán trực tuyến
- Hệ thống học trực tuyến
- Theo dõi tiến độ học tập
- Chứng chỉ hoàn thành
- Bảng điều khiển giảng viên
- Quản lý khóa học và bài giảng

## Cài đặt môi trường phát triển

1. Tạo và kích hoạt môi trường ảo:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

2. Cài đặt các gói phụ thuộc:
```bash
pip install -r requirements.txt
```

3. Tạo file .env và cấu hình các biến môi trường:
```
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
```

4. Tạo database và chạy migrations:
```bash
python manage.py migrate
```

5. Tạo tài khoản admin:
```bash
python manage.py createsuperuser
```

6. Chạy server phát triển:
```bash
python manage.py runserver
```

## Cấu trúc thư mục

```
hoc/
├── core/                   # Ứng dụng core (trang chủ, trang tĩnh)
├── courses/               # Ứng dụng quản lý khóa học
├── users/                 # Ứng dụng quản lý người dùng
├── templates/             # Templates HTML
│   ├── core/
│   ├── courses/
│   └── users/
├── static/               # Tài nguyên tĩnh
│   ├── css/
│   ├── js/
│   └── images/
├── media/               # File người dùng tải lên
├── config/              # Cấu hình Django project
└── manage.py
```

## Hướng dẫn phát triển

1. Tuân thủ chuẩn code PEP 8
2. Comment bằng tiếng Việt cho rõ ràng
3. Mỗi file không quá 500 dòng
4. Viết test cho các tính năng quan trọng
5. Kiểm tra bảo mật trước khi deploy

## Triển khai

1. Cài đặt các gói cần thiết:
```bash
pip install gunicorn psycopg2-binary
```

2. Cấu hình webserver (Nginx) và reverse proxy
3. Thiết lập SSL certificate
4. Cấu hình domain và DNS
5. Thiết lập backup database

## Bảo trì

- Theo dõi logs
- Backup database định kỳ
- Cập nhật các gói phụ thuộc
- Kiểm tra bảo mật thường xuyên

## Hỗ trợ

Liên hệ qua email: contact@hoc.tranminhvuong.com