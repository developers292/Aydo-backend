from django.urls import path, include
from .api import RegisterAPI, LoginAPI, UserDetailAPI, ChangePasswordAPI, ResetPasswordAPI
from knox import views as knox_views

urlpatterns = [
  path('register', RegisterAPI.as_view()),
  path('login', LoginAPI.as_view()),
  path('user', UserDetailAPI.as_view()),
  path('change-password', ChangePasswordAPI.as_view(), name='change_password'),
  path('reset-password', ResetPasswordAPI.as_view(), name='reset_password'),
  path('logout', knox_views.LogoutView.as_view(), name='knox_logout'),
  path('logout-all', knox_views.LogoutAllView.as_view(), name='knox_logout_all'),
]