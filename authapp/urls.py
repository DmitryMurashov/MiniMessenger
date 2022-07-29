from django.urls import path
from authapp import views as authapp

app_name = 'authapp'

urlpatterns = [
    path('register/', authapp.RegisterApiView.as_view(), name='register'),
    path('login/', authapp.LoginApiView.as_view(), name='login'),
    path('profile/', authapp.ProfileApiView.as_view(), name='profile')
]
