# users/forms.py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, EmailField
from django.urls import reverse_lazy

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Fieldset, HTML, Button, Div
from crispy_forms.bootstrap import StrictButton
from .fields import FloatingField


class CustomUserCreationForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    email = EmailField()
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'captcha',)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email          
        self.add_error('email', 'Error! That email already exists!')
        self.valid = False
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('register')
        self.helper.form_class = "col-12 col-sm-10 col-md-7 col-lg-5 mx-auto"
        self.helper.layout = Layout(
            Fieldset(
                'Register',
                FloatingField('username'),
                FloatingField('email'),
                FloatingField('password1'),
                FloatingField('password2'),
                FloatingField('captcha'),
                Div(
                HTML('<a href="{% url \"login\" %}" class="col-auto me-auto text-white" role="return-to-login-link" >Back to login</a>'),
                Submit('Register', 'Register', css_class='btn-default col-auto role="register-button"'),
                css_class="row justify-content-between"),
                ), 
            )