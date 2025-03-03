from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.core.exceptions import ValidationError

from users.models import User
from users.tasks import send_email_verification


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': "Введите имя пользователя"
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'placeholder': "Введите пароль"
        })
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': "Введите ваше имя"
        })
    )
    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': "Введите вашу фамилию"
        })
    )
    username = forms.CharField(
        label="Логин",
        help_text="Уникальное имя для входа в систему",
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': "Придумайте логин"
        })
    )
    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(attrs={
            'class': "form-control",
            'placeholder': "example@domain.com"
        })
    )
    password1 = forms.CharField(
        label="Пароль",
        help_text="Минимум 8 символов. Используйте буквы, цифры и специальные символы.",
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'placeholder': "Придумайте надежный пароль"
        })
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'placeholder': "Повторите пароль"
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        error_messages = {
            'username': {
                'unique': "Пользователь с таким логином уже существует.",
            },
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают.", code="password_mismatch")

        username = self.cleaned_data.get("username", "")
        if username and len(password1) < 8:
            raise ValidationError("Пароль должен содержать как минимум 8 символов.", code="password_too_short")

        if username and username.lower() in password1.lower():
            raise ValidationError("Пароль не должен содержать ваш логин.", code="password_too_similar")

        return password2

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        send_email_verification.delay(user.id)
        return user


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        label="Фото профиля",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        required=False
    )
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True})
    )
    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': True})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')
