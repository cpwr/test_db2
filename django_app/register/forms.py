from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('email', 'birthday', 'country', 'city')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        u = User.objects.filter(email__iexact=email)
        if u.exists():
            raise forms.ValidationError(
                "Cannot use this email. It's already registered"
            )
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        print(self.cleaned_data)
        user = super(RegisterForm, self).save(commit=False)
        print(user)
        print(type(user))
        user.password = self.cleaned_data["password1"]
        user.is_active = False

        if commit:
            user.save()
            user.send_activation_email()

        return user


class LoginForm(forms.ModelForm):

    error_messages = {
        'invalid_login':
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive.",
        'inactive': "This account is inactive.",
    }

    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(
            attrs={
                'required': 'required',
                'type': 'email'
            }
        )
    )
    password = forms.CharField(
        label=u'Password',
        widget=forms.PasswordInput(
            attrs={
                'required': 'required'
            }
        )
    )

    class Meta:
        model = User
        fields = ('email', 'password')

    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.username_field = User._meta.get_field(User.USERNAME_FIELD)

    def get_user(self):
        return self.user_cache

    def is_valid(self):
        valid = super(LoginForm, self).is_valid()

        if not valid:
            return valid

        email_lower = self.cleaned_data['email'].lower()
        user = User.objects.get(email=email_lower)
        if not user:
            self._errors['email'] = u'Email does not exist in database.'
            return False

        valid_password = user.check_password(self.cleaned_data['password'])

        if not valid_password:
            self._errors['email'] = 'You entered wrong password.'
            return False

        if not user.is_active:
            self._errors['email'] = (
                'Please check your email before you continue.'
            )
            return False

        return True

    def clean(self):

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            print(self.user_cache)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'email': self.username_field.verbose_name},
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return self.cleaned_data
