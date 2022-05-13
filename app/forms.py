from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from app.models import Profile, Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField(label='Nickname:', max_length=256, widget=forms.TextInput(
        attrs={'placeholder': 'Your nickname', 'style': 'margin: 5px 0px 18px 0px; '}))
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(
        attrs={'placeholder': '123456', 'style': 'margin: 5px 0px 18px 0px; '}))


class RegisterForm(forms.Form):
    model = Profile
    username = forms.CharField(label='Nickname:', max_length=256,
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Your nickname', 'style': 'margin: 5px 0px 18px 0px; '}))
    email = forms.EmailField(label='Email:', required=False,
                             widget=forms.TextInput(
                                 attrs={'placeholder': 'exapmle@email.com', 'style': 'margin: 5px 0px 18px 0px; '}))
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(
        attrs={'placeholder': '123456', 'style': 'margin: 5px 0px 18px 0px; '}))
    password_repeat = forms.CharField(label='Repeat password:',
                                      widget=forms.PasswordInput(
                                          attrs={'placeholder': '123456', 'style': 'margin: 5px 0px 18px 0px; '}))
    avatar = forms.ImageField(label='Avatar:', required=False, widget=forms.FileInput(
        attrs={'class': "form-control", 'style': 'margin: 5px 0px 18px 0px; ', 'onchange': 'loadFile(event)'}))

    def clean_password(self):
        if len(self.cleaned_data['password']) < 5:
            raise ValidationError("Password should contain at least 5 chars")
        return self.cleaned_data['password']

    def clean_password_repeat(self):
        pwd = self.cleaned_data.get('password')
        pwd_rep = self.cleaned_data.get('password_repeat')
        if not pwd_rep:
            raise ValidationError("Password should be confirmed")
        if pwd != pwd_rep:
            raise ValidationError("Passwords do not match")
        return pwd_rep


class SettingsForm(RegisterForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['password_repeat'].required = False

    def clean_password(self):
        if 0 < len(self.cleaned_data['password']) < 5:
            raise ValidationError("New password should contain at least 5 chars")
        return self.cleaned_data['password']

    def clean_password_repeat(self):
        pwd = self.cleaned_data.get('password')
        pwd_rep = self.cleaned_data.get('password_repeat')
        if not pwd_rep and pwd:
            raise ValidationError("Password should be confirmed")
        if pwd != pwd_rep:
            raise ValidationError("Passwords do not match")
        return pwd_rep


class AskForm(forms.Form):
    title = forms.CharField(label='Title:', max_length=256, widget=forms.TextInput(
        attrs={'placeholder': 'What is your question about?', 'style': 'margin: 5px 0px 18px 0px; '}))

    text = forms.CharField(label='Text:', widget=forms.Textarea(
        attrs={'placeholder': 'I want to....', 'style': 'margin: 5px 0px 18px 0px; '}))

    tags = forms.CharField(label='Tags:', max_length=256, widget=forms.TextInput(
        attrs={'placeholder': 'Cats, Cars, etc...', 'style': 'margin: 5px 0px 18px 0px; '}), validators=[
        RegexValidator(
            regex='(^(\w+))(,(\s)*(\w)+)*$',
            message='Usage: "Tag1, Tag2, etc"',
        ),
    ])

    def clean_title(self):
        clean_title = self.cleaned_data['title']
        if len(clean_title) < 10:
            raise ValidationError('Too short title')
        return clean_title

    def clean_text(self):
        clean_text = self.cleaned_data['text']
        if len(clean_text) < 20:
            raise ValidationError('Describe your question more exactly')
        return clean_text

    def clean_tags(self):
        clean_tags = self.cleaned_data['tags']
        if len(clean_tags) < 3:
            raise ValidationError('Set at least one valid Tag')
        return clean_tags


class AnswerForm(forms.ModelForm):
    text = forms.CharField(label='Your answer:', widget=forms.Textarea(
        attrs={'placeholder': 'I can suggest to....', 'style': 'margin: 5px 0px 18px 0px; '}))

    class Meta:
        model = Answer
        fields = ['text']

    def clean_text(self):
        cleaned_text = self.cleaned_data['text']
        if len(cleaned_text) < 2:
            raise ValidationError('Too short answer')
        return cleaned_text
