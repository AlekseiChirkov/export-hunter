from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from apps.users import views


app_name = "users"

urlpatterns = [
    # simple jwt
    path('token/',
         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),

    # password reset
    path('password-reset/',
         include('django_rest_passwordreset.urls',
                 namespace='password_reset')),

    # app
    path('register/',
         views.UserRegistrationView.as_view(), name='register'),
    path('login/',
         views.UserLoginView.as_view(), name='login'),
    path('change-password/',
         views.UserChangePasswordView.as_view(), name='change_password'),
]
