"""
Tests cho ứng dụng courses
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Category, Course, Lesson, Enrollment, Certificate

User = get_user_model()

class CourseModelTests(TestCase):
    """Test cases cho model Course"""
    
    def setUp(self):
        # Tạo user giảng viên
        self.instructor = User.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='testpass123',
            role='instructor'
        )
        
        # Tạo category
        self.category = Category.objects.create(
            name='Programming',
            slug='programming',
            description='Programming courses'
        )
        
        # Tạo khóa học
        self.course = Course.objects.create(
            title='Python for Beginners',
            slug='python-for-beginners',
            instructor=self.instructor,
            category=self.category,
            description='Learn Python basics',
            price=500000,
            is_published=True
        )

    def test_course_creation(self):
        """Test tạo khóa học"""
        self.assertEqual(self.course.title, 'Python for Beginners')
        self.assertEqual(self.course.instructor, self.instructor)
        self.assertEqual(self.course.category, self.category)
        self.assertEqual(self.course.price, 500000)
        self.assertTrue(self.course.is_published)

    def test_course_str(self):
        """Test string representation của khóa học"""
        self.assertEqual(str(self.course), 'Python for Beginners')

    def test_get_absolute_url(self):
        """Test URL của khóa học"""
        self.assertEqual(
            self.course.get_absolute_url(),
            reverse('course-detail', kwargs={'slug': 'python-for-beginners'})
        )

class EnrollmentModelTests(TestCase):
    """Test cases cho model Enrollment"""
    
    def setUp(self):
        # Tạo user học viên
        self.student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='testpass123',
            role='student'
        )
        
        # Tạo user giảng viên
        self.instructor = User.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='testpass123',
            role='instructor'
        )
        
        # Tạo category
        self.category = Category.objects.create(
            name='Programming',
            slug='programming',
            description='Programming courses'
        )
        
        # Tạo khóa học
        self.course = Course.objects.create(
            title='Python for Beginners',
            slug='python-for-beginners',
            instructor=self.instructor,
            category=self.category,
            description='Learn Python basics',
            price=500000,
            is_published=True
        )
        
        # Tạo ghi danh
        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course
        )

    def test_enrollment_creation(self):
        """Test tạo ghi danh"""
        self.assertEqual(self.enrollment.student, self.student)
        self.assertEqual(self.enrollment.course, self.course)
        self.assertFalse(self.enrollment.completed)

    def test_unique_enrollment(self):
        """Test ràng buộc unique cho ghi danh"""
        with self.assertRaises(Exception):
            Enrollment.objects.create(
                student=self.student,
                course=self.course
            )

class CertificateModelTests(TestCase):
    """Test cases cho model Certificate"""
    
    def setUp(self):
        # Tạo user học viên
        self.student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='testpass123'
        )
        
        # Tạo user giảng viên
        self.instructor = User.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='testpass123',
            role='instructor'
        )
        
        # Tạo category
        self.category = Category.objects.create(
            name='Programming',
            slug='programming',
            description='Programming courses'
        )
        
        # Tạo khóa học
        self.course = Course.objects.create(
            title='Python for Beginners',
            slug='python-for-beginners',
            instructor=self.instructor,
            category=self.category,
            description='Learn Python basics',
            price=500000,
            is_published=True
        )
        
        # Tạo ghi danh
        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            completed=True
        )
        
        # Tạo chứng chỉ
        self.certificate = Certificate.objects.create(
            enrollment=self.enrollment,
            certificate_number='CERT-001'
        )

    def test_certificate_creation(self):
        """Test tạo chứng chỉ"""
        self.assertEqual(self.certificate.enrollment, self.enrollment)
        self.assertEqual(self.certificate.certificate_number, 'CERT-001')
        self.assertIsNotNone(self.certificate.issued_date)

    def test_certificate_str(self):
        """Test string representation của chứng chỉ"""
        self.assertEqual(str(self.certificate), 'Chứng chỉ CERT-001')

class CourseViewTests(TestCase):
    """Test cases cho views của Course"""
    
    def setUp(self):
        # Tạo user giảng viên
        self.instructor = User.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='testpass123',
            role='instructor'
        )
        
        # Tạo category
        self.category = Category.objects.create(
            name='Programming',
            slug='programming',
            description='Programming courses'
        )
        
        # Tạo khóa học
        self.course = Course.objects.create(
            title='Python for Beginners',
            slug='python-for-beginners',
            instructor=self.instructor,
            category=self.category,
            description='Learn Python basics',
            price=500000,
            is_published=True
        )

    def test_course_list_view(self):
        """Test view danh sách khóa học"""
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python for Beginners')
        self.assertTemplateUsed(response, 'courses/course_list.html')

    def test_course_detail_view(self):
        """Test view chi tiết khóa học"""
        response = self.client.get(
            reverse('course-detail', kwargs={'slug': 'python-for-beginners'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python for Beginners')
        self.assertContains(response, 'Learn Python basics')
        self.assertTemplateUsed(response, 'courses/course_detail.html')