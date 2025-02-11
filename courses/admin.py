"""
Cấu hình admin cho ứng dụng courses
"""
from django.contrib import admin
from .models import Category, Course, Lesson, Enrollment, Certificate, Progress

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Tùy chỉnh giao diện admin cho model Category
    """
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Tùy chỉnh giao diện admin cho model Course
    """
    list_display = ['title', 'category', 'instructor', 'price', 'is_published', 'created_at']
    list_filter = ['category', 'is_published', 'created_at']
    search_fields = ['title', 'instructor__email', 'description']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['instructor']

class LessonInline(admin.TabularInline):
    """
    Inline admin cho model Lesson
    """
    model = Lesson
    extra = 1
    fields = ['title', 'order', 'duration', 'video_url']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Tùy chỉnh giao diện admin cho model Lesson
    """
    list_display = ['title', 'course', 'order', 'duration']
    list_filter = ['course', 'created_at']
    search_fields = ['title', 'content', 'course__title']
    ordering = ['course', 'order']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """
    Tùy chỉnh giao diện admin cho model Enrollment
    """
    list_display = ['student', 'course', 'enrolled_at', 'completed']
    list_filter = ['completed', 'enrolled_at']
    search_fields = ['student__email', 'course__title', 'payment_id']
    raw_id_fields = ['student', 'course']

    def has_add_permission(self, request):
        return False

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    """
    Tùy chỉnh giao diện admin cho model Certificate
    """
    list_display = ['certificate_number', 'get_student', 'get_course', 'issued_date']
    search_fields = ['certificate_number', 'enrollment__student__email']
    readonly_fields = ['certificate_number', 'issued_date']

    def get_student(self, obj):
        return obj.enrollment.student.email
    get_student.short_description = 'Học viên'

    def get_course(self, obj):
        return obj.enrollment.course.title
    get_course.short_description = 'Khóa học'

    def has_add_permission(self, request):
        return False

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    """
    Tùy chỉnh giao diện admin cho model Progress
    """
    list_display = ['get_student', 'get_course', 'lesson', 'completed', 'completed_at']
    list_filter = ['completed', 'completed_at']
    search_fields = ['enrollment__student__email', 'lesson__title']
    raw_id_fields = ['enrollment', 'lesson']

    def get_student(self, obj):
        return obj.enrollment.student.email
    get_student.short_description = 'Học viên'

    def get_course(self, obj):
        return obj.enrollment.course.title
    get_course.short_description = 'Khóa học'