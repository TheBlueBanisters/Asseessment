from django.urls import path
from . import views

app_name= 'myauth'


urlpatterns=[
    path('login/',views.auth_login,name='auth_login'),
    path('register/',views.register,name='register'),
    path('captcha',views.send_email_captcha,name='captcha'),
    path('logout/',views.logout_1,name='logout'),


]