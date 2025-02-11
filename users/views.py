"""
Views for the users app
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from .models import User, UserSettings
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    UserProfileForm,
    PasswordChangeForm,
    NotificationSettingsForm
)

def login_view(request):
    """View để xử lý đăng nhập"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                return redirect(next_url if next_url else 'core:home')
            else:
                messages.error(request, 'Email hoặc mật khẩu không đúng.')
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def signup_view(request):
    """View để xử lý đăng ký"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Đăng ký thành công!')
            return redirect('core:home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/signup.html', {'form': form})

@login_required
def logout_view(request):
    """View để xử lý đăng xuất"""
    logout(request)
    return redirect('core:home')

@login_required
def profile_view(request):
    """View để hiển thị trang cá nhân"""
    return render(request, 'users/profile.html')

@login_required
def profile_edit_view(request):
    """View để chỉnh sửa thông tin cá nhân"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thông tin thành công!')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/profile_edit.html', {'form': form})

@login_required
def settings_view(request):
    """View để hiển thị và xử lý trang cài đặt"""
    # Đảm bảo user có settings
    settings, created = UserSettings.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Xử lý cập nhật thông tin cá nhân
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thông tin thành công!')
            return redirect('users:settings')
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'form': form,
        'settings': settings,
    }
    
    return render(request, 'users/settings.html', context)

@login_required
def change_password_view(request):
    """View để đổi mật khẩu"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Cập nhật session để không bị logout
            update_session_auth_hash(request, user)
            messages.success(request, 'Đổi mật khẩu thành công!')
            return redirect('users:settings')
        else:
            messages.error(request, 'Vui lòng sửa các lỗi bên dưới.')
    else:
        form = PasswordChangeForm(request.user)
    
    return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
@require_http_methods(['POST'])
def update_notification_settings(request):
    """API endpoint để cập nhật cài đặt thông báo"""
    settings = get_object_or_404(UserSettings, user=request.user)
    form = NotificationSettingsForm(request.POST, instance=settings)
    
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_http_methods(['POST'])
def delete_account_view(request):
    """View để xóa tài khoản"""
    user = request.user
    logout(request)
    user.delete()
    messages.success(request, 'Tài khoản của bạn đã được xóa.')
    return redirect('core:home')

@login_required
def user_courses_view(request):
    """View để hiển thị khóa học của user"""
    enrollments = request.user.enrollments.select_related('course').all()
    paginator = Paginator(enrollments, 9)
    page = request.GET.get('page')
    enrollments = paginator.get_page(page)
    
    return render(request, 'users/user_courses.html', {
        'enrollments': enrollments
    })

@login_required
def user_certificates_view(request):
    """View để hiển thị chứng chỉ của user"""
    certificates = request.user.certificates.select_related('enrollment__course').all()
    paginator = Paginator(certificates, 12)
    page = request.GET.get('page')
    certificates = paginator.get_page(page)
    
    return render(request, 'users/user_certificates.html', {
        'certificates': certificates
    })

# Instructor views
@login_required
def instructor_dashboard_view(request):
    """View để hiển thị bảng điều khiển của giảng viên"""
    if not request.user.is_instructor:
        return redirect('core:home')
    
    context = {
        'total_courses': request.user.courses.count(),
        'total_students': request.user.get_total_students(),
        'total_revenue': request.user.get_total_revenue(),
        'recent_enrollments': request.user.get_recent_enrollments(),
        'popular_courses': request.user.get_popular_courses()
    }
    
    return render(request, 'users/instructor/dashboard.html', context)

@login_required
def instructor_courses_view(request):
    """View để hiển thị danh sách khóa học của giảng viên"""
    if not request.user.is_instructor:
        return redirect('core:home')
    
    courses = request.user.courses.all()
    paginator = Paginator(courses, 9)
    page = request.GET.get('page')
    courses = paginator.get_page(page)
    
    return render(request, 'users/instructor/courses.html', {
        'courses': courses
    })

@login_required
def instructor_earnings_view(request):
    """View để hiển thị doanh thu của giảng viên"""
    if not request.user.is_instructor:
        return redirect('core:home')
    
    context = {
        'total_revenue': request.user.get_total_revenue(),
        'total_students': request.user.get_total_students(),
        'earnings_by_course': request.user.get_earnings_by_course(),
        'monthly_data': request.user.get_monthly_earnings()
    }
    
    return render(request, 'users/instructor/earnings.html', context)