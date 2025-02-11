"""
URL patterns cho ứng dụng core
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Trang chủ và trang tĩnh
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    
    # Tìm kiếm
    path('search/', views.SearchView.as_view(), name='search'),
    
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    
    # Instructor
    path('instructors/', views.InstructorListView.as_view(), name='instructor-list'),
    path('instructors/<str:username>/', 
         views.InstructorDetailView.as_view(), 
         name='instructor-detail'),
    
    # Blog/Tin tức
    path('blog/', views.BlogListView.as_view(), name='blog-list'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog-detail'),
]