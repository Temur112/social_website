from django.urls import path
from django.contrib.auth import views as auth_views

from account import views

app_name = 'account'
urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('login/', views.ViewLogin.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', views.log_out, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', views.ChangePasswordDone.as_view(), name='password_change_done'),
]
