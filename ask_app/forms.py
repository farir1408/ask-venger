from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator

from django.contrib.auth.hashers import make_password
from ask_app.models import Profile, Question

textValidator = RegexValidator(r"[а-яА-Яa-zA-Z]",
                               "Text should contain letters")

class AskQuestion(forms.Form):
    title = forms.CharField(validators=[textValidator],
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'maxlength': 100,
                                                          'minlength': 10,
                                                          'placeholder': 'Write here your title'}), label=u'title')

    text = forms.CharField(validators=[textValidator],
                           widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'minlength': 30,
                                                        'placeholder': 'And here tell about your question in more detail'}),
                           label=u'text'
                           )


class LoginForm(forms.Form):
    login = forms.CharField(
            widget=forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'login', }),
            max_length=30,
            label=u'Login'
            )

    password = forms.CharField(
            widget=forms.PasswordInput(attrs={ 'class': 'form-control', 'placeholder': '*******', }),
            label=u'Password'
            )

    def clean(self):
        data = self.cleaned_data
        user = authenticate(username=data.get('login', ''), password=data.get('password', ''))

        if user is not None:
            if user.is_active:
                data['user'] = user
            else:
                raise forms.ValidationError(u'This user don\'t active')
        else:
            raise forms.ValidationError(u'Uncorrect login or password')

class SignupForm(forms.Form):
    username = forms.CharField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Login', }),
            max_length=30, label=u'Login'
            )
    first_name = forms.CharField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': u'Oleg', }),
            max_length=30, label=u'Name'
            )
    last_name = forms.CharField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': u'Venger', }),
            max_length=30, label=u'Second name'
            )
    email = forms.EmailField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'OVenger@gmail.com', }),
            required = False, max_length=254, label=u'E-mail'
            )
    password1 = forms.CharField(
            widget=forms.PasswordInput( attrs={ 'class': 'form-control', 'placeholder': '*****' }),
            min_length=6, label=u'Password'
            )
    password2 = forms.CharField(
            widget=forms.PasswordInput( attrs={ 'class': 'form-control', 'placeholder': '*****' }),
            min_length=6, label=u'Repeat password'
            )
    info = forms.CharField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': u'...', }),
            required=False, label=u'Status'
            )
    avatar = forms.FileField(
            widget=forms.ClearableFileInput( attrs={ 'class': 'ask-signup-avatar-input', }),
            required=False, label=u'Avatar'
            )

    def clean_username(self):
        username = self.cleaned_data.get('username', '')

        try:
            u = User.objects.get(username=username)
            raise forms.ValidationError(u'User exist')
        except User.DoesNotExist:
            return username

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1', '')
        pass2 = self.cleaned_data.get('password2', '')

        if pass1 != pass2:
            raise forms.ValidationError(u'Passwords not equal')

    def save(self):
        data = self.cleaned_data
        password = data.get('password1')
        u = User()

        u.username = data.get('username')
        u.password = make_password(password)
        u.email = data.get('email')
        u.first_name = data.get('first_name')
        u.last_name = data.get('last_name')
        u.is_active = True
        u.is_superuser = False
        u.save()

        up = Profile()
        up.user = u
        up.info = data.get('info')
        up.save()

        return authenticate(username=u.username, password=password)