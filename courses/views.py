"""
Views cho ứng dụng courses
"""
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from .models import Category, Course, Lesson, Enrollment, Certificate, Progress
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class CourseListView(ListView):
    """Danh sách khóa học"""
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 12

    def get_queryset(self):
        queryset = Course.objects.filter(is_published=True)
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset.select_related('instructor', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class CategoryDetailView(DetailView):
    """Chi tiết danh mục"""
    model = Category
    template_name = 'courses/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = self.object.courses.filter(
            is_published=True
        ).select_related('instructor')
        return context

class CourseDetailView(DetailView):
    """Chi tiết khóa học"""
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_queryset(self):
        return super().get_queryset().select_related('instructor', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_enrolled'] = Enrollment.objects.filter(
                student=self.request.user,
                course=self.object
            ).exists()
        return context

class EnrollCourseView(LoginRequiredMixin, View):
    """Đăng ký khóa học"""
    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, slug=kwargs['slug'])
        
        # Kiểm tra xem đã ghi danh chưa
        if Enrollment.objects.filter(student=request.user, course=course).exists():
            return redirect('courses:course-learn', course_slug=course.slug)

        try:
            # Tạo Stripe Checkout Session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'vnd',
                        'unit_amount': int(course.price * 100),  # Stripe requires amount in cents
                        'product_data': {
                            'name': course.title,
                            'description': course.description[:255],
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(
                    reverse('courses:payment-success')
                ) + f'?session_id={{CHECKOUT_SESSION_ID}}&course_slug={course.slug}',
                cancel_url=request.build_absolute_uri(
                    reverse('courses:payment-cancel')
                ),
                metadata={
                    'course_slug': course.slug,
                    'user_id': request.user.id,
                }
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return JsonResponse({'error': str(e)})

class PaymentSuccessView(LoginRequiredMixin, View):
    """Xử lý thanh toán thành công"""
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        course_slug = request.GET.get('course_slug')
        
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            course = Course.objects.get(slug=course_slug)
            
            # Tạo ghi danh
            enrollment = Enrollment.objects.create(
                student=request.user,
                course=course,
                payment_id=session.payment_intent
            )
            
            # Tạo progress cho mỗi bài học
            Progress.objects.bulk_create([
                Progress(enrollment=enrollment, lesson=lesson)
                for lesson in course.lessons.all()
            ])
            
            return redirect('courses:course-learn', course_slug=course.slug)
        except Exception as e:
            return JsonResponse({'error': str(e)})

class PaymentCancelView(LoginRequiredMixin, View):
    """Xử lý hủy thanh toán"""
    def get(self, request, *args, **kwargs):
        return redirect('courses:course-list')

class CourseLearnView(LoginRequiredMixin, DetailView):
    """Giao diện học khóa học"""
    model = Course
    template_name = 'courses/course_learn.html'
    context_object_name = 'course'
    slug_url_kwarg = 'course_slug'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('lessons')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrollment = get_object_or_404(
            Enrollment,
            student=self.request.user,
            course=self.object
        )
        context['enrollment'] = enrollment
        context['progress'] = Progress.objects.filter(
            enrollment=enrollment
        ).select_related('lesson')
        return context

class LessonDetailView(LoginRequiredMixin, DetailView):
    """Chi tiết bài học"""
    model = Lesson
    template_name = 'courses/lesson_detail.html'
    context_object_name = 'lesson'

    def get_object(self):
        course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        return get_object_or_404(
            Lesson,
            course=course,
            order=self.kwargs['lesson_order']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrollment = get_object_or_404(
            Enrollment,
            student=self.request.user,
            course=self.object.course
        )
        context['progress'] = Progress.objects.get(
            enrollment=enrollment,
            lesson=self.object
        )
        return context

class LessonCompleteView(LoginRequiredMixin, View):
    """Đánh dấu hoàn thành bài học"""
    def post(self, request, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=kwargs['pk'])
        enrollment = get_object_or_404(
            Enrollment,
            student=request.user,
            course=lesson.course
        )
        
        progress = Progress.objects.get(enrollment=enrollment, lesson=lesson)
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()

        # Kiểm tra xem đã hoàn thành tất cả bài học chưa
        all_completed = Progress.objects.filter(
            enrollment=enrollment,
            completed=False
        ).count() == 0

        if all_completed:
            enrollment.completed = True
            enrollment.save()
            
            # Tạo chứng chỉ
            certificate = Certificate.objects.create(
                enrollment=enrollment,
                certificate_number=f"CERT-{enrollment.id}"
            )
            return JsonResponse({
                'status': 'completed',
                'certificate_url': reverse(
                    'courses:certificate-detail',
                    kwargs={'number': certificate.certificate_number}
                )
            })
        
        return JsonResponse({'status': 'success'})

class CertificateDetailView(LoginRequiredMixin, DetailView):
    """Chi tiết chứng chỉ"""
    model = Certificate
    template_name = 'courses/certificate_detail.html'
    context_object_name = 'certificate'
    slug_field = 'certificate_number'
    slug_url_kwarg = 'number'

class CertificateVerifyView(View):
    """Xác thực chứng chỉ"""
    def get(self, request, *args, **kwargs):
        number = request.GET.get('number')
        try:
            certificate = Certificate.objects.select_related(
                'enrollment__student',
                'enrollment__course'
            ).get(certificate_number=number)
            return JsonResponse({
                'valid': True,
                'issued_to': certificate.enrollment.student.get_full_name(),
                'course': certificate.enrollment.course.title,
                'issued_date': certificate.issued_date.strftime('%d/%m/%Y')
            })
        except Certificate.DoesNotExist:
            return JsonResponse({'valid': False})

class UpdateProgressView(LoginRequiredMixin, View):
    """Cập nhật tiến độ học tập"""
    def post(self, request, *args, **kwargs):
        progress_id = request.POST.get('progress_id')
        progress = get_object_or_404(
            Progress,
            id=progress_id,
            enrollment__student=request.user
        )
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()
        return JsonResponse({'status': 'success'})