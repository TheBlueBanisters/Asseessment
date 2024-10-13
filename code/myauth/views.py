from django.shortcuts import render, redirect,reverse
from django.http import JsonResponse
import string
import random
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

from .models import Captcha
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm,LoginForm
from  django.contrib.auth import get_user_model,login,logout

from django.contrib.auth.models import User
# Create your views here.

User = get_user_model()
@csrf_exempt
@require_http_methods(['GET', 'POST'])
def auth_login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request, user)
                if not remember:
                    # 设置过期时间
                    request.session.set_expiry(0)
                return redirect('/')
            else:
                print('密码错误')
                form.add_error('email','邮箱或者密码错误！')
                # ？？
                # return render(request,'login.html',{'form':form})
                return redirect(reverse('myauth:auth_login'))


@require_http_methods(['GET','POST'])
def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # 密码会被加密后再存储
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('myauth:auth_login'))
        else:

            return redirect(reverse('myauth:register'))
def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code':400,'message':'请输入有效的邮箱地址'})
    captcha=''.join(random.sample(string.digits,4))
    Captcha.objects.update_or_create(email=email,defaults={'captcha':captcha})
    send_mail('校园博客注册验证',message=f'您的注册验证码是{captcha}。',recipient_list=[email],from_email=None)
    return JsonResponse({'code':200, "message":'验证码已发送！请注意查收'})

def logout_1(request):
    logout(request)
    return redirect('/')