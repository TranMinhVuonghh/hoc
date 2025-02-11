"""
Models for the users app
"""
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

class UserManager(BaseUserManager):
    """Custom user model manager"""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email là bắt buộc')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """Custom user model"""
    username = None
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    is_instructor = models.BooleanField(default=False)
    title = models.CharField(max_length=100, blank=True)  # For instructors
    expertise = models.CharField(max_length=200, blank=True)  # For instructors
    website = models.URLField(blank=True)  # For instructors

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """Return user's full name"""
        return f"{self.first_name} {self.last_name}".strip() or self.email

    def get_total_students(self):
        """Get total number of students for instructor"""
        if not self.is_instructor:
            return 0
        return self.courses.aggregate(
            total_students=Count('enrollments', distinct=True)
        )['total_students'] or 0

    def get_total_revenue(self):
        """Get total revenue for instructor"""
        if not self.is_instructor:
            return 0
        return self.courses.aggregate(
            total_revenue=Sum('enrollments__payment__amount')
        )['total_revenue'] or 0

    def get_earnings_by_course(self):
        """Get earnings breakdown by course"""
        if not self.is_instructor:
            return []
        return self.courses.annotate(
            revenue=Sum('enrollments__payment__amount'),
            student_count=Count('enrollments', distinct=True)
        ).values('title', 'revenue', 'student_count', 'image', 'created_at')

    def get_monthly_earnings(self):
        """Get monthly earnings data for the past 12 months"""
        if not self.is_instructor:
            return {'labels': [], 'values': []}

        end_date = timezone.now()
        start_date = end_date - timedelta(days=365)
        
        monthly_data = self.courses.filter(
            enrollments__payment__created_at__range=[start_date, end_date]
        ).values(
            'enrollments__payment__created_at__month',
            'enrollments__payment__created_at__year'
        ).annotate(
            total=Sum('enrollments__payment__amount')
        ).order_by(
            'enrollments__payment__created_at__year',
            'enrollments__payment__created_at__month'
        )

        labels = []
        values = []
        for data in monthly_data:
            month = data['enrollments__payment__created_at__month']
            year = data['enrollments__payment__created_at__year']
            labels.append(f"{month}/{year}")
            values.append(float(data['total']))

        return {
            'labels': labels,
            'values': values
        }

    def get_recent_enrollments(self, limit=5):
        """Get recent enrollments for instructor's courses"""
        if not self.is_instructor:
            return []
        return self.courses.prefetch_related('enrollments__student').order_by(
            '-enrollments__created_at'
        )[:limit]

    def get_popular_courses(self, limit=5):
        """Get most popular courses by enrollment count"""
        if not self.is_instructor:
            return []
        return self.courses.annotate(
            student_count=Count('enrollments')
        ).order_by('-student_count')[:limit]

class UserSettings(models.Model):
    """User settings model"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='settings'
    )
    course_updates = models.BooleanField(
        _('course updates notifications'),
        default=True,
        help_text=_('Receive notifications about course updates')
    )
    marketing_emails = models.BooleanField(
        _('marketing emails'),
        default=False,
        help_text=_('Receive marketing emails')
    )
    public_profile = models.BooleanField(
        _('public profile'),
        default=False,
        help_text=_('Make your profile visible to others')
    )
    show_progress = models.BooleanField(
        _('show progress'),
        default=True,
        help_text=_('Show your learning progress to others')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('user settings')
        verbose_name_plural = _('user settings')

    def __str__(self):
        return f"Settings for {self.user.email}"