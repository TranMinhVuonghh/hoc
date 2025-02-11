"""
Forms for the users app
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm as BasePasswordChangeForm
from django.core.validators import FileExtensionValidator
from .models import User, UserSettings

class UserRegistrationForm(UserCreationForm):
    """Form để đăng ký người dùng mới"""
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-input'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'})
        }

    def clean_email(self):
        """Kiểm tra email đã được sử dụng chưa"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email này đã được sử dụng.')
        return email

class UserLoginForm(forms.Form):
    """Form để đăng nhập"""
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-input'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

class UserProfileForm(forms.ModelForm):
    """Form để chỉnh sửa thông tin cá nhân"""
    avatar = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])],
        widget=forms.FileInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'bio')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'bio': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': 'Viết đôi điều về bạn...'
            })
        }

    def clean_avatar(self):
        """Kiểm tra kích thước avatar"""
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 2 * 1024 * 1024:  # 2MB
                raise forms.ValidationError('Kích thước ảnh không được vượt quá 2MB.')
        return avatar

class PasswordChangeForm(BasePasswordChangeForm):
    """Form để đổi mật khẩu"""
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    def clean_new_password2(self):
        """Kiểm tra xác nhận mật khẩu mới"""
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Mật khẩu xác nhận không khớp.')
        return password2

class NotificationSettingsForm(forms.ModelForm):
    """Form để cập nhật cài đặt thông báo"""
    class Meta:
        model = UserSettings
        fields = ('course_updates', 'marketing_emails', 'public_profile', 'show_progress')
        widgets = {
            'course_updates': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'marketing_emails': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'public_profile': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_progress': forms.CheckboxInput(attrs={'class': 'form-checkbox'})
        }

class InstructorProfileForm(UserProfileForm):
    """Form để chỉnh sửa thông tin giảng viên"""
    class Meta(UserProfileForm.Meta):
        fields = UserProfileForm.Meta.fields + ('title', 'expertise', 'website')
        widgets = {
            **UserProfileForm.Meta.widgets,
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'expertise': forms.TextInput(attrs={'class': 'form-input'}),
            'website': forms.URLInput(attrs={'class': 'form-input'})
        }