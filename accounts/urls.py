from django.urls import path, include
from .api import RegisterAPI, LoginAPI, UserAPI, ChangePasswordAPI
from knox import views as knox_views

urlpatterns = [
  path('register', RegisterAPI.as_view()),
  path('login', LoginAPI.as_view()),
  path('user', UserAPI.as_view()),
  path('change-password', ChangePasswordAPI.as_view(), name='change_password'),
  path('logout', knox_views.LogoutView.as_view(), name='knox_logout'),
  path('logout-all', knox_views.LogoutAllView.as_view(), name='knox_logout_all'),
]