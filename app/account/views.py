from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetDoneView, PasswordChangeView, PasswordResetView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from .forms import RegisterForm, LoginForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages


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


class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('account:password_reset_done')

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email,
                  html_email_template_name=None):
        # Debugging output
        print("Sending email to:", to_email)
        print("Email subject:", subject_template_name)
        print("Email body context:", context)

        # Call the parent class's send_mail method
        send_mail(subject_template_name, email_template_name, context, from_email, to_email,
                          html_email_template_name)


class CustomPasswordResetDoneView(PasswordResetView):
    template_name = 'registration/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    pass


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    pass


def register(request):
    if request.method == 'POST':
        r_form = RegisterForm(request.POST)
        if r_form.is_valid():
            new_user = r_form.save(commit=False)
            new_user.set_password(
                r_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        r_form = RegisterForm()

    return render(request, 'account/register.html', {'form': r_form})


@login_required()
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserEditForm(instance=request.user, data=request.POST)
        p_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'profile updated successfully')
        else:
            messages.error(request, 'An error occurred while updating profile')
    else:
        u_form = UserEditForm(instance=request.user)
        p_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit_profile.html', {'u_form': u_form, 'p_form': p_form})
