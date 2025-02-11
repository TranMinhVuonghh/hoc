"""
URL Configuration chính cho dự án
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),
    
    # Authentication URLs (django-allauth)
    path('accounts/', include('allauth.urls')),
    
    # Local apps URLs
    path('', include('core.urls')),
    path('courses/', include('courses.urls')),
    path('users/', include('users.urls')),
]

# Serving media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)