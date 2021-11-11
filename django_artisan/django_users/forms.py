from fuzzywuzzy import fuzz

from captcha import fields as captcha_fields, widgets as captcha_widgets 
from crispy_forms import helper, layout
from crispy_bootstrap5 import bootstrap5

from django import forms, urls
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class CustomUserCreationForm(auth.forms.UserCreationForm):
    captcha = captcha_fields.ReCaptchaField(label='', widget=captcha_widgets.ReCaptchaV2Checkbox)
    email = forms.EmailField()

    class Meta(auth.forms.UserCreationForm.Meta):
        fields = auth.forms.UserCreationForm.Meta.fields + ('email', 'captcha',)

    def clean_email(self) -> str:
        email = self.cleaned_data['email']
        try:
            user = auth.get_user_model().objects.get(email=email)
        except auth.models.User.DoesNotExist:
            return email
        self.add_error('email', 'Error! That email already exists!')
        self.valid = False
        return email

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = helper.FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = urls.reverse_lazy('register')
        self.helper.form_tag = False
        self.helper.form_class = ""
        self.helper.layout = layout.Layout(
            bootstrap5.FloatingField('username'),
            bootstrap5.FloatingField('email', autocomplete="new-password"),
            bootstrap5.FloatingField('password1'),
            bootstrap5.FloatingField('password2', autocomplete="new-password"),
            layout.Field('captcha'),
        )


class UserPasswordResetForm(auth.forms.PasswordResetForm):
    captcha = captcha_fields.ReCaptchaField(label='', widget=captcha_widgets.ReCaptchaV2Checkbox)

    def clean_email(self) -> str:
        email = self.cleaned_data['email']
        try:
            user = auth.get_user_model().objects.get(email=email)
            if user.is_active is False:
                self.valid = False
                self.add_error(
                    'email', 'Hey!, you haven\'t finished registering yet, \
                                         perhaps you want to resend a confiration token?')
                return email
        except auth.models.User.DoesNotExist:
            self.valid = False
            self.add_error(
                'email', 'Hey!, you haven\'t registered, perhaps you want to try \
                                     registering first?')
            return email
        return email

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = helper.FormHelper()
        self.helper.form_method = 'post'
        self.fields['email'].label = "Email Here!"
        self.helper.layout = layout.Layout(
            bootstrap5.FloatingField('email', css_class="mb3"),
            layout.Field('captcha'),
            layout.HTML('<div class="row justify-content-end"> \
                    <div class="col-auto"> \
                        <button class="btn btn-primary mt-3" type="submit">Send</button> \
                    </div> \
                  </div>')
        )


class UserResendConfirmationForm(forms.Form):
    captcha = captcha_fields.ReCaptchaField(label='', widget=captcha_widgets.ReCaptchaV2Checkbox)
    username = forms.CharField(label='Your username here...')

    def clean_username(self, *args, **kwargs) -> str:
        username = self.cleaned_data['username']
        try:
            user = auth.get_user_model().objects.get(username=username)
            if user.is_active:
                self.valid = False
                self.add_error(
                    'username', 'Hey, you are already a registered member, perhaps you want to \
                                            Reset your password?')
                return username
        except auth.models.User.DoesNotExist:
            self.valid = False
            self.add_error(
                'username',
                'Hey!  That username does not exist!  Try registering first.')
        return username

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = ""
        self.helper.layout = helper.Layout(
            bootstrap5.FloatingField('username', wrapper_class="col-auto",
                          css_class="mb-3"),
            layout.Field('captcha'),
            layout.HTML('<div class="row justify-content-end"> \
                    <div class="col-auto"> \
                        <button class="btn btn-primary mt-3" type="submit">Send</button> \
                    </div> \
                  </div>')
        )
