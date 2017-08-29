from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView as _LoginView
from django.contrib.auth.views import LogoutView as _LogoutView
from django.contrib.auth import get_user_model
from django.urls.base import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import redirect

# Create your views here.

from .forms import RegisterForm
from .forms import LoginForm

User = get_user_model()


def activate_user_view(request, code=None):

    if code:
        qs = User.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.confirmed:
                profile.confirm(code)
                profile.activation_key = None
                profile.save()
    return redirect("login")


class RegisterView(SuccessMessageMixin, CreateView):

    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    success_message = (
        "Your account was created successfully."
        " Please check your email."
    )


class LoginView(_LoginView):
    """
    Displays the login form and handles the login action.
    """
    form_class = LoginForm
    success_url = reverse_lazy('blog:home')


class LogoutView(_LogoutView):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    next_page = reverse_lazy('login')
