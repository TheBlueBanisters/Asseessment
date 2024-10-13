from os.path import exists

from django import forms

from django.contrib.auth import get_user_model

from .models import Captcha

User = get_user_model()


# 验证码表单
class RegisterForm(forms.Form):
    username=forms.CharField(max_length=20,min_length=2,error_messages={
        'required':'请输入用户名',
        'max_length':'用户名过长',
        'min_length':'用户名过短'})
    email=forms.EmailField(error_messages={'required':'请输入邮箱','invalid':'请输入有效的邮箱'})
    captcha = forms.CharField(min_length=4,max_length=4)
    password = forms.CharField(min_length=6,max_length=20,error_messages={
        'required':'请输入密码',
        'min_length':'密码的最小长度为6个字符',
        'max_length':'密码的最大长度为20个字符'
    })

    def clean_email(self):
        email=self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('邮箱已经被注册!')
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')

        captcha_model = Captcha.objects.filter(email=email,captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError('验证码错误！')
        captcha_model.delete()
        return captcha

class LoginForm(forms.Form):
    email=forms.EmailField(error_messages={'required':'请输入邮箱','invalid':'请输入有效的邮箱'})
    password = forms.CharField(min_length=6,max_length=20,error_messages={
        'required':'请输入密码',
        'min_length':'密码的最小长度为6个字符',
        'max_length':'密码的最大长度为20个字符'
    })

    remember = forms.IntegerField(required=False)
