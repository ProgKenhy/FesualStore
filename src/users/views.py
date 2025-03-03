from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import CommonMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserLoginView(CommonMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')
    title = 'Авторизация'


class UserRegistrationView(CommonMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = _('Вы успешно зарегистрированы!')
    title = 'Регистрация'


class UserProfileView(CommonMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Личный кабинет'

    def get_success_url(self):
        messages.success(self.request, _('Профиль успешно обновлен'))
        return reverse_lazy('users:profile', args=[self.object.id])

    def form_invalid(self, form):
        messages.error(self.request, _('Ошибка обновления профиля. Проверьте данные'))
        return super().form_invalid(form)


class EmailVerificationView(CommonMixin, TemplateView):
    title = 'Подтверждение почты'
    template_name = 'users/password/email_verification.html'

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=kwargs['email'])
            code = kwargs['code']
            email_verifications = EmailVerification.objects.filter(user=user, code=code)

            if email_verifications.exists() and not email_verifications.first().is_expired():
                user.is_verified_email = True
                user.save()
                messages.success(request, _('Email успешно подтвержден!'))
                return super().get(request, *args, **kwargs)
            else:
                messages.error(request, _('Ссылка для подтверждения недействительна или истекла'))
                return HttpResponseRedirect(reverse('index'))

        except User.DoesNotExist:
            messages.error(request, _('Пользователь не найден'))
            return HttpResponseRedirect(reverse('index'))


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password/password_reset.html'
    email_template_name = 'users/password/password_reset_email.html'
    subject_template_name = 'users/password/password_reset_subject'
    success_message = _(
        "Инструкции по сбросу пароля отправлены на ваш email. "
        "Если вы не получили письмо, проверьте спам или правильность email."
    )
    success_url = reverse_lazy('users:login')

    def form_invalid(self, form):
        messages.error(
            self.request,
            _('Ошибка отправки письма. Проверьте введенный email')
        )
        return super().form_invalid(form)
