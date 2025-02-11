"""
Mô hình dữ liệu cho ứng dụng courses
"""
from django.db import models
from django.conf import settings
from django.urls import reverse

class Category(models.Model):
    """
    Model danh mục khóa học
    """
    name = models.CharField(max_length=100, verbose_name='Tên danh mục')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Mô tả')
    image = models.ImageField(upload_to='categories/', blank=True, verbose_name='Ảnh')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Cập nhật lần cuối')

    class Meta:
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'slug': self.slug})

class Course(models.Model):
    """
    Model khóa học
    """
    title = models.CharField(max_length=200, verbose_name='Tên khóa học')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name='Danh mục'
    )
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses_teaching',
        verbose_name='Giảng viên'
    )
    description = models.TextField(verbose_name='Mô tả')
    image = models.ImageField(upload_to='courses/', verbose_name='Ảnh')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Giá'
    )
    is_published = models.BooleanField(default=False, verbose_name='Đã xuất bản')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Cập nhật lần cuối')

    class Meta:
        verbose_name = 'Khóa học'
        verbose_name_plural = 'Khóa học'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'slug': self.slug})

class Lesson(models.Model):
    """
    Model bài học trong khóa học
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Khóa học'
    )
    title = models.CharField(max_length=200, verbose_name='Tên bài học')
    content = models.TextField(verbose_name='Nội dung')
    video_url = models.URLField(blank=True, verbose_name='URL video')
    order = models.PositiveIntegerField(verbose_name='Thứ tự')
    duration = models.PositiveIntegerField(
        help_text='Thời lượng tính bằng phút',
        verbose_name='Thời lượng'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Cập nhật lần cuối')

    class Meta:
        verbose_name = 'Bài học'
        verbose_name_plural = 'Bài học'
        ordering = ['order']
        unique_together = ['course', 'order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Enrollment(models.Model):
    """
    Model ghi danh khóa học
    """
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Học viên'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Khóa học'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày ghi danh')
    payment_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Mã thanh toán'
    )
    completed = models.BooleanField(default=False, verbose_name='Đã hoàn thành')

    class Meta:
        verbose_name = 'Ghi danh'
        verbose_name_plural = 'Ghi danh'
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student.email} - {self.course.title}"

class Certificate(models.Model):
    """
    Model chứng chỉ hoàn thành khóa học
    """
    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='certificate',
        verbose_name='Ghi danh'
    )
    certificate_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Số chứng chỉ'
    )
    issued_date = models.DateTimeField(auto_now_add=True, verbose_name='Ngày cấp')
    
    class Meta:
        verbose_name = 'Chứng chỉ'
        verbose_name_plural = 'Chứng chỉ'

    def __str__(self):
        return f"Chứng chỉ {self.certificate_number}"

class Progress(models.Model):
    """
    Model theo dõi tiến độ học tập
    """
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='progress',
        verbose_name='Ghi danh'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='progress',
        verbose_name='Bài học'
    )
    completed = models.BooleanField(default=False, verbose_name='Đã hoàn thành')
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Ngày hoàn thành'
    )

    class Meta:
        verbose_name = 'Tiến độ'
        verbose_name_plural = 'Tiến độ'
        unique_together = ['enrollment', 'lesson']

    def __str__(self):
        return f"{self.enrollment.student.email} - {self.lesson.title}"