"""
Views cho ứng dụng core
"""
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth import get_user_model
from django.db.models import Count
from courses.models import Category, Course
from users.models import User

class HomeView(TemplateView):
    """Trang chủ"""
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(
            course_count=Count('courses')
        ).order_by('-course_count')[:8]
        context['featured_courses'] = Course.objects.filter(
            is_published=True
        ).select_related('instructor').order_by('-created_at')[:6]
        return context

class AboutView(TemplateView):
    """Trang giới thiệu"""
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instructor_count'] = User.objects.filter(role='instructor').count()
        context['student_count'] = User.objects.filter(role='student').count()
        context['course_count'] = Course.objects.filter(is_published=True).count()
        return context

class ContactView(TemplateView):
    """Trang liên hệ"""
    template_name = 'core/contact.html'

class TermsView(TemplateView):
    """Trang điều khoản sử dụng"""
    template_name = 'core/terms.html'

class PrivacyView(TemplateView):
    """Trang chính sách bảo mật"""
    template_name = 'core/privacy.html'

class SearchView(ListView):
    """Trang tìm kiếm"""
    template_name = 'core/search.html'
    context_object_name = 'courses'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return Course.objects.filter(
            is_published=True,
            title__icontains=query
        ).select_related('instructor', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class CategoryListView(ListView):
    """Danh sách danh mục"""
    model = Category
    template_name = 'core/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.annotate(
            course_count=Count('courses')
        ).order_by('name')

class InstructorListView(ListView):
    """Danh sách giảng viên"""
    template_name = 'core/instructor_list.html'
    context_object_name = 'instructors'
    paginate_by = 12

    def get_queryset(self):
        return User.objects.filter(
            role='instructor'
        ).annotate(
            course_count=Count('courses_teaching'),
            student_count=Count('courses_teaching__enrollments__student', distinct=True)
        ).order_by('-course_count')

class InstructorDetailView(DetailView):
    """Chi tiết giảng viên"""
    model = User
    template_name = 'core/instructor_detail.html'
    context_object_name = 'instructor'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        return User.objects.filter(role='instructor')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instructor = self.get_object()
        context['courses'] = Course.objects.filter(
            instructor=instructor,
            is_published=True
        ).order_by('-created_at')
        return context

class BlogListView(ListView):
    """Danh sách bài viết blog"""
    template_name = 'core/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 10

class BlogDetailView(DetailView):
    """Chi tiết bài viết blog"""
    template_name = 'core/blog_detail.html'
    context_object_name = 'post'