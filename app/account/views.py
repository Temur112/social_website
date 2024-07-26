from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetDoneView, PasswordChangeView
from django.urls import reverse_lazy

from .forms import LoginForm


# Create your views here.


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Account logged in")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid credentials")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html',{'section': 'dashboard'})


class ViewLogin(LoginView):
    pass


def log_out(request):
    logout(request)
    return redirect('account:login')


class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')


class ChangePasswordDone(PasswordResetDoneView):
    template_name = 'registration/password_change_done.html'

