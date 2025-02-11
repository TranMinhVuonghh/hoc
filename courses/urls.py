"""
URL patterns cho ứng dụng courses
"""
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Danh sách khóa học
    path('', views.CourseListView.as_view(), name='course-list'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course-detail'),
    
    # Ghi danh và thanh toán
    path('<slug:slug>/enroll/', views.EnrollCourseView.as_view(), name='course-enroll'),
    path('payment/process/', views.PaymentProcessView.as_view(), name='payment-process'),
    path('payment/success/', views.PaymentSuccessView.as_view(), name='payment-success'),
    path('payment/cancel/', views.PaymentCancelView.as_view(), name='payment-cancel'),
    
    # Học tập
    path('<slug:course_slug>/learn/', views.CourseLearnView.as_view(), name='course-learn'),
    path('<slug:course_slug>/learn/<int:lesson_order>/', 
         views.LessonDetailView.as_view(), 
         name='lesson-detail'),
    path('lesson/<int:pk>/complete/', 
         views.LessonCompleteView.as_view(), 
         name='lesson-complete'),
    
    # Chứng chỉ
    path('certificate/<str:number>/', 
         views.CertificateDetailView.as_view(), 
         name='certificate-detail'),
    path('certificate/verify/', 
         views.CertificateVerifyView.as_view(), 
         name='certificate-verify'),
    
    # API endpoints cho AJAX
    path('api/progress/update/', 
         views.UpdateProgressView.as_view(), 
         name='update-progress'),
]