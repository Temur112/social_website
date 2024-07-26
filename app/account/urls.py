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
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.register, name='register'),
]
