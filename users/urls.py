from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # Profile
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile-edit'),
    path('profile/delete/', views.profile_delete_view, name='profile-delete'),
    
    # Settings
    path('settings/', views.settings_view, name='settings'),
    path('settings/password/', views.change_password_view, name='change-password'),
    path('settings/delete-account/', views.delete_account_view, name='delete-account'),
    
    # API endpoints for settings
    path('api/settings/notifications/', views.update_notification_settings, name='update-notifications'),

    # Courses
    path('my-courses/', views.user_courses_view, name='user-courses'),
    path('my-certificates/', views.user_certificates_view, name='user-certificates'),

    # Instructor
    path('instructor/dashboard/', views.instructor_dashboard_view, name='instructor-dashboard'),
    path('instructor/courses/', views.instructor_courses_view, name='instructor-courses'),
    path('instructor/earnings/', views.instructor_earnings_view, name='instructor-earnings'),
    path('instructor/course/create/', views.course_create_view, name='course-create'),
    path('instructor/course/<slug:slug>/edit/', views.course_edit_view, name='course-edit'),
    path('instructor/course/<slug:slug>/delete/', views.course_delete_view, name='course-delete'),
    path('instructor/course/<slug:slug>/lessons/', views.course_lessons_view, name='course-lessons'),
    path('instructor/course/<slug:slug>/lesson/create/', views.lesson_create_view, name='lesson-create'),
    path('instructor/course/<slug:slug>/lesson/<int:order>/edit/', views.lesson_edit_view, name='lesson-edit'),
    path('instructor/course/<slug:slug>/lesson/<int:lesson_id>/delete/', views.lesson_delete_view, name='lesson-delete'),
]